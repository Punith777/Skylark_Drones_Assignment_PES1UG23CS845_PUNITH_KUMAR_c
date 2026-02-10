import os
import json
from groq import Groq

from sheets import read_sheet
from tools import (
    assign_resources,
    urgent_reassignment,
    update_pilot_status,
    update_drone_status
)

# ----------------------------
# Groq API Setup
# ----------------------------
# Ensure your actual API key is set here or via environment variable
os.environ["GROQ_API_KEY"] = "YOUR_GROQ_API_KEY"
client = Groq()


# ----------------------------
# Extract filters from query
# ----------------------------
def extract_filters(user_query):

    prompt = f"""
Extract structured filters from user query.

Entities:
- pilots
- drones
- missions

Fields:
- skills
- certifications
- location
- status
- project

Return JSON only.

Examples:

User: available pilots
{{"entity":"pilots","status":"Available"}}

User: pilots in Mumbai
{{"entity":"pilots","location":"Mumbai"}}

User: missions in Mumbai
{{"entity":"missions","location":"Mumbai"}}

User: pilots with mapping skills
{{"entity":"pilots","skills":["mapping"]}}

User: pilots with night ops certification
{{"entity":"pilots","certifications":["night ops"]}}

User query:
{user_query}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.choices[0].message.content

    # Safe JSON extraction
    try:
        start = content.index("{")
        end = content.rindex("}") + 1
        return json.loads(content[start:end])
    except:
        return {"entity": "pilots"}


# ----------------------------
# Apply dataset filters
# ----------------------------
def filter_data(filters, user_query):

    entity = filters.get("entity", "pilots")

    if entity == "pilots":
        df = read_sheet("pilot_roster")
    elif entity == "drones":
        df = read_sheet("drone_fleet")
    elif entity == "missions":
        df = read_sheet("missions")
    else:
        return "Unknown entity."

    query_lower = user_query.lower()

    # -------- Location filter --------
    if "location" in filters and "location" in df.columns:
        df = df[df["location"].str.lower()
                == filters["location"].lower()]

    # -------- Status filter --------
    if "status" in filters and "status" in df.columns:
        df = df[df["status"].str.lower()
                == filters["status"].lower()]

    # Automatic availability detection
    if "available" in query_lower and "status" in df.columns:
        df = df[df["status"].str.lower() == "available"]

    # -------- Skills filter --------
    if "skills" in filters and "skills" in df.columns:
        for skill in filters["skills"]:
            df = df[df["skills"].str.lower()
                    .str.contains(skill.lower())]

    # -------- Certification filter (LLM output) --------
    if "certifications" in filters and "certifications" in df.columns:
        for cert in filters["certifications"]:
            df = df[df["certifications"].str.lower()
                    .str.contains(cert.lower())]

    # -------- Backup certification detection --------
    if "certification" in query_lower and "certifications" in df.columns:
        words = query_lower.replace(",", "").split()

        all_certs_text = df["certifications"].str.lower().str.cat(sep=" ")

        for word in words:
            if word in all_certs_text:
                df = df[df["certifications"]
                        .str.lower()
                        .str.contains(word)]

    if df.empty:
        return "No records found."

    return df


# ----------------------------
# Main Agent Function
# ----------------------------
def run_agent(user_query):

    query_lower = user_query.lower()

    # -------- Assignment --------
    if query_lower.startswith("assign"):
        project = user_query.split()[-1]
        result = assign_resources(project)
        return {"type": "text", "data": result}

    # -------- Urgent reassignment --------
    if "urgent" in query_lower and "reassignment" in query_lower:
        project = user_query.split()[-1]
        result = urgent_reassignment(project)
        return {"type": "text", "data": result}

    # -------- Pilot status update --------
    if query_lower.startswith("set pilot"):
        parts = user_query.split()
        if len(parts) >= 4:
            name = parts[2]
            status = " ".join(parts[3:])
            result = update_pilot_status(name, status.title())
            return {"type": "text", "data": result}

    # -------- Drone status update --------
    if query_lower.startswith("set drone"):
        parts = user_query.split()
        if len(parts) >= 4:
            drone_id = parts[2]
            status = " ".join(parts[3:])
            result = update_drone_status(drone_id, status.title())
            return {"type": "text", "data": result}

    # -------- Normal query --------
    filters = extract_filters(user_query)
    result = filter_data(filters, user_query)

    if isinstance(result, str):
        return {"type": "text", "data": result}

    return {"type": "table", "data": result}

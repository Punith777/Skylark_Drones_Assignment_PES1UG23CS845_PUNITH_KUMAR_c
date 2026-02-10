# # from tools import (
# #     available_pilots,
# #     available_drones,
# #     assign_resources,
# #     urgent_reassignment,
# #     suggest_assignment
# # )


# # def agent_reply(message):

# #     msg = message.lower()

# #     # ---- PILOTS ----
# #     if "pilot" in msg and ("available" in msg or "show" in msg):
# #         pilots = available_pilots()
# #         return pilots.to_string(index=False)

# #     # ---- DRONES ----
# #     if "drone" in msg and ("available" in msg or "show" in msg):
# #         drones = available_drones()
# #         return drones.to_string(index=False)

# #     # ---- SUGGEST ASSIGNMENT ----
# #     if "suggest" in msg:
# #         project_id = message.split()[-1]
# #         return suggest_assignment(project_id)

# #     # ---- ASSIGN ----
# #     if "assign" in msg:
# #         project_id = message.split()[-1]
# #         return assign_resources(project_id)

# #     # ---- URGENT REASSIGNMENT ----
# #     if "reassignment" in msg:
# #         project_id = message.split()[-1]
# #         return urgent_reassignment(project_id)

# #     return "Sorry, I didn't understand."
# from tools import (
#     available_pilots,
#     available_drones,
#     assign_resources,
#     urgent_reassignment,
#     suggest_assignment
# )


# def format_table(df):
#     if df.empty:
#         return "No data found."

#     lines = []
#     for _, row in df.iterrows():
#         lines.append(" | ".join(str(v) for v in row))

#     return "\n".join(lines)


# def agent_reply(message):

#     msg = message.lower()

#     # ---- PILOTS ----
#     if "pilot" in msg and ("available" in msg or "show" in msg):
#         pilots = available_pilots()
#         return format_table(pilots)

#     # ---- DRONES ----
#     if "drone" in msg and ("available" in msg or "show" in msg):
#         drones = available_drones()
#         return format_table(drones)

#     # ---- SUGGEST ASSIGNMENT ----
#     if "suggest" in msg:
#         project_id = message.split()[-1]
#         return suggest_assignment(project_id)

#     # ---- ASSIGN ----
#     if "assign" in msg:
#         project_id = message.split()[-1]
#         return assign_resources(project_id)

#     # ---- URGENT REASSIGNMENT ----
#     if "reassignment" in msg:
#         project_id = message.split()[-1]
#         return urgent_reassignment(project_id)

#     return "Sorry, I didn't understand."


from tools import (
    available_pilots,
    available_drones,
    assign_resources,
    urgent_reassignment,
    suggest_assignment
)
from sheets import read_sheet


def agent_reply(message):

    msg = message.lower()

    # PILOTS
    if "pilot" in msg and ("available" in msg or "show" in msg):
        pilots = available_pilots()
        return {"type": "table", "data": pilots}

    # DRONES
    if "drone" in msg and ("available" in msg or "show" in msg):
        drones = available_drones()
        return {"type": "table", "data": drones}

    # Suggest assignment
    if "suggest" in msg:
        project_id = message.split()[-1]
        return {"type": "text", "data": suggest_assignment(project_id)}

    # Assign
    if "assign" in msg:
        project_id = message.split()[-1]
        return {"type": "text", "data": assign_resources(project_id)}

    # Urgent reassignment
    if "reassignment" in msg:
        project_id = message.split()[-1]
        return {"type": "text", "data": urgent_reassignment(project_id)}

    return {"type": "text", "data": "Sorry, I didn't understand."}

def get_context():

    pilots = read_sheet("pilot_roster").to_string()
    drones = read_sheet("drone_fleet").to_string()
    missions = read_sheet("missions").to_string()

    context = f"""
Pilot Data:
{pilots}

Drone Fleet:
{drones}

Missions:
{missions}
"""
    return context


def llm_answer(user_query):

    context = get_context()

    prompt = f"""
You are a drone operations coordinator.

Use the dataset below to answer user queries.

DATA:
{context}

User question:
{user_query}

Answer clearly and concisely.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content

def run_agent(query):
    return llm_answer(query)

# from sheets import read_sheet, update_row


# # -----------------------------
# # Available Pilots
# # -----------------------------
# def available_pilots(location=None):
#     df = read_sheet("pilot_roster")

#     df = df[df["status"] == "Available"]

#     if location:
#         df = df[df["location"] == location]

#     return df[["name", "skills", "location", "status"]]


# # -----------------------------
# # Pilots by Skill
# # -----------------------------
# def pilots_by_skill(skill_query):

#     pilots = read_sheet("pilot_roster")

#     skills = [s.strip() for s in skill_query.split(",")]

#     mask = True
#     for skill in skills:
#         mask = mask & pilots["skills"].str.contains(skill, case=False)

#     pilots = pilots[mask]

#     if pilots.empty:
#         return "No pilots found."

#     return pilots[["name", "skills", "location", "status"]]


# # -----------------------------
# # Available Drones
# # -----------------------------
# def available_drones(location=None):
#     df = read_sheet("drone_fleet")

#     df = df[df["status"] == "Available"]

#     if location:
#         df = df[df["location"] == location]

#     return df[["drone_id", "model", "location", "status"]]


# # -----------------------------
# # Fleet Status
# # -----------------------------
# def fleet_status():
#     return read_sheet("drone_fleet")


# # -----------------------------
# # Mission Fetch
# # -----------------------------
# def get_mission(project_id):
#     df = read_sheet("missions")

#     mission = df[df["project_id"] == project_id]

#     if mission.empty:
#         return None

#     return mission.iloc[0]


# # -----------------------------
# # Eligible Pilots
# # -----------------------------
# def eligible_pilots(project_id):

#     pilots = read_sheet("pilot_roster")
#     mission = get_mission(project_id)

#     if mission is None:
#         return "Mission not found."

#     skill = mission["required_skills"]
#     cert = mission["required_certs"]
#     location = mission["location"]

#     pilots = pilots[pilots["status"] == "Available"]
#     pilots = pilots[pilots["location"] == location]

#     pilots = pilots[
#         pilots["skills"].str.contains(skill, case=False)
#     ]

#     pilots = pilots[
#         pilots["certifications"].str.contains(cert, case=False)
#     ]

#     if pilots.empty:
#         return "No eligible pilots found."

#     return pilots


# # -----------------------------
# # Eligible Drones
# # -----------------------------
# def eligible_drones(project_id):

#     drones = read_sheet("drone_fleet")
#     mission = get_mission(project_id)

#     if mission is None:
#         return "Mission not found."

#     skill = mission["required_skills"]
#     location = mission["location"]

#     drones = drones[drones["status"] == "Available"]
#     drones = drones[drones["location"] == location]

#     skill_map = {
#         "Mapping": "RGB",
#         "Inspection": "RGB",
#         "Thermal": "Thermal"
#     }

#     capability = skill_map.get(skill, skill)

#     drones = drones[
#         drones["capabilities"].str.contains(capability, case=False)
#     ]

#     if drones.empty:
#         return "No eligible drones found."

#     return drones


# # -----------------------------
# # Conflict Detection
# # -----------------------------
# def detect_conflicts(project_id, pilot_name, drone_id):

#     pilots = read_sheet("pilot_roster")
#     drones = read_sheet("drone_fleet")

#     conflicts = []

#     pilot_row = pilots[pilots["name"] == pilot_name]
#     drone_row = drones[drones["drone_id"] == drone_id]

#     if pilot_row.iloc[0]["status"] == "Assigned":
#         conflicts.append("Pilot already assigned.")

#     if drone_row.iloc[0]["status"] == "Maintenance":
#         conflicts.append("Drone under maintenance.")

#     return conflicts


# # -----------------------------
# # Assign Resources
# # -----------------------------
# def assign_resources(project_id):

#     if pilot_row.iloc[0]["location"] != mission["location"]:
#         conflicts.append("Pilot location mismatch.")

#     if drone_row.iloc[0]["location"] != mission["location"]:
#         conflicts.append("Drone location mismatch.")

#     if drone_row.iloc[0]["status"] == "Maintenance":
#         conflicts.append("Drone under maintenance.")


#     pilots_df = read_sheet("pilot_roster")

#     already = pilots_df[
#         pilots_df["current_assignment"] == project_id
#     ]

#     if not already.empty:
#         return f"{project_id} already has assigned resources."
#     pilots_df = read_sheet("pilot_roster")
#     drones_df = read_sheet("drone_fleet")

#     eligible_p = eligible_pilots(project_id)
#     eligible_d = eligible_drones(project_id)

#     if isinstance(eligible_p, str):
#         return eligible_p

#     if isinstance(eligible_d, str):
#         return eligible_d

#     pilot_name = eligible_p.iloc[0]["name"]
#     drone_id = eligible_d.iloc[0]["drone_id"]

#     conflicts = detect_conflicts(project_id, pilot_name, drone_id)

#     if conflicts:
#         return "Conflict detected: " + ", ".join(conflicts)

#     pilot_row = pilots_df[pilots_df["name"] == pilot_name].index[0] + 2
#     drone_row = drones_df[drones_df["drone_id"] == drone_id].index[0] + 2

#     update_row("pilot_roster", pilot_row,
#                "current_assignment", project_id)
#     update_row("pilot_roster", pilot_row,
#                "status", "Assigned")

#     update_row("drone_fleet", drone_row,
#                "current_assignment", project_id)
#     update_row("drone_fleet", drone_row,
#                "status", "Assigned")

#     return f"Assigned {pilot_name} and drone {drone_id} to {project_id}"


# # -----------------------------
# # Urgent Reassignment
# # -----------------------------
# def urgent_reassignment(project_id):

#     pilots = read_sheet("pilot_roster")

#     assigned = pilots[
#         pilots["current_assignment"] == project_id
#     ]

#     if assigned.empty:
#         return "No pilot currently assigned."

#     old_row = assigned.index[0] + 2

#     update_row("pilot_roster", old_row,
#                "status", "Unavailable")

#     replacement = eligible_pilots(project_id)

#     if isinstance(replacement, str):
#         return "No replacement pilot available."

#     new_name = replacement.iloc[0]["name"]
#     new_row = replacement.index[0] + 2

#     update_row("pilot_roster", new_row,
#                "current_assignment", project_id)

#     update_row("pilot_roster", new_row,
#                "status", "Assigned")

#     return f"{new_name} reassigned to {project_id}"

# def update_pilot_status(name, status):

#     df = read_sheet("pilot_roster")

#     row = df[df["name"].str.lower() == name.lower()]

#     if row.empty:
#         return "Pilot not found."

#     index = row.index[0] + 2

#     update_row("pilot_roster", index, "status", status)

#     return f"{name} status updated to {status}"


# def update_drone_status(drone_id, status):

#     df = read_sheet("drone_fleet")

#     row = df[df["drone_id"] == drone_id]

#     if row.empty:
#         return "Drone not found."

#     index = row.index[0] + 2

#     update_row("drone_fleet", index, "status", status)

#     return f"{drone_id} status updated to {status}"






from sheets import read_sheet, update_row


# -----------------------------------
# Available Pilots
# -----------------------------------
def available_pilots(location=None):
    df = read_sheet("pilot_roster")

    df = df[df["status"] == "Available"]

    if location:
        df = df[df["location"] == location]

    return df


# -----------------------------------
# Available Drones
# -----------------------------------
def available_drones(location=None):
    df = read_sheet("drone_fleet")

    df = df[df["status"] == "Available"]

    if location:
        df = df[df["location"] == location]

    return df


# -----------------------------------
# Fleet Status
# -----------------------------------
def fleet_status():
    return read_sheet("drone_fleet")


# -----------------------------------
# Mission Fetch
# -----------------------------------
def get_mission(project_id):
    df = read_sheet("missions")

    mission = df[df["project_id"] == project_id]

    if mission.empty:
        return None

    return mission.iloc[0]


# -----------------------------------
# Eligible Pilots
# -----------------------------------
def eligible_pilots(project_id):

    pilots = read_sheet("pilot_roster")
    mission = get_mission(project_id)

    if mission is None:
        return "Mission not found."

    skill = mission["required_skills"]
    cert = mission["required_certs"]
    location = mission["location"]

    pilots = pilots[pilots["status"] == "Available"]
    pilots = pilots[pilots["location"] == location]

    pilots = pilots[
        pilots["skills"].str.contains(skill, case=False)
    ]

    pilots = pilots[
        pilots["certifications"].str.contains(cert, case=False)
    ]

    if pilots.empty:
        return "No eligible pilots found."

    return pilots


# -----------------------------------
# Eligible Drones
# -----------------------------------
def eligible_drones(project_id):

    drones = read_sheet("drone_fleet")
    mission = get_mission(project_id)

    if mission is None:
        return "Mission not found."

    skill = mission["required_skills"]
    location = mission["location"]

    drones = drones[drones["status"] == "Available"]
    drones = drones[drones["location"] == location]

    skill_map = {
        "Mapping": "RGB",
        "Inspection": "RGB",
        "Thermal": "Thermal"
    }

    capability = skill_map.get(skill, skill)

    drones = drones[
        drones["capabilities"].str.contains(capability, case=False)
    ]

    if drones.empty:
        return "No eligible drones found."

    return drones


# -----------------------------------
# Conflict Detection
# -----------------------------------
def detect_conflicts(project_id, pilot_name, drone_id):

    pilots = read_sheet("pilot_roster")
    drones = read_sheet("drone_fleet")
    mission = get_mission(project_id)

    conflicts = []

    pilot_row = pilots[pilots["name"] == pilot_name]
    drone_row = drones[drones["drone_id"] == drone_id]

    if pilot_row.iloc[0]["status"] == "Assigned":
        conflicts.append("Pilot already assigned.")

    if drone_row.iloc[0]["status"] == "Maintenance":
        conflicts.append("Drone under maintenance.")

    if pilot_row.iloc[0]["location"] != mission["location"]:
        conflicts.append("Pilot location mismatch.")

    if drone_row.iloc[0]["location"] != mission["location"]:
        conflicts.append("Drone location mismatch.")

    return conflicts


# -----------------------------------
# Assign Resources
# -----------------------------------
def assign_resources(project_id):

    pilots_df = read_sheet("pilot_roster")

    already = pilots_df[
        pilots_df["current_assignment"] == project_id
    ]

    if not already.empty:
        return f"{project_id} already has assigned resources."

    eligible_p = eligible_pilots(project_id)
    eligible_d = eligible_drones(project_id)

    if isinstance(eligible_p, str):
        return eligible_p

    if isinstance(eligible_d, str):
        return eligible_d

    pilot_name = eligible_p.iloc[0]["name"]
    drone_id = eligible_d.iloc[0]["drone_id"]

    conflicts = detect_conflicts(project_id, pilot_name, drone_id)

    if conflicts:
        return "Conflict detected: " + ", ".join(conflicts)

    pilot_row = pilots_df[pilots_df["name"] == pilot_name].index[0] + 2
    drones_df = read_sheet("drone_fleet")
    drone_row = drones_df[drones_df["drone_id"] == drone_id].index[0] + 2

    update_row("pilot_roster", pilot_row,
               "current_assignment", project_id)
    update_row("pilot_roster", pilot_row,
               "status", "Assigned")

    update_row("drone_fleet", drone_row,
               "current_assignment", project_id)
    update_row("drone_fleet", drone_row,
               "status", "Assigned")

    return f"Assigned {pilot_name} and drone {drone_id} to {project_id}"


# -----------------------------------
# Urgent Reassignment
# -----------------------------------
def urgent_reassignment(project_id):

    pilots = read_sheet("pilot_roster")

    assigned = pilots[
        pilots["current_assignment"] == project_id
    ]

    if assigned.empty:
        return "No pilot currently assigned."

    old_row = assigned.index[0] + 2

    update_row("pilot_roster", old_row,
               "status", "Unavailable")

    replacement = eligible_pilots(project_id)

    if isinstance(replacement, str):
        return "No replacement pilot available."

    new_name = replacement.iloc[0]["name"]
    new_row = replacement.index[0] + 2

    update_row("pilot_roster", new_row,
               "current_assignment", project_id)

    update_row("pilot_roster", new_row,
               "status", "Assigned")

    return f"{new_name} reassigned to {project_id}"


# -----------------------------------
# Update Pilot Status
# -----------------------------------
def update_pilot_status(name, status):

    df = read_sheet("pilot_roster")

    row = df[df["name"].str.lower() == name.lower()]

    if row.empty:
        return "Pilot not found."

    index = row.index[0] + 2

    update_row("pilot_roster", index, "status", status)

    return f"{name} status updated to {status}"


# -----------------------------------
# Update Drone Status
# -----------------------------------
def update_drone_status(drone_id, status):

    df = read_sheet("drone_fleet")

    row = df[df["drone_id"] == drone_id]

    if row.empty:
        return "Drone not found."

    index = row.index[0] + 2

    update_row("drone_fleet", index, "status", status)

    return f"{drone_id} status updated to {status}"

# # import streamlit as st
# # from agent import agent_reply

# # st.title("🚁 Drone Operations AI Agent")

# # if "chat" not in st.session_state:
# #     st.session_state.chat = []

# # user_input = st.text_input("Ask the agent:")

# # if user_input:
# #     response = agent_reply(user_input)

# #     st.session_state.chat.append(("You", user_input))
# #     st.session_state.chat.append(("Agent", response))

# # for speaker, msg in st.session_state.chat:
# #     st.write(f"**{speaker}:** {msg}")

# import streamlit as st

# from langchain_agent import run_agent

# # from agent import agent_reply
# from sheets import read_sheet
# # from streamlit_autorefresh import st_autorefresh
# from langchain_agent import run_agent



# st.title("🚁 Drone Operations AI Agent")
# # st_autorefresh(interval=50000, key="fleetrefresh")

# # Live feed fleet
# st.header("📊 Live Operations Dashboard")

# pilots_df = read_sheet("pilot_roster")
# drones_df = read_sheet("drone_fleet")

# st.subheader("🧑‍✈️ Pilot Roster")
# st.dataframe(pilots_df)

# st.subheader("🚁 Drone Fleet Status")
# st.dataframe(drones_df)



# if "chat" not in st.session_state:
#     st.session_state.chat = []

# user_input = st.text_input("Ask the agent:")

# if user_input:
#     response = run_agent(user_input)
#     st.session_state.chat.append(("You", user_input))
#     st.session_state.chat.append(("Agent", response))

# for speaker, msg in st.session_state.chat:
#     st.write(f"**{speaker}:**")

#     if speaker == "Agent" and msg["type"] == "table":
#         st.dataframe(msg["data"])
#     else:
#         if isinstance(msg, dict):
#             st.write(msg["data"])
#         else:
#             st.write(msg)


import streamlit as st
from streamlit_autorefresh import st_autorefresh

from sheets import read_sheet
from langchain_agent import run_agent


st.set_page_config(layout="wide")

st.title("🚁 Drone Operations AI Agent")

# Auto refresh dashboard every 5 seconds
# st_autorefresh(interval=5000, key="fleetrefresh")

# -------- Dashboard --------
st.header("📊 Live Operations Dashboard")

pilots_df = read_sheet("pilot_roster")
drones_df = read_sheet("drone_fleet")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🧑‍✈️ Pilot Roster")
    st.dataframe(pilots_df)

with col2:
    st.subheader("🚁 Drone Fleet Status")
    st.dataframe(drones_df)


st.divider()

# -------- Chat Agent --------
st.header("💬 Ask the Operations Agent")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("Ask the agent:")

if user_input:
    response = run_agent(user_input)

    st.session_state.chat.append(("You", user_input))
    st.session_state.chat.append(("Agent", response))

for speaker, msg in st.session_state.chat:
    st.write(f"**{speaker}:**")

    if speaker == "Agent" and isinstance(msg, dict):
        if msg["type"] == "table":
            st.dataframe(msg["data"])
        else:
            st.write(msg["data"])
    else:
        st.write(msg)

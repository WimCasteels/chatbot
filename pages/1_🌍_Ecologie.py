import streamlit as st
import json
from google import genai
import os
from google.genai import types

st.markdown("# 🌍Ecologie")

with open('ecologie.json') as json_file:
    inhoud = dict(json.load(json_file))

inhoud_values = list(inhoud.values())

st.write(inhoud_values[0])

# openai_api_key = st.text_input("OpenAI API Key", type="password")
google_key = os.getenv('GOOGLE_API')

# Create a client.
client = genai.Client(api_key = google_key)

if "chat_ecol" not in st.session_state:
    st.session_state.chat_ecol = client.chats.create(model="gemini-2.5-flash",
                      config=types.GenerateContentConfig(
                system_instruction=inhoud_values[0]))

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.chat_ecol.get_history():
    with st.chat_message(message.role):
        st.markdown(message.parts[0].text)

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("..."):

    # Store and display the current prompt.
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    response = st.session_state.chat_ecol.send_message(prompt)
    with st.chat_message("model"): #assistant
        st.markdown(response.text)


st.sidebar.header("🌍Ecologie")

with st.sidebar:
    module = st.radio(
    "**Modules**",
    ["Introductie", "Basisbegrippen", "Milieu-impact"],
    key="modul"
    )

    if "profiel" in st.session_state:
        st.markdown(st.session_state.profiel)




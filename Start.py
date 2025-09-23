import streamlit as st
from openai import OpenAI
from google import genai
import os
from google.genai import types
from openai import OpenAI


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


# Show title and description.
st.title("🌱 Sustainable AI")

with st.sidebar:
    st.text("Jou (leer)profiel:")
    if "profiel" in st.session_state:
        st.markdown(st.session_state.profiel)

# openai_api_key = st.text_input("OpenAI API Key", type="password")
google_key = os.getenv('GOOGLE_API')
OR_key = os.getenv('OPEN_ROUTER_API')


client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=OR_key
)

completion = client.chat.completions.create(
  model="x-ai/grok-4-fast:free",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)
# st.write(completion.choices[0].message.content)

if "messages" not in st.session_state:
    st.session_state.messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

for message in st.session_state.messages:
    if message['role'] != 'system':
      with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="x-ai/grok-4-fast:free",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})


# Create a client.
#client = genai.Client(api_key = google_key)
#if "chat" not in st.session_state:
#    st.session_state.chat = client.chats.create(model="gemini-2.5-flash",
#                      config=types.GenerateContentConfig(
#                system_instruction="""Je bent een vriendelijke chatbot in Vlaanderen die een kort en informeel startgesprek heeft met de gebruiker voordat de gebruiker start met de leermodules over AI.
#                    Pas je wat betreft de taal aan aan de gebruiker. 
#                    Je doel is om snel een beeld te vormen van de gebruiker, zonder dat het voelt als een interview. 
#                    Stuur het gesprek naar:
#                    - Leeftijd en opleidingsniveau (bijv. lager, middelbaar, universitair).
#                    - Taalvaardigheid (moedertaal, voorkeur voor instructietaal).
#                    - Reden om deel te nemen (werkgerelateerd, verplicht voor studie, persoonlijke interesse).
#                    - Digitale geletterdheid (beginner, gemiddeld, gevorderd).
#                    - Voorkeursleerstijl (tekst lezen, video, audio/podcast, interactieve oefeningen).
#                    - Huidige kennisniveau van AI (geen, basis, gemiddeld, gevorderd).
#                    - Ervaring met AI-tools (bijv. ChatGPT, DALL·E, Midjourney, Copilot, AI in MS Office/Google).
#                    - Houding tegenover AI: nieuwsgierig, sceptisch, kritisch, enthousiast.
#                    - Specifieke interesses (Praktisch gebruik, Technisch, Ethisch/juridisch, Toekomst, ...)
#
#                    Hou je reacties kort, vriendelijk en menselijk. 
#                    Vermijd formele testvragen of opsommingen; laat het voelen als een natuurlijk gesprek.
#                    Vraag niet te hard door, ga op tijd over naar een ander onderwerp."""))

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.

# Display the existing chat messages via `st.chat_message`.
#for message in st.session_state.chat.get_history():
#    with st.chat_message(message.role):
#        st.markdown(message.parts[0].text)

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
#if prompt := st.chat_input("..."):

    # Store and display the current prompt.
#    with st.chat_message("user"):
#        st.markdown(prompt)

    # Generate a response using the OpenAI API.
#    response = st.session_state.chat.send_message(prompt)
#    with st.chat_message("model"): #assistant
#        st.markdown(response.text)


client_profile = genai.Client(api_key = google_key)
if st.session_state.messages:
    prompt = f"""Maak op basis van het CHATGESPREK een beknopt profiel aan van de gebruiker. 
    Indien er geen informatie is geef dan onbekend aan.
    Concentreer je op volgende informatie:
    - Leeftijd en opleidingsniveau (bijv. lager, middelbaar, universitair).
    - Taalvaardigheid (moedertaal, voorkeur voor instructietaal).
    - Reden om deel te nemen (werkgerelateerd, verplicht voor studie, persoonlijke interesse).
    - Digitale geletterdheid (beginner, gemiddeld, gevorderd).
    - Voorkeursleerstijl (tekst lezen, video, audio/podcast, interactieve oefeningen).
    - Huidige kennisniveau van AI (geen, basis, gemiddeld, gevorderd).
    - Ervaring met AI-tools (bijv. ChatGPT, DALL·E, Midjourney, Copilot, AI in MS Office/Google).
    - Houding tegenover AI: nieuwsgierig, sceptisch, kritisch, enthousiast.
    - Specifieke interesses (Praktisch gebruik, Technisch, Ethisch/juridisch, Toekomst, ...)

    CHATGESPREK:
    {st.session_state.messages}

    Profiel:
    """
    print(prompt)
    response = client_profile.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    st.session_state.profiel = response.text
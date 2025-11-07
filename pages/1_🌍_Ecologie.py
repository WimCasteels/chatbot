import streamlit as st
import json
import os
# import requests
from openai import OpenAI
# from huggingface_hub import InferenceClient


@st.cache_data
def load_inhoud(path="ecologie.json"):
    with open(path) as f:
        return dict(json.load(f))
    
inhoud = load_inhoud()



st.sidebar.header("👤 Profiel")



with st.sidebar:
    #module = st.radio("",
    #    list(inhoud.keys()),
    #key="modul")

    if "profiel" in st.session_state:
        st.markdown(st.session_state.profiel)



st.markdown("# 🌍Ecologie")

if "profiel" not in st.session_state:
    st.session_state.profiel = ""

if "client" not in st.session_state:
  OR_key = os.getenv('OPEN_ROUTER_API')
  st.session_state.client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OR_key
  )

#if st.button("Afbeelding"):
#    HF_TOKEN = os.environ["HF_TOKEN"]
#    client = InferenceClient(
#      provider="fal-ai",
#      api_key=HF_TOKEN)
#    image = client.text_to_image(
#      "Astronaut riding a horse",
#      model="tencent/HunyuanImage-2.1")
#    st.image(image)

if "progress" not in st.session_state:
    st.session_state.progress = 0


st.write(f"# {list(inhoud.keys())[st.session_state.progress]}")

if st.button("➡️ Volgende ➡️"):
    st.session_state.progress += 1
    st.session_state["modul"] = list(inhoud.keys())[st.session_state.progress]
    st.rerun()


inhoud_values = list(inhoud.values())

# wat als het profiel aangepast wordt???
if "messages_ec" not in st.session_state:
    system_instruction=f"""Je bent een online leercoach die gebruikers begeleidt door een reeks modules over de ecologische voetafdruk van AI.
      Je schrijft in een toegankelijke, motiverende en inspirerende stijl, direct gericht aan de deelnemer (jij/je).        
      Wanneer je inhoud uitlegt:
      - Geef heldere, toegankelijke uitleg in begrijpelijke taal.
      - Vermijd jargon of leg het uit als het nodig is.
      - Gebruik concrete voorbeelden, metaforen of vergelijkingen om begrippen duidelijk te maken.
      - Maak de toon vriendelijk, activerend en uitnodigend.
      - Stimuleer de gebruiker om actief mee te denken en door te klikken naar volgende onderdelen.
      
      Pas de boodschap aan op basis van het PROFIEL van de gebruiker.
      PROFIEL: {st.session_state.profiel}"""

    st.session_state.messages_ec = [{'role': 'system', 'content': system_instruction}]

st.session_state.messages_ec.append({"role": "user", "content": inhoud_values[st.session_state.progress]})

completion = st.session_state.client.chat.completions.create(
  model=st.session_state.model,
  messages=[{"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages_ec
            ],
  stream=True,
)

response = st.write_stream(completion)

st.session_state.messages_ec.append({"role": "assistant", "content": response})

if "messages_ec_chat" not in st.session_state:
    st.session_state.messages_ec_chat = []


# if prompt := st.chat_input("Heb je nog vragen?"):
#     st.session_state.messages_ec_chat.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     system_instruction = f'''Je bent een behulpzame leercoach die gebruikersvragen beantwoord.
#     Je speelt hierbij maximaal in op het PROFIEL van de gebruiker en op de INHOUD van de leermodule die de gebruiker te zien kreeg.
    
#     PROFIEL: {st.session_state.profiel}
    
#     INHOUD: {st.session_state.messages_ec} 
#     '''

#     with st.chat_message("assistant"):
#         stream = st.session_state.client.chat.completions.create(
#             model=st.session_state.model,
#             messages=[{'role': 'system', 'content': system_instruction}] + [
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages_ec_chat
#             ],
#             stream=True,
#         )
#         response = st.write_stream(stream)
#     st.session_state.messages.append({"role": "assistant", "content": response})


# ---------- CHAT: alleen chatbox rerunt ----------



@st.fragment
def chat_fragment():

    st.subheader("Chat met je leercoach")
    # Render eerdere chat

    for m in st.session_state.messages_ec_chat:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Heb je nog vragen?"):
        st.session_state.messages_ec_chat.append({"role":"user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Maak een korte, actuele system prompt
        system_instruction = f"""Je beantwoordt vragen als behulpzame leercoach.
        Gebruik het PROFIEL en de reeds getoonde INHOUD.
        Geef geen links naar externe bronnen.
        Hou je antwoorden bondig en ga enkel in op de vragen die de gebruiker stelt!
        PROFIEL: {st.session_state.profiel}
        INHOUD (beknopt): {st.session_state.messages_ec}"""

        with st.chat_message("assistant"):
            stream = st.session_state.client.chat.completions.create(
                model=st.session_state.model,
                messages=[{'role':'system','content': system_instruction}]
                         + st.session_state.messages_ec_chat,
                stream=True,
            )
            answer = st.write_stream(stream)

        # juiste lijst bijwerken (bugfix t.o.v. jouw code)
        st.session_state.messages_ec_chat.append({"role":"assistant", "content": answer})

        # Alleen dit fragment verversen
        st.rerun(scope="fragment")

with st.container(height = 300):
    chat_fragment()



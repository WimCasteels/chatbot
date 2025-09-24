import streamlit as st
import json
import os
import requests
from openai import OpenAI
from huggingface_hub import InferenceClient

st.sidebar.header("🌍Ecologie")

def radio_action():
    st.session_state.progress = 0


with st.sidebar:
    module = st.radio(
    "**Modules**",
    ["Introductie", "Basisbegrippen", "Milieu-impact"],
    key="modul",
    on_change=radio_action)

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


with open('ecologie.json') as json_file:
    inhoud = dict(json.load(json_file))

st.write(f"# {module} - {list(inhoud.keys())[st.session_state.progress]}")

if st.button("➡️ Volgende ➡️"):
    st.session_state.progress += 1

inhoud_values = list(inhoud.values())

if "messages_ec" not in st.session_state:
    system_instruction=f"""Je bent een online leercoach die een introductie presenteert voor een leermodule over kunstmatige intelligentie (AI) en de ecologische voetafdruk. 
      Je schrijft in een toegankelijke, motiverende en inspirerende stijl, direct gericht aan de deelnemer (‘je/jij’). 
      Gebruik korte alinea’s, opsommingen waar passend, en zorg dat de tekst vlot en begrijpelijk is. 
      Elke sectie moet helder afgebakend zijn met een titel of emoji.
      
      Pas de boodschap aan op basis van het PROFIEL van de gebruiker.
      PROFIEL: {st.session_state.profiel}"""

    st.session_state.messages_ec = [{'role': 'system', 'content': system_instruction}]

prompt = f"""
{inhoud_values[st.session_state.progress]}
"""
st.session_state.messages_ec.append({"role": "user", "content": inhoud_values[st.session_state.progress]})

completion = st.session_state.client.chat.completions.create(
  model="x-ai/grok-4-fast:free",
  messages=[{"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages_ec
            ],
  stream=True,
)

response = st.write_stream(completion)

st.session_state.messages_ec.append({"role": "assistant", "content": response})





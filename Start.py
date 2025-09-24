import streamlit as st
from openai import OpenAI
import os


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)


# Show title and description.
st.title("🌱 Sustainable AI")

#with st.sidebar:
#    if "profiel" in st.session_state:
#        st.markdown(st.session_state.profiel)

if "client" not in st.session_state:
  OR_key = os.getenv('OPEN_ROUTER_API')
  st.session_state.client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OR_key
  )

#completion = client.chat.completions.create(
#  model="x-ai/grok-4-fast:free",
#  messages=[
#    {
#      "role": "user",
#      "content": "What is the meaning of life?"
#    }
#  ]
#)
# st.write(completion.choices[0].message.content)

if "messages" not in st.session_state:
    system_instruction="""Je bent een vriendelijke chatbot in Vlaanderen die een kort en informeel startgesprek heeft met de gebruiker voordat de gebruiker start met de leermodules over AI.
                    Pas je wat betreft de taal aan aan de gebruiker. 
                    Je doel is om snel een beeld te vormen van de gebruiker, zonder dat het voelt als een interview. 
                    Stuur het gesprek naar:
                    - Aanspreking (naam, bijnaam).
                    - Leeftijd en opleidingsniveau (bijv. lager, middelbaar, universitair).
                    - Taalvaardigheid (moedertaal, voorkeur voor instructietaal).
                    - Reden om deel te nemen (werkgerelateerd, verplicht voor studie, persoonlijke interesse).
                    - Digitale geletterdheid (beginner, gemiddeld, gevorderd).
                    - Voorkeursleerstijl (tekst lezen, video, audio/podcast, interactieve oefeningen).
                    - Huidige kennisniveau van AI (geen, basis, gemiddeld, gevorderd).
                    - Ervaring met AI-tools (bijv. ChatGPT, DALL·E, Midjourney, Copilot, AI in MS Office/Google).
                    - Houding tegenover AI: nieuwsgierig, sceptisch, kritisch, enthousiast.
                    - Specifieke interesses (Praktisch gebruik, Technisch, Ethisch/juridisch, Toekomst, ...)

                    Hou je reacties kort, vriendelijk en menselijk. 
                    Vermijd formele testvragen of opsommingen; laat het voelen als een natuurlijk gesprek.
                    Vraag niet te hard door, ga op tijd over naar een ander onderwerp.
                    Wijk niet af van het onderwerp. Keer terug naar het onderwerp als de gebruiker iets ander vraagt of zegt.
                    Presenteer jezelf niet als een mens."""
    

    openingszin = st.session_state.client.chat.completions.create(
            model="x-ai/grok-4-fast:free",
            messages=[{'role': 'system', 'content': system_instruction},
                      {'role': 'user', 'content': "hey"}],
        ).choices[0].message.content

    st.session_state.messages = [{'role': 'system', 'content': system_instruction},
                                 {'role': 'assistant', 'content': openingszin}]


for message in st.session_state.messages:
    if message['role'] != 'system':
      with st.chat_message(message["role"]):
        st.markdown(message["content"])



if prompt := st.chat_input("..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = st.session_state.client.chat.completions.create(
            model="x-ai/grok-4-fast:free",
            messages=[{'role': 'system', 'content': f"Huidig profiel: {st.session_state.profiel}"}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})




if st.session_state.messages:
    prompt = f"""Maak op basis van het CHATGESPREK een beknopt profiel aan van de gebruiker. 
    Indien er geen informatie is geef dan onbekend aan.
    Geef in het profiel de mogelijkheden tussen de haakjes NIET weer.
    Concentreer je op volgende informatie:
    - Aanspreking (naam, bijnaam).
    - Leeftijd en opleidingsniveau (bijv. lager, middelbaar, universitair).
    - Taal (moedertaal, voorkeur voor instructietaal).
    - Reden om deel te nemen (werkgerelateerd, voor studie, persoonlijke interesse).
    - Digitale geletterdheid (beginner, gemiddeld, gevorderd).
    - Voorkeursleerstijl (tekst lezen, video, audio/podcast, interactieve oefeningen).
    - Kennis van AI (geen, basis, gemiddeld, gevorderd).
    - Ervaring met AI-tools (bijv. ChatGPT, DALL·E, Midjourney, Copilot, AI in MS Office/Google).
    - Houding tegenover AI (nieuwsgierig, sceptisch, kritisch, enthousiast).
    - Specifieke interesses (Praktisch gebruik, Technisch, Ethisch/juridisch, Toekomst, ...)

    CHATGESPREK:
    {st.session_state.messages}

    Profiel:
    """
    response = st.session_state.client.chat.completions.create(
        model="x-ai/grok-4-fast:free",
        messages=[
        {
          "role": "user",
          "content": prompt
        }
        ]
    )
    st.session_state.profiel = response.choices[0].message.content

    with st.sidebar:
        st.markdown(st.session_state.profiel)
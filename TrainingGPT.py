import streamlit as st
from IPython.display import Audio
from IPython.core.display import display,clear_output
import requests
import openai
import os
os.system("pip install pyaudio")

import speech_recognition as sr
import time
st.sidebar.title('Lead Type Config')

lead_type = st.sidebar.selectbox(
    'Lead Type',
    ('Interested', 'Not Interested', 'Neutral')
)

behaviour = st.sidebar.selectbox(
    'Behaviour',
    ('Rude', 'Polite', 'Neutral')
)

persona = 'lead type is '+lead_type +' and on call behaviour is '+behaviour
persona_for_gpt = 'your are a '+lead_type +' and your on call behaviour is '+behaviour


def get_audio_2(script):
    headers = {
        'xi-api-key': '54762810afc15fa5d0a035bfc17caab3',
        'accept': 'audio/mpeg',
        'Content-Type': 'application/json',
        "model_id": "eleven_monolingual_v1",
        "accept-language": "en-US,en;q=0.9",

    }

    json_data = {
        'text': script,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 1,
            "model_id": "eleven_monolingual_v1",
        }

    }
    response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL', headers=headers, json=json_data)

    audio_content = response.content
    audio_length = float(response.headers.get('Content-Length', 0)) / 16000  # Assuming sample rate of 16kHz
    prompt_response_speech = "prompt_response.mp3"

    with open(prompt_response_speech, 'wb') as f:
        f.write(audio_content)

    audio = Audio(prompt_response_speech, autoplay=True)
    audio_length= audio_length*2
    return [audio, audio_length,audio_content]


def transcribe_audio(attempts=0):
    try:
        if attempts >= 3:
            st.write("Exceeded maximum number of attempts.")
            return None

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            st.write("Speak now...")
            audio = r.listen(source)
            st.write("Transcribing...")
            text = r.recognize_google(audio)
            st.write("Transcription:", text)
            return text
    except sr.UnknownValueError:
        st.write("Could not understand audio. Please try again.")
        return transcribe_audio(attempts + 1)
    except sr.RequestError:
        st.write("Speech recognition service unavailable. Please try again later.")
        return transcribe_audio(attempts + 1)
    

def should_disconnect_call(last_message):
    x = 'sk-rjTGDJ9FO1Akec2pS352T3Blb'
    y = 'kFJQai8C9IqX4nuZsAJnxmg'
    openai.api_key = x+y
    TEMP_conversation = [
        {
            'role': 'system',
            'content': 'given last msg of a coversation between lead and a tele caller, determin if this call should be disconnect right now or now? ALWAYS ANSER IN True OR False.',
        },
        {
            'role': 'user',
            'content': last_message,
        }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=TEMP_conversation,
        max_tokens=2048,
        temperature=0
    )

    ai_response = response.choices[0].message.content
    st.write(ai_response)
    if ai_response == 'True':
        return True
    else:
        return False
    


def start_call():
    x = 'sk-rjTGDJ9FO1Akec2pS352T3Blb'
    y = 'kFJQai8C9IqX4nuZsAJnxmg'
    openai.api_key = x+y
    conversation = [
        {
            'role': 'system',
            'content': f"""You are a potiental customer. a caller have called you.
{persona_for_gpt}.
    """
        }
    ]
    # first_prompt = transcribe_audio()
    # if first_prompt == None:
    #     return
    # first_prompt = """Good Morning, I'm calling form BAJAJ FINANCE SECURITIES LIMITED, Am i Speaking with Ms. Manisha?"""

    # first_prompt = """नमस्ते सर, मैं बजाज से बोल रही हूँ। क्या मैं आपका कुछ समय ले सकती हूँ?"""
    # first_prompt = """Hello, sir. I'm speaking from Bajaj. Can I take some of your time?"""

    # data = get_audio_2(first_prompt)
    # audio = data[0]
    # wait = data[1]
    # st.write(audio)
    # time.sleep(wait)

    # conversation.append({'role': 'user', 'content': first_prompt})
    conversation.append({'role': 'user', 'content': "hello, I'm a speaking with ms manisha?"})


    while True:
        st.write('generating reponse...')
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation,
            max_tokens=2048,
            temperature=0
        )

        ai_response = response.choices[0].message.content
        st.write(ai_response)

        data = get_audio_2(ai_response)
        audio = data[0]
        wait = data[1]
        st.write(audio)
        time.sleep(wait)

        conversation.append({'role': 'assistant', 'content': ai_response})

        answer = transcribe_audio()
        if answer == None:
            return
        conversation.append({'role': 'assistant', 'content': answer})

        if should_disconnect_call(ai_response):
            st.write('call disconnected')
            return








st.write('Lead Persona: ',persona)
st.button('Start Call',on_click=start_call)

# if "button_clicked" in st.session_state and st.session_state.button_clicked == True:
#     st.session_state.button_clicked = False
#     st.button('End Call')
#     start_call()
# else:
#     st.session_state.button_clicked = True
#     st.button('Start Call')

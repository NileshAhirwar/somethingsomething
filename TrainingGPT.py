import streamlit as st
#from IPython.display import Audio
#from IPython.core.display import display,clear_output
import requests
import openai
import speech_recognition as sr
import time
st.sidebar.title('Lead Type Config')

def transcribe_audio(attempts=0):
    try:
        if attempts >= 3:
            print("Exceeded maximum number of attempts.")
            return None

        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("Speak now...")
            audio = r.listen(source)
            print("Transcribing...")
            text = r.recognize_google(audio)
            print("Transcription:", text)
            return text
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return transcribe_audio(attempts + 1)
    except sr.RequestError:
        print("Speech recognition service unavailable. Please try again later.")
        return transcribe_audio(attempts + 1)


# display(get_audio_2('hello, am i speaking with Ajay')[0])

# Add a selectbox to the sidebar for Lead Status
lead_status = st.sidebar.selectbox(
    'Lead Status',
    ('Interested', 'Not Interested', 'Neutral')
)

# Add a slider to the sidebar for Lead Status value
lead_status_value = st.sidebar.slider('Lead Status', 0, 100, 100)

# Add a selectbox to the sidebar for Behaviour
behaviour = st.sidebar.selectbox(
    'Behaviour',
    ('Rude', 'Polite', 'Neutral')
)

# Add a slider to the sidebar for Behaviour value
behaviour_value = st.sidebar.slider('Behaviour', 0, 100, 100)

# Determine the persona based on inputs and slider values
if lead_status == 'Interested' and behaviour == 'Polite' and lead_status_value >= 50 and behaviour_value >= 50:
    persona = 'Friendly and Engaged'
elif lead_status == 'Not Interested' and behaviour == 'Rude' and lead_status_value >= 50 and behaviour_value >= 50:
    persona = 'Uninterested and Dismissive'
else:
    persona = 'Neutral'
import random

# Generate a random number between 1000 and 10000000
random_number = random.randint(1000, 10000000)

# Print the random number

# Display the persona
st.write("Lead's overall person type: " + persona)
st.write(random_number)
# st.write("You said:\n"+transcribe_audio())

st.snow()

with st.spinner('Wait for it...'):
    time.sleep(5)
st.success('Done!')
st.balloons()

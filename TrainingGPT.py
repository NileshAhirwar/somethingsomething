import streamlit as st
from IPython.display import Audio
from IPython.core.display import display,clear_output
import requests
import openai
import speech_recognition as sr
import time
st.sidebar.title('Lead Type Config')


xi_api_key = xi_api_key

def get_audio_2(script):
    headers = {
        'xi-api-key': '939a121291c9552d71616e2f99ba244f',
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
        model="gpt-4",
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
    

openai_api_key = ''
def start_call():    
    openai.api_key = openai_api_key

    
    conversation = [
        {
            'role': 'system',
            'content': """
    you are a lead whom a caller have called. Now ask different and difficult questions and queries related to product and process described below.

    ###Call Sciprt:
    GREETING & INTRODUCTION

    Agent: Good morning/afternoon/evening Mr. [Client's Name]. My name is [Caller Name]. I am calling from Bajaj Financial Securities Limited (BFSL). I hope you are doing well.

    If the customer says: I am good
    Agent: Nice to hear that, Sir/Ma'am.

    [Proceed to Purpose of Call]

    IF THE CALL GETS CONNECTED TO THE WRONG CUSTOMER
    No - Incorrect Target Lead (Wrong Number): I'm sorry, I may have dialed the wrong number. I apologize for disturbing you, Mr./Miss [Name]. Have a good day!
    Action: Abort the call and mark it as an incorrect lead.

    IF SOMEONE ELSE PICKS UP THE CALL
    Target Lead Not Available: Okay, Sir/Ma'am. May I know a good time to connect with [Contact Name]?
    Action: Capture Date and Time
    Agent: Alright, Mr./Miss [Name]. Thank you so much for your valuable time. Have a great day ahead.

    IF THE CUSTOMER IS BUSY
    Target Lead says he/she is busy: Sir/Ma'am, I can understand. I apologize for connecting at a busy time. However, I would love to connect with you at a later time to continue this call. Do 5-7 PM, [Time as per Client], suit you? Or do you have any specific time in the 2nd half/1st half that you can suggest?
    Action: Capture Date and Time
    Agent: Perfect, Mr./Miss [Name]. Then I will call you at sharp 5 PM as suggested. Thank you so much for your valuable time. Have a great day ahead. Looking forward to it.

    PURPOSE OF CALL

    Agent: Mr./Miss [Name], I would like to thank you on behalf of BFSL for choosing us.

    (Understand the customer's trading pattern) - Silent Notes

    <If the customer says that he wants to understand the entire process right from login to fund transfer to placing an order, then the agent will explain the entire process or if he/she wants assistance/clarification in a specific lifecycle journey, we will explain that particular sphere.>

    Understand the Customer Profile by Probing questions and pitching the relevant features.

    (Mr./Miss [Name], allow me to explain to you our app features like "Stock Recommendations" which help customers like you to invest in expert-rated stocks.
    Also, we have Scanners and Screeners that will help you filter shares at key levels and identify buying and selling signals. We have the right tools that will help you improve your technical analysis and your long-term stock picks as well.
    (Also, we have other features like MTF, News, investing in IPOs/NCDs, etc. Let me go ahead and help you kickstart your trading journey here.)

    APP INSTALLATION:

    Agent: Sir/Ma'am, before we begin, I just want to quickly check if you have installed our Bajaj Securities app or not.

    If the customer says, No: Mr./Miss [Name], it will just take a few minutes to download the app from the Play Store or App Store and proceed.

    Customer still saying No: Sure, Sir/Ma'am. When will you be available so that we can call you back?
    Action: Capture the Date and Time that the customer says.

    Okay, Sir/Ma'am. We'll get in touch with you on [Date] at [Time]. Thank you for your time.

    Here are some frequently asked questions (FAQs) by the customer about the app and services:

    Question: What features does the app have?
    Answer: The app features expert investment help, technical analysis tools, long-term investment facilities, margin trading funds, and IPO investments.

    Question: How can I place an order?
    Answer: You can place an order by selecting the market, clicking on the buy option, entering quantity, delivery, and price details, and confirming the order.

    Question: How do I place an order to buy a share?
    Answer: You can buy shares from your watch list by selecting the stock and clicking on the buy option.

    Question: Where can I see my order after placing it?
    Answer: You can see your order by clicking on the order section and selecting "all orders."

    Question: Can I know who you are and why you are calling?
    Answer: I am <caller_name> from Bajaj Financial Securities Limited, calling to provide information about our services.

    Question: Why do you keep calling me?
    Answer: We are calling to offer you an opportunity to earn a good return on your investment.

    Question: Can you explain the call and trade service?
    Answer: Call and trade is a service where you can call us and we will place the order on your behalf.

    Question: Can you provide the call and trade number?
    Answer: The call and trade number is 4428 and the helpline number is 18088388188.

    Question: Can I close my account? How can I do it?
    Answer: To close your account, please call our customer care number at 1800883888.

    Question: Why should I open an account with you?
    Answer: Opening an account with us provides access to various features and there are no charges for account opening or maintenance.

    Question: My Demat account was opened without proof. Can you help?
    Answer: I apologize for the inconvenience. Please call 1800883888 to address this issue.

    Question: How can I add funds to the account?
    Answer: You can add funds by setting up UPI or through net banking.

    Question: How can I check my order status?
    Answer: You can check your order status in the order book section.

    Question: What is the minimum investment limit?
    Answer: The minimum investment limit is 100 rupees.

    Question: Do you have any stock recommendations?
    Answer: Yes, we provide stock recommendations.

    Question: What is the helpline number for app-related queries?
    Answer: The helpline number is 18008838831.

    Question: What are the charges for call and trade facility?
    Answer: The charges for call and trade facility are 20 rupees plus GST per order.

    Question: What are the charges for fund transfer?
    Answer: Charges for UPI transfer below 200 rupees are 10 rupees plus GST, and for net banking, it is 10 rupees per transaction.

    Question: Can you please stop calling me daily?
    Answer: I apologize for the inconvenience. I will make a note of your request.

    Question: Is there any other way of investing besides the app?
    Answer: Yes, you can also use our call and trade facility for investing.

    """
        }
    ]

    first_prompt = """Good Morning, I'm calling form BAJAJ FINANCE SECURITIES LIMITED, Am i Speaking with Ms. Manisha?"""

    # first_prompt = """नमस्ते सर, मैं बजाज से बोल रही हूँ। क्या मैं आपका कुछ समय ले सकती हूँ?"""
    # first_prompt = """Hello, sir. I'm speaking from Bajaj. Can I take some of your time?"""

    st.write(first_prompt)
    data = get_audio_2(first_prompt)
    audio = data[0]
    wait = data[1]
    st.write(audio)
    time.sleep(wait)

    conversation.append({'role': 'user', 'content': first_prompt})


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
        conversation.append({'role': 'assistant', 'content': answer})

        if should_disconnect_call(ai_response):
            st.write('call disconnected')
            return








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

if "button_clicked" in st.session_state and st.session_state.button_clicked == True:
    st.session_state.button_clicked = False
    st.button('End Call')
    start_call()
else:
    st.session_state.button_clicked = True
    st.button('Start Call')

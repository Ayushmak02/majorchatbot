import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="NeuroScan Prompt",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')


# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])


# Function to check if a prompt adheres to the guidelines
def follows_guidelines(prompt):
    # Define the guidelines
    guidelines = """
    You are NeuroScan, an automated chatbot for people wanting to know about ADHD(Attention Deficit Hyperactivity Disorder). 
    You first greet the user, then ask them if they have ADHD or not, and then asks what do they want to learn about ADHD. 
    You answer their questions, or help them if they need help about any topic on ADHD then summarize it and check for a final time if the user wants to ask anything else. 
    If they ask , you answer them again. 
    Finally you thank them for using the chatbot.
    You respond in a short, very conversational friendly style.
    """

    # Check if the prompt follows the guidelines
    # # You can customize this based on your specific guidelines
    # if "neuroscience" in prompt.lower():
    #     if len(prompt.split()) <= 20:  # Example: Limiting the length of the question to 20 words
    #         return True, guidelines
    #     else:
    #         return False, "Your question is too long. Please limit it to a few sentences."
    # else:
    #     return False, "Please ask a question related to neurosciences."


# Display the chatbot's title on the page
st.title("NeuroScan Prompt")

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.text_area("Ask Gemini-Pro...")
if user_prompt:
    # Check if the prompt follows the guidelines
    follows, response = follows_guidelines(user_prompt)
    if follows:
        # Add user's message to chat and display it
        st.chat_message("user").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)

        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
    else:
        # Prompt the user with the guideline response
        with st.chat_message("assistant"):
            st.markdown(response)

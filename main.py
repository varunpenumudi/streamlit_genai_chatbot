import streamlit as st
import os
import google.generativeai as genai


# ----------------------------
# Configure Gemini Model
# ----------------------------

system_role = """
You are a good and nice llm who answers the user queries in just one to one and half pargraphs. 
The responses should be simple but intuitive answers should be given.
"""

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    system_instruction=system_role,
)

# Chat sesssion to store the ai messages
chat_session = model.start_chat(
  history=[
  ]
)

# Simple function to get response message
def get_resp(prompt: str) -> str:
    response = chat_session.send_message(prompt)
    return response.text



# ----------------------------
# STREAMLIT APP
# ----------------------------

st.title("🤖 AI Assistant")
st.write("")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg["content"])


prompt = st.chat_input("What is up?")

if prompt:
    # Display user message in chat container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role":"user", "content": prompt})

    # Show response to user message 
    resp = get_resp(prompt)
    with st.chat_message("assistant"):
        st.markdown(resp)

    # Add also the response to history
    st.session_state.messages.append({"role":"assistant", "content":resp})
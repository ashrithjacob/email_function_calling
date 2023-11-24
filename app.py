import streamlit as st
import pandas as pd
import json
from io import StringIO
from email_sender import chat_completion_request, TOOLS, tool_exception


def get_email_ids(uploaded_file):
    # To convert to a string based IO:
    decoded_str = uploaded_file.getvalue().decode("utf-8")
    # Split the string into lines and filter out any empty strings
    email_ids = [email for email in decoded_str.split("\n") if email]
    return email_ids


uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    email_ids = get_email_ids(uploaded_file)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    chat_response = chat_completion_request(st.session_state.messages, tools=TOOLS)
    # assistant_message = chat_response.json()["choices"][0]["message"]
    assistant_message = chat_response.json()["choices"][0]["message"]
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_message["content"])
    # Add assistant response to chat history
    st.session_state.messages.append(assistant_message)
    st.markdown(assistant_message)

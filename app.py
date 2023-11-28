import streamlit as st
import pandas as pd
import json
from io import StringIO
import smtplib
from email.mime.text import MIMEText
from email_sender import chat_completion_request, TOOLS


SENDER = "autoemail.ai@gmail.com"
PASSWORD = "lmsr xffu bzbh ynea"
CLIENT_ACCOUNT = st.text_input(
    "client account", "Enter email id to which response is to be directed"
)


def get_email_ids(uploaded_file):
    # To convert to a string based IO:
    decoded_str = uploaded_file.getvalue().decode("utf-8")
    # Split the string into lines and filter out any empty strings
    email_ids = [email for email in decoded_str.split("\n") if email]
    return email_ids


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


def tool_exception(assistant_message):
    if "tool_calls" not in assistant_message.keys():
        st.session_state.messages.append(assistant_message)
        st.session_state.email["tool_use"] = False
    else:
        print(assistant_message["tool_calls"][0]["function"]["arguments"])
        assistant_message = json.loads(
            assistant_message["tool_calls"][0]["function"]["arguments"], strict=False
        )
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_message["content"]}
        )
        st.session_state.email["tool_use"] = True
        st.session_state.email["subject"] = assistant_message["subject"]
        st.session_state.email["content"] = assistant_message["content"]
    return assistant_message


uploaded_file = st.file_uploader("Choose a text file('.txt' extension with all target email id's on a new line)")

if uploaded_file is not None:
    EMAIL_IDS = get_email_ids(uploaded_file)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {
            "role": "system",
            "content": """You are an email sender.
        Don't make assumptions about what values to plug into functions.
        Ask before adding any specific details into the email only then populate the field.
        Always use the fucntion calling tool when drafting the email.""",
        }
    )

if "email" not in st.session_state:
    st.session_state.email = {}

# Display chat messages from history on app rerun
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Chat here"):
    # User input
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # calling chat completion
    chat_response = chat_completion_request(
        st.session_state.messages, tools=TOOLS, tool_choice="auto"
    )
    assistant_message = chat_response.json()["choices"][0]["message"]
    assistant_message = tool_exception(assistant_message)

    # Display text box else chat with user
    if st.session_state.email["tool_use"]:
        st.markdown("Edit the Email below:")
        st.session_state.email["subject"] = st.text_input(
            "Subject", f'DO NOT REPLY: {st.session_state.email["subject"]}'
        )
        st.session_state.email["body"] = st.text_area(
            "Body", f'{st.session_state.email["content"]} \n\nTO RESPOND SEND AN EMAIL TO:{CLIENT_ACCOUNT}'
        )
    else:
        with st.chat_message("assistant"):
            st.markdown(assistant_message["content"])

# send email
if st.button("Send email"):
    if "subject" in st.session_state.email.keys():
        send_email(
            st.session_state.email["subject"],
            st.session_state.email["content"],
            SENDER,
            EMAIL_IDS,
            PASSWORD,
        )

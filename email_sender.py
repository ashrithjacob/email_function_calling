import json
import openai
import requests
import ast
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
import smtplib
from email.mime.text import MIMEText

GPT_MODEL = "gpt-4"


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, temperature=0, tool_choice= None, model=GPT_MODEL):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + openai.api_key,
    }
    json_data = {"model": model, "messages": messages}
    if tools is not None:
        json_data.update({"tools": tools})
    if tool_choice is not None:
        json_data.update({"tool_choice": tool_choice})
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=json_data,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e


def pretty_print_conversation(messages):
    role_to_color = {
        "system": "red",
        "user": "green",
        "assistant": "blue",
        "tool": "magenta",
    }

    for message in messages:
        if message["role"] == "system":
            print(
                colored(
                    f"system: {message['content']}\n", role_to_color[message["role"]]
                )
            )
        elif message["role"] == "user":
            print(
                colored(f"user: {message['content']}\n", role_to_color[message["role"]])
            )
        elif message["role"] == "assistant" and message.get("function_call"):
            print(
                colored(
                    f"assistant: {message['function_call']}\n",
                    role_to_color[message["role"]],
                )
            )
        elif message["role"] == "assistant" and not message.get("function_call"):
            print(
                colored(
                    f"assistant: {message['content']}\n", role_to_color[message["role"]]
                )
            )
        elif message["role"] == "tool":
            print(
                colored(
                    f"function ({message['name']}): {message['content']}\n",
                    role_to_color[message["role"]],
                )
            )

def tool_exception(assistant_message):
    if "tool_calls" not in assistant_message.keys():
        print("No fn call")
        messages.append(assistant_message)
    else:
        assistant_message = json.loads(assistant_message["tool_calls"][0]["function"]["arguments"])
        print("Using fn call")
        messages.append({"role": "assistant",
                         "content": assistant_message["content"]})
    return assistant_message

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_email_contents",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Subject title of the email.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Contents of the email.",
                    },
                },
                "required": ["subject", "content"],
            },
        },
    }
]

messages = []
messages.append(
    {
        "role": "system",
        "content": """You are an email sender.
        Don't make assumptions about what values to plug into functions.
        Ask before adding any specific details into the email only then populate the field.
        Always use the fucntion calling tool when drafting the email.""",
    }
)
print("type 'end' to exit convo")
user_input = ""
while user_input != "end":
    user_input = input("User:")
    if user_input == "end":
        break
    messages.append(
        {
        "role": "user",
        "content": user_input,
        }
    )
    chat_response = chat_completion_request(messages, tools= TOOLS, tool_choice="auto")
    assistant_message = chat_response.json()["choices"][0]["message"]
    assistant_message  =tool_exception(assistant_message)
    print(f'Assistant:{assistant_message["content"]}')


"""
args =json.loads(assistant_message["tool_calls"][0]["function"]["arguments"])
print(args)
subject = args["subject"]
body = args["content"]
sender = "ashrithjacob@gmail.com"
recipients = ["ashrithjacob2@gmail.com", "ashrithjacob@gmail.com"]
password = "voxp nkuk mhns ibtr"

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


send_email(subject, body, sender, recipients, password)
"""
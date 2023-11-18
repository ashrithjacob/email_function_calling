import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored

GPT_MODEL = "gpt-3.5-turbo"


@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
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


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_email_contents",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {
                        "type": "string",
                        "description": "The recepient of the email",
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject of the email.",
                    },
                    "content": {
                        "type": "string",
                        "description": "Contents of the email.",
                    },
                },
                "required": ["recipient", "content"],
            },
        },
    }
]

messages = []
messages.append(
    {
        "role": "system",
        "content": "You are an email sender. Don't make assumptions about what values to plug into functions. Ask before adding any specific details into the email only then populate the field.",
    }
)
messages.append(
    {
        "role": "user",
        "content": "send an email to ashrithjacob@gmail.com regarding pending fees to be paid to AWS.",
    }
)
chat_response = chat_completion_request(messages, tools=tools)
assistant_message = chat_response.json()["choices"][0]["message"]
messages.append(assistant_message)
args =json.loads(assistant_message["tool_calls"][0]["function"]["arguments"])
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage


msg = EmailMessage()
body = args["content"]
msg.set_content(body)
msg["Subject"] = args["subject"]
msg["From"] = "ashrithjacob2@gmail.com"
msg["To"] = args["recipient"]

# Send the message via our own SMTP server.
s = smtplib.SMTP("localhost")
s.send_message(msg)
s.quit()


a = {
    "role": "assistant",
    "content": None,
    "tool_calls": [
        {
            "id": "call_x675zfwqb4G35vK3Ll0hNRuW",
            "type": "function",
            "function": {
                "name": "get_email_contents",
                "arguments": '{\n  "recipient": "ashrithjacob@gmail.com",\n  "subject": "Pending fees payment for AWS",\n  "content": "Hello, \\n\\nI hope this email finds you well. I wanted to inform you that there are pending fees to be paid for the AWS services that we have been using. Could you please check the outstanding balance on your AWS account and make the necessary payment as soon as possible? \\n\\nThank you for your attention to this matter. If you have any questions or need assistance, please feel free to reach out to me. \\n\\nBest regards, \\n[Your Name]"\n}',
            },
        }
    ],
}

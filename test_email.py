import smtplib
from email.mime.text import MIMEText

subject = "Email Subject"
body = "This is the body of the text message"
sender = "ashrithjacob@gmail.com"
recipients = ["ashrithjacob2@gmail.com", "ashrithjacob@gmail.com"]
password = "voxp nkuk mhns ibtr"


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


send_email(subject, body, sender, recipients, password)

{
    "id": "chatcmpl-8OM5gapnnJzBTVYwNWZN4Xs78bjtC",
    "object": "chat.completion",
    "created": 1700815480,
    "model": "gpt-3.5-turbo-0613",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Subject: Reminder: Pending Fees to be Paid to AWS\n\nDear [recipient's name],\n\nI hope this email finds you well. \n\nI am writing to remind you about the pending fees that need to be paid to AWS. As per our records, there are outstanding payments for the following services:\n\n1. [Service 1]: Amount - $[amount]\n2. [Service 2]: Amount - $[amount]\n3. [Service 3]: Amount - $[amount]\n\nIt is important to settle these dues at the earliest to avoid any interruption in your AWS services. Please find attached the detailed invoice for your reference.\n\nTo make the payment, you can log in to your AWS account and follow the instructions provided there. If you have any questions or require assistance, feel free to reach out to our AWS support team at [contact details].\n\nWe highly appreciate your prompt attention to this matter and cooperation in settling the outstanding fees. Your continued usage of AWS services is important to us, and we are here to assist you in any way we can.\n\nThank you for being a valued customer of AWS.\n\nKind regards,\n\n[Your Name]\n[Your Position]\n[Your Company]",
                "tool_calls": [
                    {
                        "id": "call_VNUbS9jSpuxofRCXCjFyK4aN",
                        "type": "function",
                        "function": {
                            "name": "get_email_contents",
                            "arguments": '{\n  "subject": "Pending Fees Reminder - AWS",\n  "content": "Dear [recipient\'s name],\\n\\nI hope this email finds you well.\\n\\nI am writing to remind you about the pending fees that need to be paid to AWS. As per our records, there are outstanding payments for the following services:\\n\\n1. [Service 1]: Amount - $[amount]\\n2. [Service 2]: Amount - $[amount]\\n3. [Service 3]: Amount - $[amount]\\n\\nIt is important to settle these dues at the earliest to avoid any interruption in your AWS services. Please find attached the detailed invoice for your reference.\\n\\nTo make the payment, you can log in to your AWS account and follow the instructions provided there. If you have any questions or require assistance, feel free to reach out to our AWS support team at [contact details].\\n\\nWe highly appreciate your prompt attention to this matter and cooperation in settling the outstanding fees. Your continued usage of AWS services is important to us, and we are here to assist you in any way we can.\\n\\nThank you for being a valued customer of AWS.\\n\\nKind regards,\\n\\n[Your Name]\\n[Your Position]\\n[Your Company]"\n}',
                        },
                    }
                ],
            },
            "finish_reason": "tool_calls",
        }
    ],
    "usage": {"prompt_tokens": 106, "completion_tokens": 511, "total_tokens": 617},
}

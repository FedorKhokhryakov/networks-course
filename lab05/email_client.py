import ssl
import sys
import smtplib
import socket
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

SENDER_EMAIL = "fekhokh@gmail.com"
PASSWORD = ".... .... .... ...." #здесь был мой пароль для 2FA

def send_email_lib(to_email, subject, text_body, html_body=None):
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(text_body, "plain"))

    if html_body:
        msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, PASSWORD)
        server.send_message(msg)


SMTP_SOCKET_SERVER = "smtp.gmail.com"
SMTP_SOCKET_PORT = 587

def _recv(sock):
    return sock.recv(1024).decode()


def _send(sock, cmd):
    print(">>", cmd.strip())
    sock.send((cmd + "\r\n").encode())
    print("<<", _recv(sock))


def send_email_socket(from_addr, to_addr, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SMTP_SOCKET_SERVER, SMTP_SOCKET_PORT))

    print(_recv(sock))

    _send(sock, "EHLO localhost")
    _send(sock, "STARTTLS")

    context = ssl.create_default_context()
    sock = context.wrap_socket(sock, server_hostname=SMTP_SOCKET_SERVER)

    _send(sock, "EHLO localhost")
    _send(sock, "AUTH LOGIN")
    _send(sock, base64.b64encode(SENDER_EMAIL.encode()).decode())
    _send(sock, base64.b64encode(PASSWORD.encode()).decode())

    _send(sock, f"MAIL FROM:<{from_addr}>")
    _send(sock, f"RCPT TO:<{to_addr}>")
    _send(sock, "DATA")

    sock.send((message + "\r\n.\r\n").encode())
    print(_recv(sock))

    _send(sock, "QUIT")
    sock.close()


def create_image_message(from_addr, to_addr, filename):
    with open(filename, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    boundary = "BOUNDARY123"

    msg = f"""From: {from_addr}
To: {to_addr}
Subject: Image test
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary={boundary}

--{boundary}
Content-Type: text/plain

Here is an image

--{boundary}
Content-Type: image/jpeg
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="{filename}"

{encoded}
--{boundary}--
"""

    return msg

if __name__ == "__main__":
    if sys.argv.__len__() < 2:
        print("Usage: python email_client.py <to_addr> [<filename>]")
        sys.exit(1)
    to_email = sys.argv[1]

    if sys.argv.__len__() > 2:
        file = sys.argv[2]

    print("1 - library")
    print("2 - socket")
    print("3 - socket with image")

    choice = input("Choose: ")

    if choice == "1":
        send_email_lib(
            to_email,
            "Test",
            "Hello text",
            "<h1>Hello HTML</h1>"
        )

    elif choice == "2":
        msg = f"From: {SENDER_EMAIL} \nTo: {to_email} \nSubject: Test SMTP \n\nHello from raw SMTP!"
        send_email_socket(SENDER_EMAIL, to_email, msg)

    elif choice == "3":
        msg = create_image_message(
            SENDER_EMAIL,
            to_email,
            file
        )
        send_email_socket(SENDER_EMAIL, to_email, msg)
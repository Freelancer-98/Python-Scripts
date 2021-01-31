import jinja2
import itertools
import operator
import smtplib, ssl
import env.email_config as email_config
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def create_pocket_template(stats):
    templateLoader = jinja2.FileSystemLoader(searchpath="./transform")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "pocket_template.html"
    template = templateEnv.get_template(TEMPLATE_FILE)

    number_articles_read = len(stats)
    minutes_read = list(itertools.accumulate(map(lambda x: x[2], stats), operator.add))[-1]
    total_annotations = list(itertools.accumulate(map(lambda x: len(x[4]), stats), operator.add))[-1]
    outputText = template.render(number_articles_read=number_articles_read, 
                                total_annotations=total_annotations, 
                                minutes_read=minutes_read, stats=stats)
    return outputText

def send_pocket_notification(subject, template):
    port = 465  # For SSL
    password = email_config.password
    sender_email = email_config.sender
    receiver_email = email_config.receiver

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    # Turn these into plain/html MIMEText objects
    html = MIMEText(template, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(html)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


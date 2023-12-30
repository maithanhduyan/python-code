import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from datetime import datetime

def read_template(template_path):
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()
    return template_content

def send_email(subject, html_body, status_message, to_address, smtp_server, smtp_port, smtp_username, smtp_password):
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = ", ".join(to_address)
    message['Subject'] = subject

    # Gán nội dung HTML từ file template
    template_path = 'mail_template.html'
    html_template = read_template(template_path)
    html_body = html_template.format(backup_date=datetime.now(), status_message=status_message)

    # Tạo phần HTML của email
    html_part = MIMEText(html_body, 'html')
    message.attach(html_part)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, to_address, message.as_string())
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
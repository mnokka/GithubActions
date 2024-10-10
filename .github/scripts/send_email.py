import os
import msal
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get credentials and email details from environment variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
tenant_id = os.getenv('TENANT_ID')
from_email = os.getenv('FROM_EMAIL')
to_email = os.getenv('TO_EMAIL')

authority_url = f'https://login.microsoftonline.com/{tenant_id}/'
scope = ['https://graph.microsoft.com/.default']

# SMTP settings
smtp_host = 'smtp.office365.com'
smtp_port = 587

# Get OAuth2 token
def get_oauth2_token():
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority_url,
        client_credential=client_secret,
    )

    result = app.acquire_token_for_client(scopes=scope)
    if 'access_token' in result:
        return result['access_token']
    else:
        raise Exception("Failed to acquire token")

# Send email
def send_email(subject, body):
    token = get_oauth2_token()

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(from_email, token)
        server.sendmail(from_email, to_email, msg.as_string())

# Example usage
send_email('Test Email', 'This is  a test email sent from GitHub Actions using Python.')

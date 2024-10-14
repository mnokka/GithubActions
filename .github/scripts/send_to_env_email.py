import requests
import os

# Function to acquire the OAuth2 token
def get_access_token(tenant_id, client_id, client_secret, scope):
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': scope,
    }

    token_r = requests.post(token_url, data=token_data)
    token = token_r.json().get('access_token')

    if token:
        print("Access token acquired!")
        return token
    else:
        print("Error acquiring access token:", token_r.text)
        return None

# Function to send the email using Microsoft Graph API
def send_email(access_token, from_email, to_email, subject, body):
    endpoint = f"https://graph.microsoft.com/v1.0/users/{from_email}/sendMail"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": to_email
                    }
                }
            ]
        }
    }

    response = requests.post(endpoint, headers=headers, json=email_data)

    if response.status_code == 202:
        print("Email sent successfully!")
    else:
        print("Error sending email:", response.status_code, response.text)

# Use environment variables for sensitive values
tenant_id = os.getenv('TENANT_ID')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
from_email = os.getenv('FROM_EMAIL')

# Assume this email is discovered from the last commit
to_email = os.getenv('PR_AUTHOR_EMAIL')  # Set this from the commit email discovery
scope = 'https://graph.microsoft.com/.default'
subject = "Build Status Update for Your PR"
body = "Hello,\n\nThe build for your PR has completed. Please check the results.\n\nBest,\nYour CI System"

# Get the access token
access_token = get_access_token(tenant_id, client_id, client_secret, scope)

# Send the email if the token was acquired successfully
if access_token and to_email:
    send_email(access_token, from_email, to_email, subject, body)
else:
    print("Access token could not be acquired or email address is missing.")

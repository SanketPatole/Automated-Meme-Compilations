import datetime
import os
from googleapiclient.http import MediaFileUpload
import googleapiclient.errors
from googleapiclient.discovery import build #pip install google-api-python-client
from google_auth_oauthlib.flow import InstalledAppFlow #pip install google-auth-oauthlib
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

TOKEN_NAME = "token.json"

# Setup Google
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
client_secrets_file = "googleAPI.json"

# Handle GoogleAPI oauthStuff
print("Handling GoogleAPI")
creds = None
# The file token1.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists(TOKEN_NAME):
    creds = Credentials.from_authorized_user_file(TOKEN_NAME, SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, SCOPES)
        creds = flow.run_console()
    # Save the credentials for the next run
    with open(TOKEN_NAME, 'w') as token:
        token.write(creds.to_json())

googleAPI = build('youtube', 'v3', credentials=creds)

print("Token generated!")

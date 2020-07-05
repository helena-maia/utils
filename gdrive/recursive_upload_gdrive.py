from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaFileUpload
import os
import glob
import argparse

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
mimetype_dict = {
                "txt": "text/plain",
                "json": "application/json",
                "tar": "application/x-tar"
                }

def init(credentials_path):
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    cred_full_path = os.path.join(credentials_path, "credentials.json")
    token_full_path = os.path.join(credentials_path, "token.pickle")

    if os.path.exists(token_full_path):
        with open(token_full_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_full_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_full_path, 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    return service

def createFolder(folder_name, parent_id):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents':[parent_id]
    }

    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    
    return file.get('id')

def upload_file(file_path, parent_id, mimetype):
    file_name = os.path.basename(file_path)
    ext = file_name.split(".")[-1].lower()
    mimetype = mimetype_dict.get(ext, None)

    if mimetype:
        file_metadata = {'name': file_name, 
                         'parents':[parent_id]}
        media = MediaFileUpload(file_path, mimetype=mimetype)
        file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()

        return file.get('id')
    return None

def sweep(root, parent_id):
    content_list = glob.glob(os.path.join(root,"*"))

    for c in content_list:
        if os.path.isdir(c):
            print(c)
            folder_name = os.path.basename(c)
            new_parent = createFolder(folder_name, parent_id)
            sweep(c, new_parent)
        elif os.path.isfile(c):
            id = upload_file(c, parent_id, "application/pdf")


def main():
    parser = argparse.ArgumentParser(description='Recursive upload on google drive')
    parser.add_argument('root', metavar='DIR', help='path to root')
    parser.add_argument('parent_id', metavar='ID', help='google drive folder id')
    parser.add_argument('credentials_path', metavar='ID', help='Path to credentials.json and to save token.pickle')
    args = parser.parse_args()

    root = args.root
    parent_id = args.parent_id
    credentials_path = args.credentials_path

    global service
    service = init(credentials_path)
    if root[-1] == "/": root = root[:-1]
    folder_name = os.path.basename(root)
    parent_id = createFolder(folder_name, parent_id)
    sweep(root, parent_id)

    

if __name__ == '__main__':
    main()
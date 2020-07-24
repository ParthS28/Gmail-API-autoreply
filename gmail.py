from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from urllib.error import HTTPError
from email.mime.text import MIMEText
import base64



def getMessage(service, user_id, msg_id):    
	try:
		message = service.users().messages().get(userId = user_id, id = msg_id).execute()
		print ('Message snippet: {}'.format(message['snippet']))
		service.users().messages().modify(userId = user_id, id = msg_id, body = {'removeLabelIds': ['UNREAD'], 'addLabelIds': ['STARRED']}).execute()
		return message
	except HTTPError:
		print ('An error occurred: {}'.format(error))

def create_message(sender, to, subject, message_text, threadId):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode(), 'threadId': threadId}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print ('Message Id: %s' % message['id'])
        return message
    except HTTPError:
        print ('An error occurred: %s' % error)

def get_unread(service, user_id, label = ['UNREAD']):
	try:
		response = service.users().messages().list(userId = user_id, labelIds = label).execute()
		messages =[]
		if 'messages' in response:
			messages.extend(response['messages'])
		while 'nextPageToken' in response:
			page_token = response['nextPageToken']
			response = service.users().messages().list(userId = user_id, labelIds = label, pageToken = page_token).execute()
			messages.extend(response['messages'])
		print(messages)

		return messages
	except HTTPError:
		print('Error occured: {}'.format(error))


if __name__ == '__main__':

	creds = None
	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
		if not creds or not creds.valid:
			if creds and creds.expired and creds.refresh_token:
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file(
                	   'credentials.json', SCOPES)
				creds = flow.run_local_server(port = 0)
				with open('token.pickle', 'wb') as token:
					pickle.dump(creds, token)

	service = build('gmail', 'v1', credentials = creds)

	unread_list = get_unread(service, 'me')  

	for mail in unread_list:
		details = getMessage(service, 'me', mail['id'])
		
		subject = ''
		to = ''
		d = details['payload']['headers']
		for i in d:
			if i['name'] == 'From':
				print('sender: {}'.format(i['value']))
				to = i['value']
			if i['name'] == 'Subject':
				subject = i['value']

		sender = 'me'
		message_text = 'Hello, sent automated through API'
		message = create_message(sender, to, subject, message_text, mail['threadId'])
		send_message(service, 'me', message)
		print('success')


		


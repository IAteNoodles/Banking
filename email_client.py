from mailjet_rest import Client
<<<<<<< HEAD
from os import environ as env
api_key = env['api_key']
api_secret = env['api_secret']
=======
import os
api_key = "Key"
api_secret = "Secret"
>>>>>>> 910cc603d4a3ecb121fe47558f1239e235cee396
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
def send_mail(email: str, name: str, subject: str, text: str, html: str, custom_id: str):
  data = {
  'Messages': [
    {
      "From": {
        "Email": "project.banking.management.system@protonmail.com",
        "Name": "Banking Management System"
      },
      "To": [
        {
          "Email": email,
          "Name": name
        }
      ],
      "Subject": subject,
      "TextPart": text,
      "HTMLPart": html,
      "CustomID": custom_id
    }
  ]
}
  result = mailjet.send.create(data=data)
  print (result.status_code)
  print (result.json())

@staticmethod
def check_email(email: str):
  pass
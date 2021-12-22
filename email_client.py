from mailjet_rest import Client
import os
api_key = '3d74517449d9f7f99e09fc187bf1461d'
api_secret = '3ce95a997cd0c5ce8b67e4594c508647'
mailjet = Client(auth=(api_key, api_secret), version='v3.1')
data = {
  'Messages': [
    {
      "From": {
        "Email": "project.banking.management.system@protonmail.com",
        "Name": "Abhijit"
      },
      "To": [
        {
          "Email": "project.banking.management.system@protonmail.com",
          "Name": "Abhijit"
        }
      ],
      "Subject": "Greetings from Mailjet.",
      "TextPart": "My first Mailjet email",
      "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
      "CustomID": "AppGettingStartedTest"
    }
  ]
}
result = mailjet.send.create(data=data)
print (result.status_code)
print (result.json())

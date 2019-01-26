# parse_gmail_message
Parses the response from the Gmail API's GET message method.

  It was almost exactly what we needed. But it was in javascript. https://github.com/EmilTholin/gmail-api-parse-message

## Example usage

```python
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from parse_gmail_message import parse


client = build('gmail', 'v1', ...)

response = client().users().messages().get(userId='me', id='YOUR-MESSAGE-ID')
parsed = parse(response)

assert parsed looks_something_like ({ 
  'id': '{MESSAGE_ID}',
  'threadId': '{THREAD_ID}',
  'labelIds': [ 'SENT', 'INBOX', 'UNREAD' ],
  'snippet': 'This is one cool message, buddy.',
  'historyId': '701725',
  'internalDate': 1451995756000,
  'attachments': [{ 
    'filename': 'example.jpg',
    'mimeType': 'image/jpeg',
    'size': 100446,
    'attachmentId': '{ATTACHMENT_ID}',
    'headers': {
      'content_type': 'image/jpeg; name="example.jpg"',
      'content_description': 'example.jpg',
      'content_transfer_encoding': 'base64',
      'content_id': '...',
      ...
    }
  }],
  'inline': [{ 
    'filename': 'example.png',
    'mimeType': 'image/png',
    'size': 5551,
    'attachmentId': '{ATTACHMENT_ID}',
    'headers': {
      'content-type': 'image/jpeg; name="example.png"',
      'content-description': 'example.png',
      'content-transfer-encoding': 'base64',
      'content-id': '...',
      ...
    }
  }],
  'headers': {
    'subject': 'Example subject',
    'from': 'Example Name <example@gmail.com>',
    'to': '<foo@gmail.com>, Foo Bar <fooBar@gmail.com>',
    ...
  },
  'textPlain': 'This is one cool *message*, buddy.\r\n',
  'textHtml': '<div dir="ltr">This is one cool <b>message</b>, buddy.</div>\r\n' 
})
```

## Licence
MIT

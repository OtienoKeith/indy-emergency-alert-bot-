# Indy Emergency Alert Bot 🚨

A chatbot for Facebook Messenger that sends local emergency alerts to residents of Indianapolis by ZIP code.

## Features

- Users can subscribe using: `subscribe 46204`
- Sends either:
  - Mock alerts for demos
  - Real alerts from the NWS API
- Built with Flask + Facebook Messenger API

## Tech Stack

- Python + Flask
- Facebook Messenger Webhook API
- National Weather Service API
- Hosted with `ngrok` for development

## Setup

```bash
pip install -r requirements.txt
python app.py
``` 
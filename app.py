import os
import json
import logging
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
from mock_alerts import MOCK_ALERTS

# Setup logging
logging.basicConfig(level=logging.INFO)

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
print(f"DEBUG: VERIFY_TOKEN loaded: {repr(VERIFY_TOKEN)}")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
print(f"DEBUG: PAGE_ACCESS_TOKEN loaded: {repr(PAGE_ACCESS_TOKEN)}")
SUBSCRIBERS_FILE = "subscribers.json"

VALID_ZIPS = {
    "46201", "46202", "46203", "46204", "46205",
    "46208", "46214", "46220", "46225", "46227",
    "46228", "46235", "46236", "46237", "46239",
    "46240", "46241", "46250", "46254", "46256"
}

def fetch_nws_alerts_for_indianapolis():
    try:
        response = requests.get("https://api.weather.gov/alerts/active?area=IN")
        if response.status_code != 200:
            logging.error(f"NWS API error: {response.status_code} - {response.text}")
            return []
        data = response.json()
        alerts = []
        for alert in data.get("features", []):
            alerts.append(alert.get("properties", {}).get("headline", "Unknown alert"))
        return alerts
    except Exception as e:
        logging.error(f"Error fetching NWS alerts: {e}")
        return []

def load_subscribers():
    try:
        with open(SUBSCRIBERS_FILE, "r") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            logging.warning("subscribers.json is not a dictionary, resetting to empty dict")
            data = {}
    except Exception as e:
        logging.error(f"Could not load subscribers: {e}")
        data = {}
    return data

def save_subscribers(data):
    try:
        with open(SUBSCRIBERS_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        logging.error(f"Could not save subscribers: {e}")

def save_subscriber(zip_code, sender_id):
    data = load_subscribers()
    if zip_code not in data:
        data[zip_code] = []
    if sender_id not in data[zip_code]:
        data[zip_code].append(sender_id)
    save_subscribers(data)

def send_message(recipient_id, message):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    }
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=payload, headers=headers)
        if resp.status_code != 200:
            logging.error(f"Failed to send message: {resp.text}")
    except Exception as e:
        logging.error(f"Exception sending message: {e}")

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge, 200
        return "Invalid verification token", 403

    if request.method == "POST":
        data = request.get_json()
        logging.info(f"Received webhook: {data}")
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if "message" in event and "text" in event["message"]:
                    text = event["message"]["text"].strip()
                    lower_text = text.lower()
                    # Subscribe flow
                    if lower_text.startswith("subscribe"):
                        parts = lower_text.split()
                        if len(parts) == 2 and parts[1] in VALID_ZIPS:
                            zip_code = parts[1]
                            save_subscriber(zip_code, sender_id)
                            send_message(sender_id, f"✅ Subscribed to alerts for ZIP code {zip_code}.")
                        else:
                            send_message(sender_id, "❌ Invalid ZIP. Try: subscribe 46204")
                    # If just a ZIP code, send real alerts
                    elif text in VALID_ZIPS:
                        alerts = fetch_nws_alerts_for_indianapolis()
                        if alerts:
                            for alert in alerts:
                                send_message(sender_id, f"🚨 {alert}")
                        else:
                            send_message(sender_id, "No current emergency alerts for Indianapolis.")
                    else:
                        send_message(sender_id, "Send 'subscribe <ZIP>' to subscribe or a ZIP code to get alerts.")
        return "ok", 200

@app.route("/send_mock_alert", methods=["POST"])
def send_mock_alert():
    data = request.get_json()
    zip_code = data.get("zip")
    if zip_code not in MOCK_ALERTS:
        return jsonify({"error": "No mock alert for this ZIP"}), 400

    subscribers = load_subscribers()
    users = subscribers.get(zip_code, [])
    message = MOCK_ALERTS[zip_code]

    for user_id in users:
        send_message(user_id, message)

    return jsonify({"sent_to": len(users)}), 200

@app.route("/send_real_alert", methods=["POST"])
def send_real_alert():
    zip_code = request.get_json().get("zip")
    alerts = fetch_nws_alerts_for_indianapolis()
    subscribers = load_subscribers()
    users = subscribers.get(zip_code, [])
    if not users or not alerts:
        return jsonify({"message": "No users or alerts"}), 200

    for alert in alerts:
        for user_id in users:
            send_message(user_id, f"🚨 {alert}")

    return jsonify({"sent_to": len(users), "alerts": len(alerts)}), 200

if __name__ == "__main__":
    app.run(debug=True)

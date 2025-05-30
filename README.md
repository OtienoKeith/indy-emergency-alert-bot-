
# Indy Emergency Alert Bot 🚨

A simple chatbot built with Flask and the Facebook Messenger API that provides **real-time emergency alerts** to Indianapolis residents using the **National Weather Service (NWS) API** and mock ZIP code data.

---

## 🌟 Features

- ✅ Facebook Messenger chatbot integration
- 📍 Accepts ZIP code from user (e.g. 46201)
- 🚨 Responds with mock or real-time emergency alerts (weather, safety notices)
- 🔄 Uses [NWS API](https://www.weather.gov/documentation/services-web-api)
- 🧪 Local development using **ngrok**
- 🧰 Ready-to-deploy project with `.env` config

---

## 📦 Tech Stack

- Python 3.11+
- Flask
- Facebook Messenger API
- NWS API (mocked or real)
- Ngrok (for webhook testing)
- GitHub (code hosting)


---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/OtienoKeith/indy-emergency-alert-bot-.git
cd indy-emergency-alert-bot/alertbot
````

### 2. Create `.env` File

```env
VERIFY_TOKEN=My_secure_verify_token_123
PAGE_ACCESS_TOKEN=EAAKVlIDci6ABO3... (your full page token)
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask App

```bash
python app.py
```

Flask runs on `http://localhost:5000` by default.

---

## 🌐 Expose Your Local Server (for Facebook Webhook)

Make sure `ngrok` is installed and added to PATH:

```bash
ngrok http 5000
```

Copy the `https://xxxxx.ngrok-free.app/webhook` URL and set it as your **callback URL** in [Meta Developer Console](https://developers.facebook.com/).

---

## 💬 Facebook Messenger Setup

1. Create a Facebook Page
2. Create a Facebook App and connect your page
3. Add **Messenger** and **Webhook** products to the app
4. Use the verify token above
5. Subscribe to the `messages` event
6. Test your bot from Messenger

---

## 🧪 Example Messages

**User:** `46201`
**Bot:** `⚠️ Tornado Warning in effect until 6 PM.`

---

## 📸 Demo

[![Watch the demo](https://img.youtube.com/vi/YOUR_VIDEO_ID_HERE/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID_HERE)

---

## 📜 License

MIT License – feel free to fork, remix, and build on top of it.

---

## 🙌 Author

Keith Otieno



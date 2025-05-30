import requests

def fetch_nws_alerts_for_indianapolis():
    url = "https://api.weather.gov/alerts/active?area=IN"
    headers = {"User-Agent": "indy-alert-bot/1.0"}
    response = requests.get(url, headers=headers)
    alerts = []

    if response.status_code == 200:
        data = response.json()
        for alert in data.get("features", []):
            props = alert.get("properties", {})
            if "Indianapolis" in props.get("areaDesc", ""):
                alerts.append(props.get("headline"))
    return alerts 
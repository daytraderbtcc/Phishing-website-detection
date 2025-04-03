import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Replace with your Google Safe Browsing API Key
API_KEY = "AIzaSyAesETOJZQ37BICMo9h-EZ1XYTfMqgj5Vk"
API_URL = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={AIzaSyAesETOJZQ37BICMo9h-EZ1XYTf>

def check_url_with_api(url):
    payload = {
        "client": {"clientId": "phishing-detector", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }
    response = requests.post(API_URL, json=payload)
    data = response.json()
    return "matches" in data  # Returns True if phishing

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        url = request.form["url"]
        if check_url_with_api(url):
            result = "⚠️ Warning! This website is reported as unsafe."
        else:
            result = "✅ This website appears safe."
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

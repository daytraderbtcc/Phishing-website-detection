import requests
from flask import Flask, render_template, request, jsonify
from markupsafe import Markup

app = Flask(__name__)

# GitHub-hosted Phishing URL List
GITHUB_URL = "https://raw.githubusercontent.com/daytraderbtcc/Phishing-URL-Blacklist-/main/phishing_urls.txt"

try:
    url_list = requests.get(GITHUB_URL).text.split("\n")
except Exception as e:
    print("Error fetching phishing URL list:", str(e))
    url_list = []  # Fallback in case of error

def check_phishing(url):
    """Check if the given URL is in the phishing list."""
    if url in url_list:
        return Markup('<div class="alert alert-danger">⚠️ <b>Warning!</b> This website is flagged as <b>phishing</b>.</div>')
    else:
        return Markup('<div class="alert alert-success">✅ <b>Safe!</b> No phishing threats detected.</div>')

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/check-url", methods=["POST"])
def check_url():
    try:
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"result": '<div class="alert alert-warning">⚠️ Invalid request!</div>'}), 400

        url = data["url"].strip()
        if not url:
            return jsonify({"result": '<div class="alert alert-warning">⚠️ Please enter a valid URL!</div>'}), 400

        result = check_phishing(url)
        return jsonify({"result": str(result)})

    except Exception as e:
        print("Error processing request:", str(e))
        return jsonify({"result": '<div class="alert alert-danger">❌ Server error occurred!</div>'}), 500

if __name__ == "__main__":
    app.run(debug=True)

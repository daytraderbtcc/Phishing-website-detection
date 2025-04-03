import requests
from flask import Flask, render_template, request
from markupsafe import Markup

app = Flask(__name__)

# GitHub-hosted Phishing URL List
GITHUB_URL = "https://raw.githubusercontent.com/daytraderbtcc/Phishing-URL-Blacklist-/main/phishing_urls.txt"

try:
    response = requests.get(GITHUB_URL)
    response.raise_for_status()  # Raises an error for bad responses (e.g., 404, 500)
    url_list = {url.strip() for url in response.text.split("\n") if url.strip()}
    print(f"✅ Loaded {len(url_list)} phishing URLs.")  # Debugging: Check URL count
except Exception as e:
    print(f"❌ Error loading phishing URLs: {e}")
    url_list = set()  # Use an empty set if loading fails

def normalize_url(url):
    """Ensure the URL format matches the stored phishing list."""
    url = url.strip()
    if not url.startswith("http"):
        url = "https://" + url  # Default to HTTPS if missing
    return url.rstrip("/")  # Remove trailing slashes for consistency

def check_phishing(url):
    """Check if the URL (normalized) is in the phishing list."""
    try:
        normalized_url = normalize_url(url)
        print(f"🔍 Checking URL: {normalized_url}")  # Debugging: See what’s being checked

        if normalized_url in url_list:
            return Markup('<div class="alert alert-danger">⚠️ <b>Warning!</b> This website is flagged as <b>phishing</b>.</div>')
        else:
            return Markup('<div class="alert alert-success">✅ <b>Safe!</b> No phishing threats detected.</div>')
    except Exception as e:
        print(f"❌ Error checking URL: {e}")
        return Markup('<div class="alert alert-warning">❌ Error checking URL. Try again!</div>')

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        url = request.form["url"].strip()
        if not url:
            result = Markup('<div class="alert alert-warning">⚠️ Please enter a valid URL!</div>')
        else:
            result = check_phishing(url)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

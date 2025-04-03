import requests from flask import Flask, render_template, request from markupsafe import Markup from urllib.parse import urlparse

app = Flask(name)

GitHub-hosted Phishing URL List

GITHUB_URL = "https://raw.githubusercontent.com/daytraderbtcc/Phishing-URL-Blacklist-/main/phishing_urls.txt" response = requests.get(GITHUB_URL)

if response.status_code == 200: url_list = [url.strip() for url in response.text.split("\n") if url.strip()] else: url_list = [] print("Error fetching phishing URL list from GitHub.")

def normalize_url(url): """Normalize URL by stripping scheme and www.""" parsed = urlparse(url) domain = parsed.netloc or parsed.path  # Handle missing scheme return domain.lower().strip("/")

def check_phishing(url): """Check if the given URL is in the phishing list.""" url_normalized = normalize_url(url) phishing_urls_normalized = {normalize_url(u) for u in url_list}

print(f"Checking: {url} (Normalized: {url_normalized})")

if url_normalized in phishing_urls_normalized:
    print("\U0001F6A8 Found in list!")
    return Markup('<div class="alert alert-danger">⚠️ <b>Warning!</b> This website is flagged as <b>phishing</b>.</div>')
else:
    print("✅ Not found in list.")
    return Markup('<div class="alert alert-success">✅ <b>Safe!</b> No phishing threats detected.</div>')

@app.route("/", methods=["GET", "POST"]) def home(): result = "" if request.method == "POST": url = request.form.get("url", "").strip() if not url: result = Markup('<div class="alert alert-warning">⚠️ Please enter a valid URL!</div>') else: result = check_phishing(url) return render_template("index.html", result=result)

if name == "main": app.run(debug=True)

                         

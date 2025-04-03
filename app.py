import requests from flask import Flask, render_template, request, jsonify from markupsafe import Markup

app = Flask(name)

GitHub-hosted Phishing URL List

GITHUB_URL = "https://raw.githubusercontent.com/daytraderbtcc/Phishing-URL-Blacklist-/main/phishing_urls.txt" url_list = requests.get(GITHUB_URL).text.split("\n")

def check_phishing(url): """Check if the given URL is in the phishing list.""" if url in url_list: return Markup('<div class="alert alert-danger">⚠️ <b>Warning!</b> This website is flagged as <b>phishing</b>.</div>') else: return Markup('<div class="alert alert-success">✅ <b>Safe!</b> No phishing threats detected.</div>')

@app.route("/") def home(): return render_template("index.html")

@app.route("/check-url", methods=["POST"]) def check_url(): data = request.get_json() url = data.get("url", "").strip()

if not url:
    result = '<div class="alert alert-warning">⚠️ Please enter a valid URL!</div>'
else:
    result = check_phishing(url)

return jsonify({"result": result})

if name == "main": app.run(debug=True)


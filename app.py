import requests
from flask import Flask, render_template, request, Markup

app = Flask(__name__)

# GitHub-hosted Phishing URL List
GITHUB_URL = "https://raw.githubusercontent.com/daytraderbtcc/Phishing-URL-Blacklist-/main/phishing_urls.txt"
url_list = requests.get(GITHUB_URL).text.split("\n")

def check_phishing(url):
    """Check if the given URL is in the phishing list."""
    if url in url_list:
        return Markup('<div class="alert alert-danger">⚠️ <b>Warning!</b> This website is flagged as <b>phishing</b>.</div>')
    else:
        return Markup('<div class="alert alert-success">✅ <b>Safe!</b> No phishing threats detected.</div>')

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        url = request.form["url"]
        if url.strip() == "":
            result = Markup('<div class="alert alert-warning">⚠️ Please enter a valid URL!</div>')
        else:
            result = check_phishing(url)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, render_template, request
import os

app = Flask(__name__)
UPLOAD = "static/output"
os.makedirs(UPLOAD, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return "Form empfangen!"
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

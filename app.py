from flask import Flask, render_template, request
import os
from utils.image_tools import create_card
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="static", template_folder="templates")

# Ordner für generierte Zigarrenkarten
UPLOAD_FOLDER = 'generated_cards'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = {k: request.form.get(k, "") for k in request.form}
        bild = request.files.get("bild")
        img_path = None
        if bild and bild.filename:
            filename = secure_filename(bild.filename)
            img_path = os.path.join(UPLOAD_FOLDER, filename)
            bild.save(img_path)
            data["bildpfad"] = img_path

        # Generiere einen eindeutigen Dateinamen für die Karte
        # Dies verhindert, dass alte Karten überschrieben werden
        card_filename = f"karte_{os.urandom(8).hex()}.png"
        card_path = os.path.join(UPLOAD_FOLDER, card_filename)
        
        create_card(data, card_path)
        return render_template("result.html", card_url=f"/{UPLOAD_FOLDER}/{card_filename}")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)


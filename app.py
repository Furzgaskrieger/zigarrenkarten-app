from flask import Flask, render_template, request, send_from_directory
import os
from utils.image_tools import create_card
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder="static", template_folder="templates")

# Ordner für generierte Zigarrenkarten
UPLOAD_FOLDER = 'generated_cards'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Route zum Ausliefern der generierten Karten
@app.route(f'/{UPLOAD_FOLDER}/<path:filename>')
def serve_generated_card(filename):
    # Dient dazu, Dateien aus dem 'generated_cards'-Ordner bereitzustellen.
    # Der Pfad wird relativ zum Root-Verzeichnis der Anwendung angegeben.
    return send_from_directory(UPLOAD_FOLDER, filename)

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
        # Die URL muss nun auf die neue Route verweisen, die die generierten Karten ausliefert
        return render_template("result.html", card_url=f"/{UPLOAD_FOLDER}/{card_filename}")

    return render_template("index.html")

if __name__ == "__main__":
    # Für externen Zugriff (Wichtig!): host='0.0.0.0' ermöglicht den Zugriff von außerhalb des Containers
    app.run(debug=True, host='0.0.0.0')


from flask import Flask, render_template, request, send_from_directory
from PIL import Image, ImageDraw, ImageFont
import os
from utils.image_tools import load_cigar_image

app = Flask(__name__)
UPLOAD = "static/output"
os.makedirs(UPLOAD, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        marke = request.form["marke"]
        sorte = request.form["sorte"]
        format_ = request.form["format"]
        ringmass = request.form["ringmass"]
        laenge = request.form["laenge"]
        staerke = int(request.form["staerke"])
        dauer = request.form["dauer"]
        deckblatt = request.form["deckblatt"]
        umblatt = request.form["umblatt"]
        einlage = request.form["einlage"]
        beschreibung = request.form["beschreibung"]
        file = request.files["bild"]
        filename = "karte.jpg"
        path = os.path.join(UPLOAD, filename)
        file_path = os.path.join(UPLOAD, "upload.png")
        file.save(file_path)

        cigar_img = load_cigar_image(file_path)

        card_width, card_height = 800, 1200
        img = Image.new("RGB", (card_width, card_height), (250, 245, 235))
        draw = ImageDraw.Draw(img)
        header_brown = (150, 90, 40)
        border_brown = (90, 50, 20)
        text_black = (0, 0, 0)
        sortenrahmen = (200, 180, 160)

        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font_large = ImageFont.truetype(font_path, 50)
        font_medium = ImageFont.truetype(font_path, 36)
        font_small = ImageFont.truetype(font_path, 30)

        draw.rounded_rectangle([(0, 0), (card_width, card_height)], radius=40, outline=border_brown, width=10, fill=border_brown)
        draw.rounded_rectangle([(10, 10), (card_width - 10, card_height - 10)], radius=30, fill=(250, 245, 235))

        draw.rectangle([(10, 10), (card_width - 10, 110)], fill=header_brown)
        draw.text((card_width // 2 - 160, 25), marke, fill="black", font=font_large)

        draw.rectangle([(20, 115), (card_width - 20, 190)], fill=(255, 255, 255), outline=sortenrahmen, width=4)
        draw.text((card_width // 2 - 160, 130), sorte, fill="black", font=font_medium)

        x_text, y_text = 40, 210
        lines = [
            ("Format:", f"{format_} – {ringmass} × {laenge} mm"),
            ("Stärke:", "★" * staerke + "☆" * (5 - staerke)),
            ("Rauchdauer:", f"{dauer} Minuten"),
            ("Deckblatt:", deckblatt),
            ("Umblatt:", umblatt),
            ("Einlage:", einlage),
            ("Charakter & Besonderheiten:", beschreibung),
        ]

        for title, value in lines:
            draw.text((x_text, y_text), title, fill="black", font=font_medium)
            y_text += 40
            draw.text((x_text, y_text), value, fill="black", font=font_small)
            y_text += 50

        img.paste(cigar_img.resize((250, 700)), (card_width - 290, 300))
        img.save(path)
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    return render_template("index.html")

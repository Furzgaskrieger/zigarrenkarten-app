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

        x, y = 40, 210
        draw.text((x, y), f"Format:", fill=text_black, font=font_medium)
        y += 40
        draw.text((x, y), f"{format_} – {laenge} mm / {ringmass} Ringmaß", fill=text_black, font=font_small)
        y += 60

        draw.text((x, y), "Stärke:", fill=text_black, font=font_medium)
        y += 40
        draw.text((x, y), "★" * staerke + "☆" * (5 - staerke), fill=text_black, font=font_small)
        y += 60

        draw.text((x, y), "Rauchdauer:", fill=text_black, font=font_medium)
        y += 40
        draw.text((x, y), f"{dauer} Minuten", fill=text_black, font=font_small)
        y += 60

        draw.text((x, y), "Herstellung:", fill=text_black, font=font_medium)
        y += 40
        draw.text((x, y), f"Deckblatt: {deckblatt}", fill=text_black, font=font_small)
        y += 35
        draw.text((x, y), f"Umblatt: {umblatt}", fill=text_black, font=font_small)
        y += 35
        draw.text((x, y), f"Einlage: {einlage}", fill=text_black, font=font_small)
        y += 60

        draw.text((x, y), "Charakter & Besonderheiten:", fill=text_black, font=font_medium)
        y += 40
        lines = beschreibung.split("\n")
        for line in lines:
            draw.text((x, y), line, fill=text_black, font=font_small)
            y += 35

        if cigar_img:
            cigar_img = cigar_img.resize((200, 800))
            img.paste(cigar_img, (card_width - 220, 250), cigar_img)

        img.save(path)
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    return render_template("index.html")

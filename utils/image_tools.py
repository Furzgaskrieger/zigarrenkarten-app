from PIL import Image, ImageDraw, ImageFont
import os

def create_card(data, output_path):
    width, height = 1200, 630
    background_color = (245, 235, 220)
    img = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Pfade zu den Schriftarten relativ zum Skript
    # Stelle sicher, dass diese Schriftartdateien im 'fonts'-Ordner im Hauptverzeichnis deiner App liegen
    script_dir = os.path.dirname(__file__)
    # Geht einen Ordner hoch (von utils zu cigar_card_app_package) und dann in 'fonts'
    font_dir = os.path.join(script_dir, '..', 'fonts') 

    font_path_bold = os.path.join(font_dir, "DejaVuSans-Bold.ttf")
    font_path_regular = os.path.join(font_dir, "DejaVuSans.ttf")

    # Fallback für Schriftarten, falls sie nicht gefunden werden
    try:
        font_header = ImageFont.truetype(font_path_bold, 40)
        font_label = ImageFont.truetype(font_path_regular, 24)
        font_text = ImageFont.truetype(font_path_regular, 22)
    except IOError:
        print("Schriftarten nicht gefunden. Verwende Standard-Schriftart.")
        font_header = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_text = ImageFont.load_default()
        # Skalieren der Standard-Schriftart, da load_default() eine feste Größe hat
        font_header = font_header.font_variant(size=40)
        font_label = font_label.font_variant(size=24)
        font_text = font_text.font_variant(size=22)


    # Titel der Zigarrenkarte
    draw.text((30, 25), f"{data.get('marke', '')} – {data.get('sorte', '')}", fill="black", font=font_header)

    # Allgemeine Informationen
    lines = [
        ("Format", data.get("format", "")),
        ("Ringmaß", data.get("ringmass", "")),
        ("Länge", f"{data.get('laenge', '')} mm"),
        ("Stärke", f"{data.get('staerke', '')} Sterne"), # Angepasst für Sterne
        ("Rauchdauer", f"{data.get('dauer', '')} Min."),
    ]

    y_offset = 100
    for label, text in lines:
        draw.text((30, y_offset), f"{label}:", font=font_label, fill=(80, 50, 20))
        draw.text((250, y_offset), text, font=font_text, fill="black")
        y_offset += 40

    # Herkunftsinformationen
    y_offset += 20 # Zusätzlicher Abstand
    draw.text((30, y_offset), "Herkunft:", font=font_label, fill=(80, 50, 20))
    y_offset += 40
    draw.text((30, y_offset), "Deckblatt:", font=font_label, fill=(80, 50, 20))
    draw.text((250, y_offset), data.get("deckblatt_herkunft", ""), font=font_text, fill="black")
    y_offset += 40
    draw.text((30, y_offset), "Umblatt:", font=font_label, fill=(80, 50, 20))
    draw.text((250, y_offset), data.get("umblatt_herkunft", ""), font=font_text, fill="black")
    y_offset += 40
    draw.text((30, y_offset), "Einlage:", font=font_label, fill=(80, 50, 20))
    draw.text((250, y_offset), data.get("einlage_herkunft", ""), font=font_text, fill="black")

    # Charakter & Besonderheiten
    y_offset_charakter_label = 450 # Feste Position für den Charakter-Label
    draw.text((30, y_offset_charakter_label), "Charakter & Besonderheiten:", font=font_label, fill=(80, 50, 20))
    
    # Zeilenumbrüche für den Charakter-Text
    charakter_text = data.get("beschreibung", "")
    # Hier verwenden wir ImageDraw.multiline_text, um Zeilenumbrüche automatisch zu handhaben.
    # Wir müssen die maximale Breite berechnen, die der Text einnehmen darf.
    # Die Bildbreite ist 1200px. Wir lassen links 30px Rand und rechts Platz für das Bild (ca. 300px + 20px Rand).
    # Also 1200 - 30 - (300 + 20) = 850px maximale Textbreite.
    max_text_width = 800 # Angepasste Breite, um sicherzustellen, dass es nicht überlappt

    # Funktion zum Umbrechen von Text
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split(' ')
        current_line = []
        for word in words:
            # Testen, ob das Hinzufügen des nächsten Wortes die Zeile zu lang macht
            if draw.textbbox((0,0), ' '.join(current_line + [word]), font=font)[2] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line)) # Füge die letzte Zeile hinzu
        return '\n'.join(lines)

    wrapped_charakter_text = wrap_text(charakter_text, font_text, max_text_width)
    
    # Startposition für den umbrochenen Charakter-Text
    y_offset_charakter_text = y_offset_charakter_label + 40 
    draw.multiline_text((30, y_offset_charakter_text), wrapped_charakter_text, font=font_text, fill="black", spacing=6)

    # Bild einfügen
    if "bildpfad" in data and os.path.exists(data["bildpfad"]):
        try:
            user_img = Image.open(data["bildpfad"]).convert("RGB")
            
            # Skalierung des Bildes auf eine maximale Größe von 300x300 Pixeln
            # und Beibehaltung des Seitenverhältnisses
            user_img.thumbnail((300, 300))
            
            # Positionierung des Bildes: Rechts oben (ca. 850px von links, 50px von oben)
            # Zentrierung des Bildes im vorgesehenen Bereich
            img_x = width - user_img.width - 50 # 50px Rand von rechts
            img_y = 50 # 50px Rand von oben
            img.paste(user_img, (img_x, img_y))
        except Exception as e:
            print("Bild konnte nicht eingebunden werden:", e)
            # Optional: Füge hier eine Fehlermeldung auf der Karte ein oder ein Platzhalterbild
            draw.text((850, 150), "Bildfehler", fill="red", font=font_label)

    img.save(output_path)


from PIL import Image, ImageDraw, ImageFont
import os

def create_card(data, output_path):
    # Definierte Kartengröße für Hochformat (ca. DIN A6 bei 300 DPI)
    width, height = 1240, 1748 
    background_color = (245, 235, 220) # Helles Beige/Elfenbein
    img = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    # --- Hilfsfunktion zum Zeichnen abgerundeter Rechtecke ---
    def draw_filled_rounded_rectangle(draw_context, xy, radius, fill):
        x1, y1, x2, y2 = xy
        draw_context.ellipse((x1, y1, x1 + 2 * radius, y1 + 2 * radius), fill=fill)
        draw_context.ellipse((x2 - 2 * radius, y1, x2, y1 + 2 * radius), fill=fill)
        draw_context.ellipse((x1, y2 - 2 * radius, x1 + 2 * radius, y2), fill=fill)
        draw_context.ellipse((x2 - 2 * radius, y2 - 2 * radius, x2, y2), fill=fill)
        draw_context.rectangle((x1 + radius, y1, x2 - radius, y2), fill=fill)
        draw_context.rectangle((x1, y1 + radius, x2, y2 - radius), fill=fill)

    # --- Schriftarten laden ---
    script_dir = os.path.dirname(__file__)
    font_dir = os.path.join(script_dir, '..', 'fonts') 

    font_path_bold = os.path.join(font_dir, "DejaVuSans-Bold.ttf")
    font_path_regular = os.path.join(font_dir, "DejaVuSans.ttf")

    try:
        # Angepasste Schriftgrößen für Hochformat und Lesbarkeit
        font_marke = ImageFont.truetype(font_path_bold, 95) # Marke (noch größer)
        font_sorte = ImageFont.truetype(font_path_regular, 70) # Sorte (noch größer)
        font_label_header = ImageFont.truetype(font_path_bold, 50) # Überschriften wie "Herstellung" (größer)
        font_label_bold = ImageFont.truetype(font_path_bold, 45) # Labels wie "Format:", "Stärke:" (fett und größer)
        font_text_regular = ImageFont.truetype(font_path_regular, 42) # Inhaltstexte (normal und größer)
        font_charakter_label = ImageFont.truetype(font_path_bold, 48) # "Charakter & Besonderheiten" Überschrift (größer)
        font_charakter_text = ImageFont.truetype(font_path_regular, 40) # Charakter Text (größer gemacht)
    except IOError:
        print("Schriftarten nicht gefunden. Verwende Standard-Schriftart.")
        font_marke = ImageFont.load_default().font_variant(size=95)
        font_sorte = ImageFont.load_default().font_variant(size=70)
        font_label_header = ImageFont.load_default().font_variant(size=50)
        font_label_bold = ImageFont.load_default().font_variant(size=45)
        font_text_regular = ImageFont.load_default().font_variant(size=42)
        font_charakter_label = ImageFont.load_default().font_variant(size=48)
        font_charakter_text = ImageFont.load_default().font_variant(size=40)


    # --- Farben ---
    brand_brown = (139, 94, 60) # Mittelbraun/Orangebraun für Header und Rahmen
    text_dark = (51, 51, 51) # Dunkler Text
    label_color = (80, 50, 20) # Brauner Farbton für Labels
    white_bg = (255, 255, 255) # Weiß für den Hauptinhaltsbereich

    # --- Hauptrahmen der Karte und Hintergrund ---
    outer_border_radius = 40
    outer_border_width = 15
    
    # Zeichne den gefüllten weißen Bereich mit abgerundeten Ecken
    content_area_x1 = outer_border_width + 15 
    content_area_y1 = outer_border_width + 15
    content_area_x2 = width - (outer_border_width + 15)
    content_area_y2 = height - (outer_border_width + 15)
    
    draw_filled_rounded_rectangle(draw, (content_area_x1, content_area_y1, content_area_x2, content_area_y2), 
                                  outer_border_radius - 10, fill=white_bg) 

    # Zeichne den braunen Rahmen um den weißen Inhaltsbereich
    draw.rounded_rectangle((content_area_x1, content_area_y1, content_area_x2, content_area_y2), 
                           radius=outer_border_radius - 10, outline=brand_brown, width=outer_border_width)


    # --- Kopfbereich: Marke und Sorte ---
    header_box_y_start = content_area_y1 
    header_box_height = 320 # Noch mehr Höhe für Marke und Sorte
    
    draw.rectangle([(content_area_x1, header_box_y_start), (content_area_x2, header_box_y_start + header_box_height)], fill=brand_brown)

    # Marke (groß und fett, zentriert)
    marke_text = data.get('marke', '').upper()
    marke_bbox = draw.textbbox((0,0), marke_text, font=font_marke)
    marke_x = (width - marke_bbox[2]) / 2
    marke_y = header_box_y_start + 50 # Mehr Abstand von oben im braunen Bereich
    draw.text((marke_x, marke_y), marke_text, fill="white", font=font_marke)

    # Weißes Feld für Sorte unter der Marke (innerhalb des braunen Headers)
    sorte_box_y_start = marke_y + marke_bbox[3] + 30 # Start unter Marke mit mehr Abstand
    sorte_box_height = 110 # Erhöhte Höhe für Sorte
    
    draw.rounded_rectangle((content_area_x1 + 30, sorte_box_y_start, content_area_x2 - 30, sorte_box_y_start + sorte_box_height), 
                           radius=20, fill="white")

    # Sortenname (zentriert im weißen Feld)
    sorte_text = data.get('sorte', '')
    sorte_bbox = draw.textbbox((0,0), sorte_text, font=font_sorte)
    sorte_x = (content_area_x1 + 30) + ((content_area_x2 - 30) - (content_area_x1 + 30) - sorte_bbox[2]) / 2
    sorte_y = sorte_box_y_start + (sorte_box_height - sorte_bbox[3]) / 2
    draw.text((sorte_x, sorte_y), sorte_text, fill="black", font=font_sorte)

    # Horizontale Trennlinie unter der Sorte (innerhalb des weißen Bereichs)
    line_y = sorte_box_y_start + sorte_box_height + 40 # Mehr Abstand zur Linie
    draw.line([(content_area_x1 + 30, line_y), (content_area_x2 - 30, line_y)], fill=brand_brown, width=5)


    # --- Logo Platzhalter (oben links, innerhalb des braunen Headers) ---
    # logo_path = os.path.join(script_dir, '..', 'static', 'your_logo.png') # Beispielpfad
    # if os.path.exists(logo_path):
    #     try:
    #         logo = Image.open(logo_path).convert("RGBA")
    #         logo.thumbnail((250, 100)) # Größe anpassen
    #         img.paste(logo, (content_area_x1 + 30, content_area_y1 + 30), logo) # Oben links
    #     except Exception as e:
    #         print(f"Logo konnte nicht geladen werden: {e}")
    # else:
    #     # Wenn kein Logo vorhanden, zeige einen Text-Platzhalter
    #     draw.text((content_area_x1 + 30, content_area_y1 + 30), "Dein Logo", fill="white", font=font_label_bold)


    # --- Zigarrenbild (Rechte Spalte, groß) ---
    img_area_x_start = content_area_x1 + (content_area_x2 - content_area_x1) * 0.55 
    img_area_width = (content_area_x2 - img_area_x_start) - 30 
    img_area_y_start = line_y + 50 # Start unter der Trennlinie mit mehr Abstand
    charakter_text_start_y_global = height - 450 
    img_area_height = charakter_text_start_y_global - img_area_y_start - 30 

    if "bildpfad" in data and os.path.exists(data["bildpfad"]):
        try:
            user_img = Image.open(data["bildpfad"]).convert("RGBA") 
            
            user_img.thumbnail((img_area_width, img_area_height), Image.Resampling.LANCZOS)
            
            img_paste_x = int(img_area_x_start + (img_area_width - user_img.width) / 2)
            img_paste_y = int(img_area_y_start + (img_area_height - user_img.height) / 2)
            
            img.paste(user_img, (img_paste_x, img_paste_y), user_img)
        except Exception as e:
            print(f"Bild konnte nicht eingebunden werden: {e}")
            draw.text((img_area_x_start + 50, img_area_y_start + 100), "Bildfehler", fill="red", font=font_label_bold)
    else:
        draw.rectangle([(img_area_x_start, img_area_y_start), (img_area_x_start + img_area_width, img_area_y_start + img_area_height)], fill=(200, 200, 200))
        draw.text((img_area_x_start + 50, img_area_y_start + 100), "Kein Bild", fill="black", font=font_label_bold)


    # --- Linke Textspalte (Eckdaten und Herkunft) ---
    text_x_start = content_area_x1 + 60 # Etwas weiter eingerückt
    current_y = line_y + 100 # Noch weiter nach unten verschoben für mehr Platz oben

    # Funktion zum Zeichnen von Label und Text
    # Nutzt jetzt font_label_bold für das Label und font_text_regular für den Text
    def draw_info_line(label, text, y, label_font, text_font, label_color=label_color, text_color=text_dark):
        draw.text((text_x_start, y), f"{label}:", font=label_font, fill=label_color)
        label_width = draw.textbbox((0,0), f"{label}:", font=label_font)[2]
        draw.text((text_x_start + label_width + 25, y), text, font=text_font, fill=text_dark) 
        return y + max(label_font.getbbox("Tg")[3] - label_font.getbbox("Tg")[1], text_font.getbbox("Tg")[3] - text_font.getbbox("Tg")[1]) + 40 # Zeilenhöhe + mehr Abstand

    # Kombinierter Block der Eckdaten und Herkunftsdaten in neuer Reihenfolge
    current_y = draw_info_line("Format", data.get("format", ""), current_y, font_label_bold, font_text_regular)
    current_y = draw_info_line("Ringmaß", data.get("ringmass", ""), current_y, font_label_bold, font_text_regular)
    current_y = draw_info_line("Länge", f"{data.get('laenge', '')} mm", current_y, font_label_bold, font_text_regular)
    current_y = draw_info_line("Einlage", data.get("einlage_herkunft", ""), current_y, font_label_bold, font_text_regular)
    current_y = draw_info_line("Umblatt", data.get("umblatt_herkunft", ""), current_y, font_label_bold, font_text_regular)
    current_y = draw_info_line("Deckblatt", data.get("deckblatt_herkunft", ""), current_y, font_label_bold, font_text_regular)
    current_y = draw_info_line("Stärke", f"{data.get('staerke', '')} Sterne", current_y, font_label_bold, font_text_regular)
    current_y = draw_info_line("Rauchdauer", f"{data.get('dauer', '')} Min.", current_y, font_label_bold, font_text_regular)

    # --- Charakter & Besonderheiten (unten über die volle Breite) ---
    charakter_text_x_start = content_area_x1 + 30 
    charakter_text_y_start = charakter_text_start_y_global 
    
    draw.text((charakter_text_x_start, charakter_text_y_start), "Charakter & Besonderheiten:", font=font_charakter_label, fill=label_color)
    charakter_text_y_start += 50 

    charakter_text = data.get("beschreibung", "")
    max_charakter_text_width = content_area_x2 - charakter_text_x_start - 30 

    def wrap_text_for_drawing(text, font, max_width, draw_context):
        lines = []
        words = text.split(' ')
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if draw_context.textbbox((0,0), test_line, font=font)[2] <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line)) 
        return '\n'.join(lines)

    wrapped_charakter_text = wrap_text_for_drawing(charakter_text, font_charakter_text, max_charakter_text_width, draw)
    
    draw.multiline_text((charakter_text_x_start, charakter_text_y_start), wrapped_charakter_text, font=font_charakter_text, fill=text_dark, spacing=15) # Mehr Zeilenabstand

    img.save(output_path)

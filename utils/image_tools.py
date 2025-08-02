def create_card(data, output_path):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (800, 600), color=(245, 235, 220))
    d = ImageDraw.Draw(img)
    y = 10
    for key, value in data.items():
        d.text((10, y), f"{key}: {value}", fill=(0, 0, 0))
        y += 25
    img.save(output_path)

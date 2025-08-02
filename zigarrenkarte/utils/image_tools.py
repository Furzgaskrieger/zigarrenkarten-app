from PIL import Image

def load_cigar_image(path):
    cigar = Image.open(path).convert("RGBA")
    width = int(cigar.width * (700 / cigar.height))
    cigar = cigar.resize((width, 700))
    return cigar

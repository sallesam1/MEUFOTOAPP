from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io

def get_watermarked_bytes(filepath, text='MeuFotoApp', color='#ffffff', opacity=30, position='diagonal', stroke=False, logo_path=None):
    img = Image.open(filepath).convert('RGBA')
    r = int(color[1:3], 16) if color.startswith('#') and len(color) >= 7 else 255
    g = int(color[3:5], 16) if color.startswith('#') and len(color) >= 7 else 255
    b = int(color[5:7], 16) if color.startswith('#') and len(color) >= 7 else 255
    alpha = int(opacity * 255 / 100)

    # Tamanho da fonte proporcional e discreto (~4% da largura)
    fs = max(14, int(img.width * 0.04))
    try:
        font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', fs)
    except:
        try:
            font = ImageFont.truetype('arial.ttf', fs)
        except:
            font = ImageFont.load_default()

    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    bb = d.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    th = bb[3] - bb[1]

    if position == 'diagonal':
        # Desenha UMA vez, rotaciona -45 e posiciona discreta no canto inferior direito
        marca = Image.new('RGBA', (tw + 40, th + 40), (0, 0, 0, 0))
        dm = ImageDraw.Draw(marca)
        if stroke:
            dm.text((20, 20), text, font=font, fill=(r, g, b, alpha), stroke_width=1, stroke_fill=(0, 0, 0, alpha))
        else:
            dm.text((20, 20), text, font=font, fill=(r, g, b, alpha))
        marca = marca.rotate(-45, resample=Image.BICUBIC, expand=True)
        # Posição: canto inferior direito, com margem
        margem = int(img.width * 0.03)
        x = img.width - marca.width - margem
        y = img.height - marca.height - margem
        overlay.paste(marca, (x, y), marca)
    else:
        # Centralizada
        x = (img.width - tw) / 2
        y = (img.height - th) / 2
        if stroke:
            d.text((x, y), text, font=font, fill=(r, g, b, alpha), stroke_width=2, stroke_fill=(0, 0, 0, alpha))
        else:
            d.text((x, y), text, font=font, fill=(r, g, b, alpha))

    result = Image.alpha_composite(img, overlay)
    output = result.convert('RGB')
    buf = io.BytesIO()
    output.save(buf, format='JPEG', quality=95)
    buf.seek(0)
    return buf

def apply_watermark(filepath, text='MeuFotoApp', color='#ffffff', opacity=30, position='diagonal', stroke=False, logo_path=None):
    buf = get_watermarked_bytes(filepath, text, color, opacity, position, stroke, logo_path)
    img = Image.open(buf)
    img.save(filepath, quality=95)

def enhance_image(filepath):
    img = Image.open(filepath)
    img = ImageEnhance.Contrast(img).enhance(1.2)
    img = ImageEnhance.Brightness(img).enhance(1.1)
    img = ImageEnhance.Sharpness(img).enhance(1.3)
    img.save(filepath, quality=95)
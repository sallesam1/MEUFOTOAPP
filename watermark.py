from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io

def get_watermarked_bytes(filepath, text='MeuFotoApp', color='#ffffff', opacity=30, position='diagonal', stroke=False, logo_path=None):
    img = Image.open(filepath).convert('RGBA')
    r = int(color[1:3], 16) if color.startswith('#') and len(color) >= 7 else 255
    g = int(color[3:5], 16) if color.startswith('#') and len(color) >= 7 else 255
    b = int(color[5:7], 16) if color.startswith('#') and len(color) >= 7 else 255
    alpha = int(opacity * 255 / 100)
    fs = max(14, img.width // 25)
    try:
        font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', fs)
    except:
        try:
            font = ImageFont.truetype('arial.ttf', fs)
        except:
            font = ImageFont.load_default()

    if position == 'diagonal':
        # Canvas grande, desenha em grade, DEPOIS ROTACIONA
        canvas_w = img.width * 3
        canvas_h = img.height * 3
        diag = Image.new('RGBA', (canvas_w, canvas_h), (0, 0, 0, 0))
        d = ImageDraw.Draw(diag)
        bb = d.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        sp_x = tw + max(150, img.width // 3)
        sp_y = max(50, fs + 30)
        for y in range(0, canvas_h, sp_y):
            for x in range(0, canvas_w, sp_x):
                if stroke:
                    d.text((x, y), text, font=font, fill=(r, g, b, alpha), stroke_width=1, stroke_fill=(0, 0, 0, alpha))
                else:
                    d.text((x, y), text, font=font, fill=(r, g, b, alpha))
        # ROTACIONAR -45 GRAUS
        diag = diag.rotate(-45, resample=Image.BICUBIC)
        # CORTAR no tamanho original
        left = (diag.width - img.width) // 2
        top = (diag.height - img.height) // 2
        diag = diag.crop((left, top, left + img.width, top + img.height))
        result = Image.alpha_composite(img, diag)
    else:
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)
        fs2 = max(20, img.width // 10)
        try:
            font2 = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', fs2)
        except:
            try:
                font2 = ImageFont.truetype('arial.ttf', fs2)
            except:
                font2 = ImageFont.load_default()
        bb = d.textbbox((0, 0), text, font=font2)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        x = (img.width - tw) / 2
        y = (img.height - th) / 2
        if stroke:
            d.text((x, y), text, font=font2, fill=(r, g, b, alpha), stroke_width=2, stroke_fill=(0, 0, 0, alpha))
        else:
            d.text((x, y), text, font=font2, fill=(r, g, b, alpha))
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

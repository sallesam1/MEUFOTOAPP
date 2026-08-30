from PIL import Image

SOCIAL_SIZES = {
    'instagram_feed': (1080, 1080),
    'instagram_story': (1080, 1920),
    'facebook_feed': (1200, 630),
    'linkedin': (1200, 627),
    'twitter': (1200, 675),
    'pinterest': (1000, 1500),
    'youtube': (1280, 720),
    'whatsapp': (800, 600),
    'tiktok': (1080, 1920),
}

def resize_for_social(image_path, platform):
    if platform not in SOCIAL_SIZES:
        return None
    w, h = SOCIAL_SIZES[platform]
    img = Image.open(image_path).convert('RGB')
    img = img.resize((w, h), Image.LANCZOS)
    output = image_path.rsplit('.', 1)[0] + '_' + platform + '.jpg'
    img.save(output, quality=90)
    return output

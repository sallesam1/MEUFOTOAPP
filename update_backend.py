import os

base = os.path.dirname(os.path.abspath(__file__))

# Remove banco antigo (vai criar conta nova depois)
db_path = os.path.join(base, 'meufotoapp.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print('Banco antigo removido.')

instance_path = os.path.join(base, 'instance')
if os.path.exists(instance_path):
    import shutil
    shutil.rmtree(instance_path)
    print('Pasta instance removida.')

# Garante pastas
os.makedirs(os.path.join(base, 'uploads'), exist_ok=True)
os.makedirs(os.path.join(base, 'static', 'css'), exist_ok=True)
os.makedirs(os.path.join(base, 'templates'), exist_ok=True)

files = {}

files['requirements.txt'] = """Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-Bcrypt==1.0.1
python-dotenv==1.0.1
Pillow==10.4.0
Authlib==1.3.1"""

files['.env'] = """SECRET_KEY=meufotoapp_secret_2026
FLASK_ENV=development
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET="""

files['config.py'] = """import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-123')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///meufotoapp.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024"""

files['models.py'] = '''from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studio_name = db.Column(db.String(120))
    name = db.Column(db.String(120))
    email = db.Column(db.String(180), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    google_id = db.Column(db.String(200), unique=True, nullable=True)
    plan = db.Column(db.String(20), default='free')
    is_admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    trial_started_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Galeria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    client_name = db.Column(db.String(120))
    client_email = db.Column(db.String(180))
    category = db.Column(db.String(50))
    event_date = db.Column(db.String(20))
    client_message = db.Column(db.Text)
    share_token = db.Column(db.String(64), unique=True)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    galeria_id = db.Column(db.Integer, db.ForeignKey('galeria.id'), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    filename = db.Column(db.String(200))
    has_watermark = db.Column(db.Boolean, default=False)
    enhanced = db.Column(db.Boolean, default=False)

class Selection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    galeria_id = db.Column(db.Integer, db.ForeignKey('galeria.id'), nullable=False)
    photo_ids = db.Column(db.Text)
    package_key = db.Column(db.String(50))
    status = db.Column(db.String(20), default='received')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Watermark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(200))
    color = db.Column(db.String(20), default='#ffffff')
    opacity = db.Column(db.Integer, default=30)
    logo_path = db.Column(db.String(500))
    position = db.Column(db.String(20), default='diagonal')
    stroke = db.Column(db.Boolean, default=True)

class AppSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(120), default='MeuFotoApp')
    primary_color = db.Column(db.String(20), default='#4a90d9')
    smtp_host = db.Column(db.String(200))
    smtp_port = db.Column(db.Integer)
    smtp_user = db.Column(db.String(200))
    smtp_password = db.Column(db.String(200))

class PortfolioPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    before_path = db.Column(db.String(500))
    after_path = db.Column(db.String(500))
    title = db.Column(db.String(200))
    share_token = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PosePhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filepath = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50))
    group_name = db.Column(db.String(200))
    prompt_text = db.Column(db.Text)
    share_token = db.Column(db.String(64), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True)
    label = db.Column(db.String(100))
    limit = db.Column(db.Integer)
    price = db.Column(db.String(50))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True)
    label = db.Column(db.String(100))'''

files['watermark.py'] = '''from PIL import Image, ImageDraw, ImageFont, ImageEnhance

def apply_watermark(image_path, wm_text, color='#ffffff', opacity=30, position='diagonal', stroke=True, logo_path=None):
    img = Image.open(image_path).convert('RGBA')
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    alpha = int(opacity * 255 / 100)
    rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    fill_color = rgb + (alpha,)
    stroke_color = (0, 0, 0, alpha) if stroke else None
    try:
        font = ImageFont.truetype("arial.ttf", max(24, img.width // 20))
    except:
        font = ImageFont.load_default()
    text = wm_text or 'MeuFotoApp'
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    if position == 'diagonal':
        step_x = max(tw + 100, 200)
        step_y = max(th + 100, 150)
        for y in range(-th, img.height + th, step_y):
            for x in range(-tw, img.width + tw, step_x):
                draw.text((x, y), text, font=font, fill=fill_color, stroke_width=2 if stroke else 0, stroke_fill=stroke_color)
    else:
        x = (img.width - tw) // 2
        y = (img.height - th) // 2
        draw.text((x, y), text, font=font, fill=fill_color, stroke_width=2 if stroke else 0, stroke_fill=stroke_color)
    result = Image.alpha_composite(img, overlay)
    result = result.convert('RGB')
    result.save(image_path, quality=85)
    return image_path

def enhance_image(image_path):
    img = Image.open(image_path)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.3)
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)
    img.save(image_path, quality=90)
    return image_path'''

files['social_sizes.py'] = """from PIL import Image

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
    return output"""

for rel_path, content in files.items():
    full_path = os.path.join(base, rel_path.replace('/', os.sep))
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f'OK: {rel_path}')

print('\nBackend atualizado com sucesso!')
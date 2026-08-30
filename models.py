from datetime import datetime
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
    catalog_token = db.Column(db.String(64), unique=True, nullable=True)

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
    openai_api_key = db.Column(db.String(200))
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(120), default='MeuFotoApp')
    primary_color = db.Column(db.String(20), default='#4a90d9')
    smtp_host = db.Column(db.String(200))
    smtp_port = db.Column(db.Integer)
    smtp_user = db.Column(db.String(200))
    smtp_password = db.Column(db.String(200))

    notification_email = db.Column(db.String(180))
    smtp_server = db.Column(db.String(200))
    smtp_port = db.Column(db.Integer)
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    filename = db.Column(db.String(500))
    profession = db.Column(db.String(120))
    prompt = db.Column(db.Text)
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
    label = db.Column(db.String(100))

class PoseSelection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120))
    client_name = db.Column(db.String(120))
    client_email = db.Column(db.String(180))
    selected_poses = db.Column(db.Text)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Plan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price_monthly = db.Column(db.Float, default=0.0)
    price_yearly = db.Column(db.Float, default=0.0)
    description = db.Column(db.Text)
    max_galleries = db.Column(db.Integer, default=5)
    max_photos = db.Column(db.Integer, default=50)
    max_poses = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

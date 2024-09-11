from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    customization = db.relationship('Customization', backref='user', uselist=False)

class Customization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(100), nullable=True)
    brand_color = db.Column(db.String(7), nullable=False)
    button_primary_default_color_bg = db.Column(db.String(7), nullable=False)
    button_primary_default_color_text = db.Column(db.String(7), nullable=False)
    button_primary_default_color_stroke = db.Column(db.String(7), nullable=True)
    button_radius = db.Column(db.String(10), nullable=False)
    button_primary_hover_color_bg = db.Column(db.String(7), nullable=False)
    button_primary_hover_color_text = db.Column(db.String(7), nullable=False)
    button_primary_hover_color_stroke = db.Column(db.String(7), nullable=True)

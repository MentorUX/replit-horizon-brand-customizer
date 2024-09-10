from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    customization = db.relationship('Customization', backref='user', uselist=False)

    def get_verification_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='email-verify')

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='email-verify', max_age=1800)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Customization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(100), nullable=True)
    brand_color = db.Column(db.String(7), nullable=False)
    button_bg_color = db.Column(db.String(7), nullable=False)
    button_text_color = db.Column(db.String(7), nullable=False)
    button_radius = db.Column(db.String(10), nullable=False)
    button_hover_bg_color = db.Column(db.String(7), nullable=False)
    button_hover_text_color = db.Column(db.String(7), nullable=False)

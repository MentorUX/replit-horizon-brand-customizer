from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message
from config import Config
from forms import LoginForm, RegistrationForm, CustomizationForm
from models import db, User, Customization
from utils import save_picture
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
csrf = CSRFProtect(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        token = new_user.get_verification_token()
        verify_url = url_for('verify_email', token=token, _external=True)
        msg = Message('Verify Your Email',
                      sender='noreply@example.com',
                      recipients=[new_user.email])
        msg.body = f'''To verify your email, visit the following link:
{verify_url}

If you did not make this request then simply ignore this email and no changes will be made.
'''
        mail.send(msg)
        
        flash('A verification email has been sent to your email address. Please check your inbox.', 'info')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/verify_email/<token>')
def verify_email(token):
    user = User.verify_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('login'))
    user.is_verified = True
    db.session.commit()
    flash('Your email has been verified! You can now log in.', 'success')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            if not user.is_verified:
                flash('Please verify your email before logging in.', 'warning')
                return redirect(url_for('login'))
            login_user(user)
            return redirect(url_for('customize'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/customize', methods=['GET', 'POST'])
@login_required
def customize():
    form = CustomizationForm()
    if form.validate_on_submit():
        logo_filename = None
        if form.logo.data:
            logo_filename = save_picture(form.logo.data)
        
        customization = Customization.query.filter_by(user_id=current_user.id).first()
        if customization:
            customization.company_name = form.company_name.data
            customization.logo = logo_filename or customization.logo
            customization.brand_color = form.brand_color.data
            customization.button_bg_color = form.button_bg_color.data
            customization.button_text_color = form.button_text_color.data
            customization.button_radius = form.button_radius.data
            customization.button_hover_bg_color = form.button_hover_bg_color.data
            customization.button_hover_text_color = form.button_hover_text_color.data
        else:
            customization = Customization(
                user_id=current_user.id,
                company_name=form.company_name.data,
                logo=logo_filename,
                brand_color=form.brand_color.data,
                button_bg_color=form.button_bg_color.data,
                button_text_color=form.button_text_color.data,
                button_radius=form.button_radius.data,
                button_hover_bg_color=form.button_hover_bg_color.data,
                button_hover_text_color=form.button_hover_text_color.data
            )
            db.session.add(customization)
        
        db.session.commit()
        flash('Your customization has been saved!', 'success')
        return redirect(url_for('customize'))
    
    customization = Customization.query.filter_by(user_id=current_user.id).first()
    if customization:
        form.company_name.data = customization.company_name
        form.brand_color.data = customization.brand_color
        form.button_bg_color.data = customization.button_bg_color
        form.button_text_color.data = customization.button_text_color
        form.button_radius.data = customization.button_radius
        form.button_hover_bg_color.data = customization.button_hover_bg_color
        form.button_hover_text_color.data = customization.button_hover_text_color
    
    return render_template('customize.html', form=form, customization=customization)

@app.route('/delete_logo', methods=['POST'])
@login_required
def delete_logo():
    customization = Customization.query.filter_by(user_id=current_user.id).first()
    if customization and customization.logo:
        try:
            logo_path = os.path.join(app.root_path, 'static', 'uploads', customization.logo)
            if os.path.exists(logo_path):
                os.remove(logo_path)
            
            customization.logo = None
            db.session.commit()
            
            return jsonify({"success": True, "message": "Logo deleted successfully"})
        except Exception as e:
            return jsonify({"success": False, "message": "Error deleting logo"}), 500
    else:
        return jsonify({"success": False, "message": "No logo found"}), 404

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000)

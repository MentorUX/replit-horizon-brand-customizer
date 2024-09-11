import logging
from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect
from config import Config
from forms import LoginForm, RegistrationForm, CustomizationForm
from models import db, User, Customization
from utils import save_picture
import os

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/customize', methods=['GET', 'POST'])
@login_required
def customize():
    form = CustomizationForm()
    customization = Customization.query.filter_by(user_id=current_user.id).first()
    if form.validate_on_submit():
        try:
            if customization:
                logging.info(f"Updating existing customization for user {current_user.id}")
                customization.company_name = form.company_name.data
                customization.brand_color = form.brand_color.data
                customization.button_primary_default_color_bg = form.button_primary_default_color_bg.data
                customization.button_primary_default_color_text = form.button_primary_default_color_text.data
                customization.button_primary_default_color_stroke = form.button_primary_default_color_stroke.data
                customization.button_radius = form.button_radius.data
                customization.button_primary_hover_color_bg = form.button_primary_hover_color_bg.data
                customization.button_primary_hover_color_text = form.button_primary_hover_color_text.data
                customization.button_primary_hover_color_stroke = form.button_primary_hover_color_stroke.data
            else:
                logging.info(f"Creating new customization for user {current_user.id}")
                customization = Customization(user_id=current_user.id, company_name=form.company_name.data,
                                              brand_color=form.brand_color.data, 
                                              button_primary_default_color_bg=form.button_primary_default_color_bg.data,
                                              button_primary_default_color_text=form.button_primary_default_color_text.data,
                                              button_primary_default_color_stroke=form.button_primary_default_color_stroke.data,
                                              button_radius=form.button_radius.data,
                                              button_primary_hover_color_bg=form.button_primary_hover_color_bg.data,
                                              button_primary_hover_color_text=form.button_primary_hover_color_text.data,
                                              button_primary_hover_color_stroke=form.button_primary_hover_color_stroke.data)
                db.session.add(customization)
            if form.logo.data:
                picture_file = save_picture(form.logo.data)
                customization.logo = picture_file
            db.session.commit()
            logging.info(f"Customization saved successfully for user {current_user.id}")
            flash('Your customization has been updated!', 'success')
            return redirect(url_for('customize'))
        except Exception as e:
            logging.error(f"Error saving customization for user {current_user.id}: {str(e)}")
            db.session.rollback()
            flash('An error occurred while saving your customization. Please try again.', 'danger')
    elif request.method == 'GET' and customization:
        form.company_name.data = customization.company_name
        form.brand_color.data = customization.brand_color
        form.button_primary_default_color_bg.data = customization.button_primary_default_color_bg
        form.button_primary_default_color_text.data = customization.button_primary_default_color_text
        form.button_primary_default_color_stroke.data = customization.button_primary_default_color_stroke
        form.button_radius.data = customization.button_radius
        form.button_primary_hover_color_bg.data = customization.button_primary_hover_color_bg
        form.button_primary_hover_color_text.data = customization.button_primary_hover_color_text
        form.button_primary_hover_color_stroke.data = customization.button_primary_hover_color_stroke
    return render_template('customize.html', title='Customize', form=form, customization=customization)

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('index'))
    users = User.query.all()
    customizations = Customization.query.all()
    return render_template('admin_panel.html', users=users, customizations=customizations)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    user = User.query.get_or_404(user_id)
    if user.is_admin:
        return jsonify({'success': False, 'message': 'Cannot delete admin user'}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True, 'message': 'User deleted successfully'})

@app.route('/admin/delete_customization/<int:customization_id>', methods=['POST'])
@login_required
def delete_customization(customization_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    customization = Customization.query.get_or_404(customization_id)
    db.session.delete(customization)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Customization deleted successfully'})

def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        # Create an admin user
        admin = User(email='admin@example.com', password=generate_password_hash('admin123'), is_admin=True)
        db.session.add(admin)
        db.session.commit()
        app.logger.info("Database tables created and admin user added")

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port=5000)

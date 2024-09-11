import os
import secrets
from PIL import Image
from flask import current_app
import shutil

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/uploads', picture_fn)

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)

    if f_ext.lower() == '.svg':
        # For SVG files, just save the file without resizing
        form_picture.save(picture_path)
    else:
        # For other image formats, resize and save
        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

    return picture_fn

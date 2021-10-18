from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
import os
import PIL.Image as PIL_Image
from wand.image import Image as Wand_Image
from flask_login import login_required, current_user
from .models import User, Image
from . import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name, role=current_user.role)


@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        if 'image_file' not in request.files:
            flash('No image selected.')
            return render_template('image_form.html')

        img = request.files['image_file']
        filename = img.filename
        if filename.rsplit('.', 1)[1] != 'jpg':
            flash('Please upload jpg image.')
            return render_template('image_form.html')

        # TODO: DO NOT ALLOW UNDERSCORES IN FILENAME

        # Store image metadata in database table
        user_image = Image(user_id=current_user.id, name=filename)
        db.session.add(user_image)
        db.session.commit()

        # Create unique path
        base_path = os.path.join(f"{current_app.config.get('UPLOAD_FOLDER')}")

        # Perform image transformations and save transformed images (and thumbnail)
        transform_and_save(img, base_path, user_image.id)

        flash('File successfully uploaded.')
        return render_template('profile.html', name=current_user.name, role=current_user.role)

    return render_template('image_form.html')


@main.route('/gallery', methods=['GET'])
@login_required
def view_gallery():
    thumbnails_path = os.path.join(f"{current_app.config.get('UPLOAD_FOLDER')}/{current_user.name}/thumbnails/")
    # Initialize directory if user hasn't uploaded anything
    os.makedirs(thumbnails_path, exist_ok=True)
    return render_template('gallery.html', images_folder=thumbnails_path, current_user_name=current_user.name)


@main.route('/images/<string:image_uid>', methods=['GET'])
@login_required
def view_image(image_uid):
    image_id = image_uid.split('.', 1)[0].split('_', 1)[0]

    image = Image.query.filter_by(id=image_id).first()
    if image is None:
        flash("Selected Image does not exist anymore.")
        return render_template('profile.html', name=current_user.name, role=current_user.role)

    print(image.name)

    image_paths = [f"/static/uploads/{current_user.name}/{image_id}/main/{image_id}_{image.name}",
                   f"/static/uploads/{current_user.name}/{image_id}/blur/{image_id}_{image.name}",
                   f"/static/uploads/{current_user.name}/{image_id}/shade/{image_id}_{image.name}",
                   f"/static/uploads/{current_user.name}/{image_id}/spread/{image_id}_{image.name}"]
    return render_template('view_image.html', image_paths=image_paths)


# ---------------------------  Helper Methods  --------------------------------
def transform_and_save(image, base_path, image_id):
    # Save original Image
    main_image_folder = f"{base_path}/{current_user.name}/{image_id}/main/"
    os.makedirs(main_image_folder, exist_ok=True)
    unique_filename = f"{image_id}_{image.filename}"
    main_image_path = f"{main_image_folder}/{unique_filename}"
    image.save(main_image_path)

    # Create Thumbnail
    thumbnail_folder = f"{base_path}/{current_user.name}/thumbnails/"
    os.makedirs(thumbnail_folder, exist_ok=True)
    thumbnail_and_save(main_image_path, thumbnail_folder, unique_filename)

    # Create Blur
    blur_folder = f"{base_path}/{current_user.name}/{image_id}/blur/"
    os.makedirs(blur_folder, exist_ok=True)
    blur_and_save(main_image_path, blur_folder, unique_filename)

    # Create Shade
    shade_folder = f"{base_path}/{current_user.name}/{image_id}/shade/"
    os.makedirs(shade_folder, exist_ok=True)
    shade_and_save(main_image_path, shade_folder, unique_filename)

    # Create Spread
    spread_folder = f"{base_path}/{current_user.name}/{image_id}/spread/"
    os.makedirs(spread_folder, exist_ok=True)
    spread_and_save(main_image_path, spread_folder, unique_filename)


def thumbnail_and_save(source_image_path, destination_folder, filename):
    main_image = PIL_Image.open(source_image_path)
    thumbnail_image = main_image.resize((200, 200))
    thumbnail_image.save(f"{destination_folder}{filename}", optimize=True)


def blur_and_save(source_image_path, destination_folder, filename):
    with Wand_Image(filename=source_image_path) as img:
        img.gaussian_blur(radius=0, sigma=8)
        img.save(filename=f"{destination_folder}{filename}")


def shade_and_save(source_image_path, destination_folder, filename):
    with Wand_Image(filename=source_image_path) as img:
        img.shade(gray=True, azimuth=286.0, elevation=45.0)
        img.save(filename=f"{destination_folder}{filename}")


def spread_and_save(source_image_path, destination_folder, filename):
    with Wand_Image(filename=source_image_path) as img:
        img.spread(radius=8.0)
        img.save(filename=f"{destination_folder}{filename}")

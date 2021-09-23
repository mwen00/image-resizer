import os
import glob
import re

from flask import Blueprint, flash, g, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('resize', __name__)	
base_dir = os.path.abspath(os.path.dirname(__file__))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = 'static/uploads/'
RESIZE_WIDTHS = [100, 300, 500, 750, 1000, 1500, 2500]
UPLOAD_PATH = 'uploads/'
DOWNLOAD_PATH = 'processed/'

# TODO: Add functionality to delete images
'''
filename_dir - image path in static folder
title - filename with extension
name - filename without extension
'''

@bp.route('/')
def gallery():
    
    if g.user is not None:
      # Get the images uploaded by logged in user
      db = get_db()
      user_images = db.execute(
          'SELECT title, created, author_id'
          ' FROM images i JOIN user u ON i.author_id = u.id'
          ' WHERE u.id = ?',
          (g.user['id'],)
      ).fetchall()
      
      # Convert sqlite row object to dict
      images = [dict(row) for row in user_images]
      
      for i in images:
          i['filename_dir'] = UPLOAD_PATH + i['title']
          
          # Remove extension from title of image
          i['name'] = i['title'].split(".")[-2]
    
    return render_template('gallery.html', images=images)

def process(sizes, filename_dir):
    path = APP_ROOT + '/static/' + filename_dir
    image = Image.open(path)
    image_name, image_ext = image.filename.split("/")[-1].split('.')

    # Resize images for each of the selected sizes
    for s in sizes:
      if image.width > s:
        downsize_pct = s/image.width
            
        new_width = int(image.width * downsize_pct)
        new_height = int(image.height * downsize_pct)
        
        # Have to use absolute path to save the new image
        download_dir = APP_ROOT + '/static/' + DOWNLOAD_PATH + image_name + "_" + str(s) + "w." + image_ext
        
        # Resize and then save image
        resized_image = image.resize((new_width, new_height))
        resized_image.save(download_dir)

@bp.route('/resize/<string:title>', methods=('GET', 'POST'))
@login_required
def resize(title):
    filename_dir = UPLOAD_PATH + title
    
    # Append the width to the new resized files
    widths = [str(i) for i in RESIZE_WIDTHS]

    if request.method == 'POST':
        try:
            # Selected sizes and convert to int
            sizes = request.form.to_dict(flat=False)['sizes']
            int_sizes = [int(i) for i in sizes]
            
            process(int_sizes, filename_dir)
            
            return redirect(url_for('resize.download'))
        except:
            flash('Something went wrong. Please try again.')
    
    return render_template('resize.html', filename_dir=filename_dir, resize_widths=widths)

def allowed_file(title):
  return '.' in title and \
    title.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload():
  # TODO: Check for duplicate filenames for user
  
  if request.method == 'POST':
    file = request.files['file']
    error = None
    
    if not file:
      error = 'File is required.'
    elif not allowed_file(file.filename):
      error = 'Accepted file formats: ' + ', '.join(str(i) for i in ALLOWED_EXTENSIONS)
    
    if error is not None:
      flash(error)
    else:
      # Save the file locally 
      filename = secure_filename(file.filename)
      file.save(os.path.join(base_dir, UPLOAD_FOLDER, filename))
      
      # Associate the file with the logged in user
      db = get_db()
      db.execute(
        'INSERT INTO images (title, author_id)'
        ' VALUES (?, ?)',
        (filename, g.user['id'])
        )
      db.commit()
      
      return redirect(url_for('resize.gallery'))
  
  return render_template('upload.html')

@bp.route('/download')
@login_required
def download():
    # Location of already resized images 
    processed_dir = APP_ROOT + '/static/processed/'
    processed_images = []
    
    # Get the images uploaded by logged in user
    db = get_db()
    user_images = db.execute(
        'SELECT title'
        ' FROM images i JOIN user u ON i.author_id = u.id'
        ' WHERE u.id = ?',
        (g.user['id'],)
    ).fetchall()
    
    # Strip extension from title of image files
    titles = [i['title'].replace('.jpg', '') for i in user_images]
    
    # Create a list of resized images that match 'titles'
    for i in glob.glob(processed_dir + '*.jpg'):
        filename = i.split('/')[-1]
        filename_dir = 'processed/' + filename
        original_name = re.sub(r"_\d+w.+", "", filename)
        
        # Add filenames to list
        if original_name in titles:
            processed_images.append(filename_dir)
    
    return render_template('download.html', images=processed_images)
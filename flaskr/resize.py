import os
import glob

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

@bp.route('/gallery')
@login_required
def gallery():
    db = get_db()
    images = db.execute(
        'SELECT title, created, author_id'
        ' FROM images i JOIN user u ON i.author_id = u.id'
        ' WHERE u.id = ?',
        (g.user['id'],)
    ).fetchall()
    
    # Convert sqlite row object to dict
    images_dict = [dict(row) for row in images]
    
    for i in images_dict:
        image_filename = 'uploads/' + i['title']
        i['src'] = url_for('static', filename=image_filename)
    
    return render_template('gallery.html', images=images_dict)

def process(sizes, filename):
    path = APP_ROOT + '/static/' + filename
    img = Image.open(path)
    img_name = img.filename.split("/")[-1].strip('.jpg')
    
    for s in sizes:
        if img.width > s:
            downsize_pct = s/img.width
            
            new_width = int(img.width * downsize_pct)
            new_height = int(img.height * downsize_pct)
            
            destination_dir = 'processed/' + img_name + "_" + str(s) + "w.jpg"
            save_dir = APP_ROOT + '/static/' + destination_dir
            
            resized_img = img.resize((new_width, new_height))
            resized_img.save(save_dir)

@bp.route('/resize/<string:name>', methods=('GET', 'POST'))
@login_required
def resize(name):
    filename = 'uploads/' + name
    widths = [str(i) for i in RESIZE_WIDTHS]

    if request.method == 'POST':
        try:
            sizes = request.form.to_dict(flat=False)['sizes']
            int_sizes = [int(i) for i in sizes]
            
            process(int_sizes, filename)
            
            return redirect(url_for('resize.download'))
        except:
            flash('something went wrong')
    
    return render_template('resize.html', filename=filename, resize_widths=widths)

def allowed_file(filename):
  return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload_file():
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
      
      # TODO: Remove this eventually 
      flash('SUCCESS!!!!!!!!!')
  
  return render_template('upload.html')

@bp.route('/download')
@login_required
def download():
    
    return render_template('download.html')
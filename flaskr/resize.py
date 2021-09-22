import os

from flask import Blueprint, flash, g, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('resize', __name__)	
base_dir = os.path.abspath(os.path.dirname(__file__))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'images/uploads/'

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
        i['src'] = os.path.join(base_dir, UPLOAD_FOLDER, i['title'])
    
    return render_template('gallery.html', images=images_dict)

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

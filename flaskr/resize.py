import os

from flask import Blueprint, flash, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('resize', __name__)	
base_dir = os.path.abspath(os.path.dirname(__file__))

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'images/uploads/'

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
    
    if error is not None:
      flash(error)
    elif allowed_file(file.filename):
      filename = secure_filename(file.filename)
      img = Image.open(file)
      img.save(os.path.join(basedir, UPLOAD_FOLDER, filename))
  
  return render_template('upload.html')

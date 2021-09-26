# Image Resizer

Login or create an account and upload images (.png, .jpg, or .jpeg). These will form a gallery that can then be used to selectively resize images into standard widths that can be used for responsive web pages.

###### Video Demo: https://www.youtube.com/watch?v=gc3pFn-ycNU

## Description

This Flask application allows a user to create a new account / login and upload image files. The user can then pick from a gallery and choose to resize these images into the following widths(px): 100, 300, 500, 750, 1000, 1500, 2500. These widths are the recommended sizes from Squarespace ([more here](https://support.squarespace.com/hc/en-us/articles/206542517-Formatting-your-images-for-display-on-the-web)). The user also has the option to delete uploaded images and this will remove any resized images derived from the original file.

![app-demo](https://github.com/mwen00/image-resizer/blob/main/flaskr/static/resizer_demo.gif)

## Dependencies / Used Technologies

### Flask

Python 3.6 and newer is required. The following distributions are installed automatically when installing [Flask](https://flask.palletsprojects.com/en/2.0.x/):

* [Werkzeug](https://palletsprojects.com/p/werkzeug/)
* [Jinja](https://palletsprojects.com/p/jinja/)

A [Blueprint](https://flask.palletsprojects.com/en/2.0.x/api/#flask.Blueprint) is used to organize related views and code. In this application, there are two blueprints, one for image handling and one for authentication functions.

### Database

This app uses a small sqlite3 database to store users and uploaded image filenames.  Users can register, login, upload images, and delete images. The db could be expanded to store information for resized images and improve the download experience (e.g. implement a "download all" feature & display more descriptive information to the download page). There is also a known issue that users that upload files with the same name may view incorrect data when downloading.

To initialize the database use the `init-db` command:

``` bash
$ flask init-db
Initialized the database.
```

### Image Files

Image files are uploaded locally into `static/uploads` as their original size. Resized images are all stored in `static/processed`.

### Styling

The gallery template uses the [Masonry grid layout library](https://masonry.desandro.com/) and is initialized with jQuery. [Compiled Bootstrap v4.0.0](https://getbootstrap.com/docs/4.0/getting-started/download/) is also used locally. JQuery dependencies are imported into the `base.html` template.

## Getting Started

Currently only the development environment is implemented. To run:

``` bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

An expected output looks similar to this:

``` bash
* Serving Flask app "flaskr"
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 855-212-761
```

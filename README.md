# Image Resizer

Upload PNG/JPEG images to an account and resize the images into standard widths that can be used for responsive webpages

###### Video Demo: https://www.youtube.com/watch?v=gc3pFn-ycNU

## Description

This Flask application allows a user to create a new account and upload image files. The user can then pick from a gallery and choose to resize these images into the following widths(px): 100, 300, 500, 750, 1000, 1500, 2500. These widths are the recommended sizes from Squarespace ([more here](https://support.squarespace.com/hc/en-us/articles/206542517-Formatting-your-images-for-display-on-the-web)).

![app-demo](https://github.com/mwen00/image-resizer/blob/main/flaskr/static/resizer_demo.gif)

## Dependencies

### Database

This app uses a small sqlite3 database to store users and uploaded image filenames.  Users can register, login, upload images, and delete images. The db could be expanded to store information for resized images and improve the download experience.

### Image Files

Image files are uploaded locally into 'static/uploads' as their original size. Resized images are all stored in 'static/processed'.

### Styling

The gallery template uses the [Masonry grid layout library](https://masonry.desandro.com/) and is initialized with jQuery. [Compiled Bootstrap v4.0.0](https://getbootstrap.com/docs/4.0/getting-started/download/) is also used locally. JQuery dependencies are imported into the base.html template.

## Getting Started

``` bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

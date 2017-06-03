import os
from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory
from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = os.path.join(os.getcwd(),'/data')
UPLOAD_FOLDER = './data'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello_world():
    return 'Hello World!'

def allowed_file(filename):
    return True

@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part.')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file.')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('upload.html')

@app.route('/uploaded/<filename>')
def uploaded_file(filename):
    return 'Uploaded file {}.'.format(filename)

@app.route('/all/')
def all_files():
    filenames = [str(x) for x in os.listdir(os.path.abspath(UPLOAD_FOLDER))]
    urls = [url_for('download', filename=filename) for filename in filenames]
    return render_template('archive.html', file_download_urls = zip(filenames, urls))

@app.route('/all/<filename>')
def download(filename):
    if os.path.isfile(os.path.join(UPLOAD_FOLDER, filename)):
        return send_from_directory('data', filename, as_attachment=True)
    else:
        redirect(url_for('all_files'))




if __name__ == '__main__':
    app.run()

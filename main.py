from flask import Flask, render_template, request, flash, redirect, url_for, logging, session
from azure.storage.blob import BlockBlobService
from azure.storage.blob import PublicAccess
from azure.storage.blob import ContentSettings
import os


app = Flask(__name__)

block_blob_service = BlockBlobService(account_name='ashuazurestorage', account_key='HGvsHgPPFOp64gztvR6B9g+RNUUqzwhl+aNid8wpwca1uwejBMEhyVkP3oev1SKEnI5eeq4EIXWfcvzWjxAjuQ==')
#block_blob_service.create_container('ashu-blob-container', public_access=PublicAccess.Container)
block_blob_service.set_container_acl('ashu-blob-container', public_access=PublicAccess.Container)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        for file in request.files.getlist("file"):
            file_to_upload = file.filename
            full_path_to_file = os.path.join(os.path.dirname(__file__), file_to_upload)
            app.logger.info(file_to_upload)
            block_blob_service.create_blob_from_path(
            'ashu-blob-container',
            file_to_upload,
            full_path_to_file,
            content_settings=ContentSettings(content_type='image/png')
            )
        return render_template('complete.html')
    return render_template('upload.html')

class MyBlob(object):
    url = ''
    size = 0
    title = ''
    date = ''

    def __init__(self, url, size, title, date):
        self.url = url
        self.size = (size/1024)
        self.title = title
        self.date = date


@app.route('/viewImages', methods=['GET', 'POST'])
def viewImages():
    blobs = []
    generators = block_blob_service.list_blobs('ashu-blob-container')
    for blob in generators:
        blob_url = block_blob_service.make_blob_url('ashu-blob-container', blob.name, protocol=None, sas_token=None)
        myBlob = MyBlob(blob_url,blob.properties.content_length,blob.name,blob.properties.last_modified)
        blobs.append(myBlob)
    return render_template('viewImages.html', blobs=blobs)

if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(port=4555, debug=True)

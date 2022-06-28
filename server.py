import json, os, logging
from config import *
from PIL import Image
from copy import copy
from time import sleep
from base64 import b64encode
from traceback import format_exc
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import Flask, request, send_from_directory

app = Flask(__name__)
app.logger = logging.getLogger(LOG_PATH)
log_format = '%(asctime)s %(name)s %(levelname)s|%(process)d %(message)s'
log_formatter = logging.Formatter(log_format)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.INFO)

@app.route('/generate_thumbnail', methods=['POST'])
def generate_thumbnail():
    '''generate the thumbnail of a JPEG/PNG/BMP/JPG file'''
    default_result = {
        'code': 0,
        'message': 'default',
        'filename':'',
        'format':'',
        'size':[],
        'data': None
    }
    result = copy(default_result)

    # check if 'image' exists in request field
    if not 'image' in request.files:
        message = 'Requires "image" in request field. '
        app.logger.info(message)
        result['message'] = message
        return json.dumps(result)

    # check if uploaded file exists
    if  not request.files['image']:
        message = 'No image file found. '
        app.logger.info(message)
        result['message'] = message
        return json.dumps(result)
    
    file = request.files['image']
    image = Image.open(file.stream)
    original_format = image.format

    # check file format
    if original_format not in ALLOWED_FORMAT:
        message = f'File should be JPEG/PNG/BMP, not {original_format}. '
        app.logger.info(message)
        result['message'] = message
        return json.dumps(result)

    width, height = image.size
    data = b64encode(file.stream.read()).decode()
    filename = secure_filename(file.filename)
    location_in_queue = os.path.join(QUEUE, filename)
    if os.path.isfile(location_in_queue):
        filename = f"{data[:10]}.{original_format}"
        location_in_queue = os.path.join(QUEUE, filename)
    image.save(location_in_queue)
    image.show()

    resized_image = image.resize(NEW_SIZE)
    location_in_finised = os.path.join(FINISHED, filename)
    resized_image.save(location_in_finised, "jpeg")
    resized_image.show()
    
    result['filename'] = filename
    result['format'] = format
    result['size'] = [width, height]
    result['data'] = data
    
    app.logger.info(f"filename = {filename}")
    app.logger.info(f"format = {format}")
    app.logger.info(f"size = {[width, height]}")
    # app.logger.info(f"data = {data}")

    # return json.dumps(result)
    return send_from_directory(FINISHED, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=630, debug=True)
    # app.run(host='0.0.0.0', port=630)
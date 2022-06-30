import json, os, logging, base64, re, requests
from traceback import format_exc
from flask import Flask, request
from io import BytesIO
from hashlib import md5
from PIL import Image
from copy import copy
from time import time
from config import *

logging.basicConfig(
    filename = LOG_PATH, 
    level = logging.DEBUG, 
    format = '[%(asctime)s] %(name)s %(levelname)s|%(module)s: %(message)s'
)

app = Flask(__name__)

default_result = {
    'code': 0,
    'message': '',
    'image_data': None
}

def check_exists_in_finished(filename:str):
    '''
    Check if the resized image already exists in 'finished' folder.
    Return: image string if the resized image exists. 
    Return: None otherwise. 
    '''
    app.logger.info(f"filename = {filename}")
    location_in_finised = os.path.join(FINISHED_DIR, filename)
    app.logger.info(f"location_in_finised = {location_in_finised}")
    if os.path.isfile(location_in_finised):
        app.logger.info("Resized image already exists in finished. ")
        with open(location_in_finised, 'rb') as f:
            image_bytes = f.read()
        return base64.encodebytes(image_bytes).decode('utf-8')
        # return base64.b64encode(image_bytes)
    app.logger.info("Resized image does not exist in finished. ")
    return False

def check_image_format(original_format:str):
    '''
    Check if image format is jpg/jpeg/png/bmp. 
    return: True if format is allowed
    return: False otherwise
    '''
    app.logger.info(f"original format = {original_format}")
    if original_format in ALLOWED_FORMAT:
        return None
    message = f'File should be jpg/jpeg/png/bmp, not {original_format}. '
    app.logger.info(message)
    return message

@app.route('/generate_thumbnail', methods=['POST'])
def generate_thumbnail():
    '''generate the thumbnail of a JPEG/PNG/BMP/JPG file'''
    strart_time = time()
    result = copy(default_result)
    image_data_type = ''
    original_format = ''
    image_file = None
    image_data = None
    filename = ''
    image = None

    # Check if image file/url/data(bytes) exist in request. 
    # Then check if resized image has been saved in 'finished' folder. 
    try:
        content = request.json
        if 'image_file' in request.files:
            image_file = request.files['image_file']
            image = Image.open(image_file.stream)
            original_format = image.format
            if original_format.lower() == 'jpg':
                original_format = 'jpeg' 
            message = check_image_format(original_format)
            if message:
                result['message'] = message
                return json.dumps(result)
            original_image_hash = md5(image.tobytes()).hexdigest()
            filename = f"{original_image_hash}.{original_format}"
            image_data = check_exists_in_finished(filename)
            if image_data:
                result['code'] = 1
                result['message'] = 'SUCCESS'
                result['image_data'] = image_data
                app.logger.info(f"image_data = {image_data}")
                return json.dumps(result)
            image_data_type = 'file'

        elif 'image_url' in content:
            image_url = content['image_url']
            regex_result = re.findall(r'\.(jpg|jpeg|png|bmp)$', image_url, re.IGNORECASE)
            if not regex_result:
                result['message'] = 'Image URL should end with .jpg/.jpeg/.png/.bmp. '
                return json.dumps(result)
            original_format = regex_result[-1]
            if original_format.lower() == 'jpg':
                original_format = 'jpeg' 
            filename = image_url[-50:]
            image_data = check_exists_in_finished(filename)
            if image_data:
                result['code'] = 1
                result['message'] = 'SUCCESS'
                result['image_data'] = image_data
                app.logger.info(f"image_data = {image_data}")
                return json.dumps(result)
            image_downloaded = requests.get(image_url, stream=True)
            image = Image.open(BytesIO(image_downloaded.content))
            image_data_type = 'url'

        elif 'image_data' in content:
            original_image_bytes = content['image_data']
            original_image_data = base64.b64decode(original_image_bytes)
            buffer = BytesIO(original_image_data)
            image = Image.open(buffer)
            original_format = image.format
            if original_format.lower() == 'jpg':
                original_format = 'jpeg' 
            message = check_image_format(original_format)
            if message:
                result['message'] = message
                return json.dumps(result)
            filename = f"{md5(original_image_bytes.encode('utf-8')).hexdigest()}.{original_format}"
            image_data = check_exists_in_finished(filename)
            if image_data:
                result['code'] = 1
                result['message'] = 'SUCCESS'
                result['image_data'] = image_data
                app.logger.info(f"image_data = {image_data}")
                return json.dumps(result)
            image_data_type = 'bytes'
        else:
            result['message'] = 'Cannot find image in request. '
            return json.dumps(result)
    except:
        result['message'] = format_exc()
        print(format_exc())
        return json.dumps(result)
    
    app.logger.info(f"original data type = {image_data_type}")
    
    # If the resized image file is not found in 'finished' folder,
    # resize the image and save in 'finished' folder. 
    try:
        resized_image = image.resize(NEW_SIZE)
        location_in_finised = os.path.join(FINISHED_DIR, filename)
        resized_image.save(location_in_finised, format=original_format)
        # image.show()
        # resized_image.show()

        buffer = BytesIO()
        resized_image.save(buffer, format=original_format)
        result['image_data'] = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        # calculate time cost
        end_time = time()
        time_cost = round(end_time - strart_time, 4)
        time_cost_sec = int(time_cost)
        time_cost_ms = int((time_cost - time_cost_sec)*1000)
        app.logger.info(f"Time cost = {time_cost_sec}s{time_cost_ms}ms")
        return json.dumps(result)
    except:
        message = format_exc()
        result['message'] = message
        app.logger.exception(f"[exception] {message}")
        print(f"[exception] {message}")
        return json.dumps(result)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=630, debug=True)
    app.run(host='0.0.0.0', port=630)
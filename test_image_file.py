import os, json, base64, requests
from traceback import print_exc
from io import BytesIO
from PIL import Image
from config import *
from pprint import pprint
from PIL import Image

url = 'http://localhost:630/generate_thumbnail'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# test with image file
image_file = os.path.join(EXAMPLE_DIR, 'dog 1.jpeg')
with open(image_file, "rb") as f:
    image_bytes = f.read()
image_data = base64.b64encode(image_bytes).decode("utf-8")
original_image_data = base64.b64decode(image_data)
buffer = BytesIO(original_image_data)
image = Image.open(buffer)
image.show()
payload = json.dumps({"image_data": image_data})

try:
    response = requests.post(url, data=payload, headers=headers)
    response_dict = response.json()
    print(f"response_dict={response_dict}")
    image_data = response_dict['image_data']
    if image_data:
        resized_image_data = base64.b64decode(image_data)
        buffer = BytesIO(resized_image_data)
        image = Image.open(buffer)
        image.show()
    else:
        pprint(response_dict)
except:
    print_exc()
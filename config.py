import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(ROOT_DIR, "logs/thumbnail_generator.log")
QUEUE = os.path.join(ROOT_DIR, "queue")
FINISHED = os.path.join(ROOT_DIR, "finished")
ALLOWED_FORMAT = {'JPEG', 'PNG', 'BMP', 'JPG'}
NEW_SIZE = (100, 100)
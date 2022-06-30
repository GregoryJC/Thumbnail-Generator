import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(ROOT_DIR, "logs/thumbnail_generator.log")
EXAMPLE_DIR = os.path.join(ROOT_DIR, "examples")
FINISHED_DIR = os.path.join(ROOT_DIR, "finished")
ALLOWED_FORMAT = {'JPEG', 'PNG', 'BMP', 'JPG'}
NEW_WIDTH = 100
NEW_HEIGHT = 100
NEW_SIZE = (NEW_WIDTH, NEW_HEIGHT)
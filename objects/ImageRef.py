import requests
from io import BytesIO
from PIL import Image


class ImageRef:
    def __init__(self, image_id, url):
        self._image_id = image_id
        self._url = url

    def get_image_id(self):
        return self._image_id

    def set_attribute1(self, image_id):
        self._image_id = image_id

    def get_url(self):
        return self._url

    def set_url(self, url):
        self._url = url

    def show_img(self):
        response = requests.get(self._url)
        image_content = response.content
        image_bytes = BytesIO(image_content)
        img = Image.open(image_bytes)
        # img.show() TODO: fix implement


import pickle


class Report:

    def __init__(self, report_id, reporter_email, text, image, wp_id, direction):
        self._report_id = report_id
        self._reporter_email = reporter_email
        self._text = text
        self._image = image
        self._wp_id = wp_id
        self._direction = direction

    def get_report_id(self):
        return self._report_id

    def set_report_id(self, report_id):
        self._report_id = report_id

    def get_reporter_email(self):
        return self._reporter_email

    def set_reporter_email(self, reporter_email):
        self._reporter_email = reporter_email

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text

    def get_image(self):
        return self._image

    def set_image(self, image):
        self._image = image

    def get_wp_id(self):
        return self._wp_id

    def set_wp_id(self, wp_id):
        self._wp_id = wp_id

    def get_direction(self):
        return self._direction

    def set_direction(self, direction):
        self._direction = direction

    def serialize(self):
        return {
            'report_id': self.get_report_id(),
            'reporter_email': self.get_reporter_email(),
            'text': self.get_text(),
            'image': self.get_image(),
            'wp_id': self.get_wp_id(),
            'direction': self.get_direction()
        }

import pickle


class Report:

    def __init__(self, report_id, reporter_email, description, wp_id, direction, site_name):
        self._report_id = report_id
        self._reporter_email = reporter_email
        self._description = description
        self._wp_id = wp_id
        self._direction = direction
        self._site_name = site_name

    def get_report_id(self):
        return self._report_id

    def set_report_id(self, report_id):
        self._report_id = report_id

    def get_reporter_email(self):
        return self._reporter_email

    def set_reporter_email(self, reporter_email):
        self._reporter_email = reporter_email

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._description = description

    def get_wp_id(self):
        return self._wp_id

    def set_wp_id(self, wp_id):
        self._wp_id = wp_id

    def get_direction(self):
        return self._direction

    def set_direction(self, direction):
        self._direction = direction

    def get_site_name(self):
        return self._site_name

    def set_site_name(self, site_name):
        self._site_name = site_name

    def serialize(self):
        return {
            'report_id': self.get_report_id(),
            'reporter_email': self.get_reporter_email(),
            'description': self.get_description(),
            'wp_id': self.get_wp_id(),
            'direction': self.get_direction(),
            'site_name': self.get_site_name()
        }

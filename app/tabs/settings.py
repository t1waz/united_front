import constants
from cache import CACHE
from tabs import BaseTab


class SettingsTab(BaseTab):
    ACCESS_TOKEN_RESPONSE_KEY = 'access'

    def _clear_settings_data(self):
        self.ids.settings_username.text = ''
        self.ids.settings_password.text = ''

    def _handle_status_label(self):
        if CACHE.get('access_token') is not None:
            self.ids.settings_status_label.text = 'LOGGED'
            self.ids.settings_status_label.color = (0, 1, 0, 1)
        else:
            self.ids.settings_status_label.text = 'NOT LOGGED'
            self.ids.settings_status_label.color = (1, 0, 0, 1)

    def settings_tab_click(self):
        self._clear_settings_data()
        self._handle_status_label()

        self.terminate_robot_data_process()

    def login(self):
        response = self._get_response(
            method='post',
            url=constants.LOGIN_URL,
            data={
                'username': self.ids.settings_username.text,
                'password': self.ids.settings_password.text,
            },
        )

        self._clear_settings_data()

        if not response or response.status_code != 200:
            CACHE['access_token'] = None
            self.display_error_popup(message='external error')
        else:
            CACHE['access_token'] = response.json()[self.ACCESS_TOKEN_RESPONSE_KEY]

        self._handle_status_label()

from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown

import constants
from cache import CACHE
from tabs import BaseTab


class RobotTab(BaseTab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._robot_dropdown = DropDown()

    def _setup_robot_dropdown(self, robot_data):
        self._robot_dropdown.clear_widgets()
        for robot_uuid in robot_data:
            robot_button = Button(text=robot_uuid, size_hint_y=None, height=50)
            robot_button.bind(on_release=lambda btn: self._robot_dropdown_click(btn))
            setattr(robot_button, 'robot_uuid', robot_uuid)
            self._robot_dropdown.add_widget(robot_button)

        self.ids.robot_available_robots.bind(on_release=self._robot_dropdown.open)

    def robot_tab_click(self):
        self._robot_dropdown.clear_widgets()
        self.ids.robot_available_robots.text = 'SELECT ROBOT'

        response = self._get_response(
            method='get', url=constants.ME_URL, is_authenticated=True
        )
        if response.status_code != 200:
            self.display_error_popup(message='login first')
            return

        self._setup_robot_dropdown(robot_data=response.json().get('robots'))

    def _robot_dropdown_click(self, button):
        CACHE['current_robot_uuid'] = getattr(button, 'robot_uuid')
        self.ids.robot_available_robots.text = CACHE['current_robot_uuid']
        self._robot_dropdown.dismiss()

        self.terminate_robot_data_process()

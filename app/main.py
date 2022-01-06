from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.utils import platform

from tabs.control import ControlTab
from tabs.robot import RobotTab
from tabs.settings import SettingsTab


if platform != 'android':
    Window.size = (540, 960)

Builder.load_file('ui.kv')

CACHE = {}


class UnitedApp(SettingsTab, RobotTab, ControlTab, TabbedPanel):
    pass


class TabbedPanelApp(App):
    def build(self):
        return UnitedApp()


if __name__ == '__main__':
    TabbedPanelApp().run()

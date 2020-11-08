import common_environ_set
from qtpy.QtWidgets import QStyleFactory, QCommonStyle


class StyleManager:
    """Style manager class"""
    def __init__(self, app_ptr):
        self.app_ptr = app_ptr
        self.native_styles = QStyleFactory.keys()
        print(self.native_styles)

    def list_styles(self):
        return self.native_styles

    def change_style(self, new_style):
        if new_style == "Classic":
            print(self.native_styles)
            self.app_ptr.setStyle(self.native_style[0])
        else:
            self.app_ptr.setStyle(new_style)

import common_environ_set
from qtpy.QtWidgets import QStyleFactory, QAction


class StyleManager:
    """Style manager class"""
    def __init__(self, app_ptr):
        self.app_ptr = app_ptr
        self.native_styles = QStyleFactory.keys()

    def list_styles(self):
        """List the available application styles for the current OS. """
        return self.native_styles

    def add_styles_to_menu(self, main_win, menu_style, style_group):
        """Add all the available styles to the Menu styles in the bar menu in a mutually exclusive action group. """
        style_list = self.list_styles()
        if style_list:
            default_style = style_list[0]
            for st in style_list:
                style_action = QAction(main_win)
                style_action.setObjectName(st)
                style_action.setCheckable(True)
                style_action.setText(st)
                if st == default_style:
                    style_action.setChecked(True)
                menu_style.addAction(style_action)
                style_group.addAction(style_action)

    def change_style(self, new_style):
        """Set the new style"""
        self.app_ptr.setStyle(new_style)

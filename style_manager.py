from qtpy.QtWidgets import QStyleFactory, QAction
from qtpy.QtGui import QPalette, QColor
from qtpy.QtCore import Qt


class StyleManager:
    """Style manager class"""
    def __init__(self, app_ptr):
        self.app_ptr = app_ptr
        self.native_styles = QStyleFactory.keys()
        self.default_palette = QPalette()

    def list_styles(self):
        """List the available application styles for the current OS. """
        return self.native_styles

    def add_styles_to_menu(self, main_win, menu_style, style_group, palette_group):
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
                if st.lower() == "fusion":
                    menu_style.addSeparator()
                    palette_action = QAction(main_win)
                    palette_action.setObjectName("Dark")
                    palette_action.setText("Dark")
                    palette_action.setCheckable(True)
                    if default_style.lower() == "fusion":
                        palette_action.setEnabled(True)
                    menu_style.addAction(palette_action)
                    palette_group.addAction(palette_action)

    def change_style(self, new_style):
        """Set the new style"""
        self.app_ptr.setStyle(new_style)
        # if new_style.lower() == "fusion":

    def set_palette(self, new_palette):
        dark_gray = QColor(53,53,53)
        gray = QColor(128, 128, 128)
        black = QColor(25, 25, 25)
        blue = QColor(42, 130, 218)

        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, dark_gray)
        dark_palette.setColor(QPalette.Window, dark_gray)
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, black)
        dark_palette.setColor(QPalette.AlternateBase, dark_gray)
        dark_palette.setColor(QPalette.ToolTipBase, blue)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, dark_gray)
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.Link, blue)
        dark_palette.setColor(QPalette.Highlight, blue)
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)

        dark_palette.setColor(QPalette.Active, QPalette.Button, gray.darker())
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, gray)
        dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, gray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, gray)
        dark_palette.setColor(QPalette.Disabled, QPalette.Light, dark_gray)

        self.app_ptr.setPalette(dark_palette)

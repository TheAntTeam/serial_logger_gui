class StyleManager():
    """Style manager class"""
    def __init__(self, app_ptr):
        self.app_ptr = app_ptr

    def change_style(self):
        app.setStyle('Fusion')

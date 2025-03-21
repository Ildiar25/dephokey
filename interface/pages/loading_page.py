import flet as ft

from shared.utils.colors import neutral00, secondaryCorporateColor


class LoadingPage(ft.Container):
    """Creates Loading page and displays it between pages navigation"""
    def __init__(self):
        super().__init__()

        # Main container settings
        self.alignment = ft.alignment.top_center
        self.expand = True
        self.bgcolor = ft.Colors.with_opacity(opacity=0.3, color=neutral00)
        self.image = ft.DecorationImage(src="interface/assets/bgimage-load-page.png", fit=ft.ImageFit.COVER)

        # Content
        self.content = ft.ProgressBar(color=secondaryCorporateColor)

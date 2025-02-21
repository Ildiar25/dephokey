import flet as ft

from shared.utils.colors import *


class LoadingPage(ft.Container):

    def __init__(self):
        super().__init__()

        # Main container settings
        self.alignment = ft.alignment.top_center
        self.expand = True
        self.bgcolor = ft.Colors.with_opacity(0.3, neutral00)
        self.image = ft.DecorationImage(src="interface/assets/bgimage-load-page.png", fit=ft.ImageFit.COVER)

        # Content
        self.content = ft.ProgressBar(color=secondaryCorporateColor)

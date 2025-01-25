import flet as ft

from shared.utils.colors import *


class LoadPage(ft.Container):

    def __init__(self):
        super().__init__()

        # Main container settings
        self.alignment = ft.alignment.center
        self.expand = True
        self.bgcolor = ft.Colors.with_opacity(0.3, neutral00)

        # Content
        self.content = ft.ProgressRing(color=secondaryCorporateColor)

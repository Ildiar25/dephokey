import flet as ft


def main(page: ft.Page):

    page.bgcolor = ft.Colors.RED

    page.overlay.append(
        ft.Container(
            alignment=ft.alignment.center,
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.WHITE),
            content=ft.ProgressRing(
                color=ft.Colors.AMBER_ACCENT_400
            )
        )
    )
    page.update()


if __name__ == "__main__":
    ft.app(target=main)

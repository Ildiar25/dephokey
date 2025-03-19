
"""
App color settings

This file helps to define all colors used through the app. It includes corporate colors and its variants,
grayscale, generic status colors and text colors.

"""

from flet import Colors

# Corporate colors
primaryCorporateColor: str = "#4860B5"
secondaryCorporateColor: str = "#FB9820"


# Corporate variants
primaryCorporate100: str = "#0E2060"
primaryCorporate75: str = "#32548C"
primaryCorporate25: str = "#95A6E1"
primaryCorporate00: str = "#CBD4F4"
secondaryCorporate100: str = "#802305"
secondaryCorporate75: str = "#BF5610"
secondaryCorporate25: str = "#FFB55B"
secondaryCorporate00: str = "#FDD29F"


# General greyscale Colors
neutral00: Colors = Colors.WHITE      # 0xFFFFFF
neutral05: Colors = Colors.GREY_200   # 0xF2F2F2
neutral10: Colors = Colors.GREY_300   # 0xE6E6E6
neutral20: Colors = Colors.GREY_400   # 0xCDCDCD
neutral40: Colors = Colors.BLACK38    # 0x9A9A9A
neutral60: Colors = Colors.GREY_700   # 0x686868
neutral80: Colors = Colors.GREY_900   # 0x333333


# Neutral colors
neutralSuccessDark: str = "#217B21"
neutralSuccessMedium: str = "#32B832"
neutralSuccessLight: str = "#B7EAB7"
neutralInfoDark: str = "#0E2060"
neutralInfoMedium: str = "#4860B5"
neutralInfoLight: str = "#95A6E1"
neutralDangerDark: str = "#9C001C"
neutralDangerMedium: str = "#D80027"
neutralDangerLight: str = "#F6A8B3"
neutralWarningMedium: Colors = Colors.AMBER_600
neutralWarningLight: Colors = Colors.AMBER_300
transparentColor: Colors = Colors.TRANSPARENT


# Text colors
primaryTextColor: Colors = neutral80
secondaryTextColor: Colors = neutral40
tertiaryTextColor: Colors = neutral00
accentTextColor: str = primaryCorporateColor
successTextColor: str = neutralSuccessDark
infoTextColor: str = neutralInfoDark
warningTextColor: Colors = neutralWarningMedium
dangerTextColor: str = neutralDangerDark

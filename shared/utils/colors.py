from flet import Colors

# TODO: Rename colors base on first color names

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
neutral00: Colors = Colors.WHITE      # #FFFFFF
neutral05: Colors = Colors.GREY_200   # #F2F2F2
neutral10: Colors = Colors.GREY_300   # #E6E6E6
neutral20: Colors = Colors.GREY_400   # #CDCDCD
neutral40: Colors = Colors.BLACK38    # #9A9A9A
neutral60: Colors = Colors.GREY_700   # #686868
neutral80: Colors = Colors.GREY_900   # #333333


# Neutral colors
neutralSuccessDark: str = "#217B21"
neutralSuccessMedium: str = "#32B832"
neutralSuccessLight: str = "#B7EAB7"
neutralInfoDark: str = primaryCorporate100
neutralInfoMedium: str = primaryCorporateColor
neutralInfoLight: str = primaryCorporate25
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


# Icon-text colors
primaryIconColor: Colors = neutral80
secondaryIconColor: Colors = neutral40
tertiaryIconColor: Colors = neutral00
accentIconColor: str = primaryCorporateColor


# Appbar colors
bgAppbarColor: Colors = neutral80
iconAppbarColor: Colors = neutral05
selectedIconAppbarColor: str = primaryCorporateColor


# Sidebar colors
bgSidebarColor: Colors = neutral80
selectSidebarColor: str = primaryCorporateColor
iconSidebarColor: Colors = neutral05
textSidebarColor: Colors = tertiaryTextColor


# Footer colors
bgFooterColor: str = primaryCorporateColor
textFooterColor: Colors = tertiaryTextColor


# Snackbar colors
bgSnackbarDangerColor:str = neutralDangerLight
bgSnackbarInfoColor: str = primaryCorporate25
bgSnackbarSuccessColor: str = neutralSuccessLight
bgSnackbarWarningColor: Colors = neutralWarningLight


# Textfield colors
cursorTextfieldColor: str = primaryCorporateColor
selectCursorTextfieldColor: Colors = secondaryTextColor
staticBorderTextfieldColor: Colors = neutral20
selectedBorderTextfieldColor: str = primaryCorporateColor


# E-button colors
bgEButtonColor: str = primaryCorporateColor
bgHoverEButtonColor: str = primaryCorporate25
bgDissabledEButtonColor: Colors = neutral10
borderEButtonColor: str = primaryCorporateColor
borderDissabledEButtonColor: Colors = neutral20
borderHoverEButtonColor: str = primaryCorporate25


# Sitewidget colors
bgSiteWidgetColor: Colors = neutral00
titleSiteWidgetColor: Colors = primaryTextColor
textSiteWidgetColor: Colors = neutral60
accentSiteWidgetColor: Colors = tertiaryTextColor


# Creditcardwidget colors
bgCreditcardWidgetColor = primaryCorporateColor
titleCreditcardWidgetColor = tertiaryTextColor


# Notewidget colors
bgNoteWidgetColor = neutral00
titleNoteWidgetColor = primaryTextColor
textNoteWidgetColor = neutral60
accentNoteWidgetColor = tertiaryTextColor
iconNoteWidgetColor = neutral80
iconAccentNoteWidgetColor = primaryCorporateColor


# General form colors
bgGeneralFormColor = neutral00
iconGeneralFormColor = neutral00
iconAccentGeneralFormColor = neutral80
selectedIconGeneralFormColor = neutral40
hoverIconGeneralFormColor = neutral20

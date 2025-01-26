from flet import Colors


# Corporate colors
primaryCorporateColor = "#4860B5"
secondaryCorporateColor = "#FB9820"


# Corporate variants
darkPrimaryCorporateColor = "#0E2060"
lightPrimaryCorporateColor = ""
darkSecondaryCorporateColor = ""
lightSecondaryCorporateColor = ""


# General color styles
neutral00 = Colors.WHITE      #FFFFFF
neutral05 = Colors.GREY_200   #F2F2F2
neutral10 = Colors.GREY_300   #E6E6E6
neutral20 = Colors.GREY_400   #CDCDCD
neutral40 = Colors.BLACK38    #9A9A9A
neutral60 = Colors.GREY_700   #686868
neutral80 = Colors.GREY_900   #333333

neutralSuccess = "#32B832"
neutralInfo = primaryCorporateColor
neutralWarning = ""
neutralDanger = "#D80027"

transparentColor = Colors.TRANSPARENT


# Text colors
primaryTextColor = neutral80
secondaryTextColor = neutral40
tertiaryTextColor = neutral00
accentTextColor = primaryCorporateColor
successTextColor = neutralSuccess
infoTextColor = neutralInfo
warningTextColor = neutralWarning
dangerTextColor = neutralDanger


# Appbar colors
bgAppbarColor = neutral80
iconAppbarColor = neutral05


# Sidebar colors
bgSidebarColor = neutral80
selectSidebarColor = primaryCorporateColor
iconSidebarColor = neutral05
textSidebarColor = tertiaryTextColor


# Footer colors
bgFooterColor = primaryCorporateColor
textFooterColor = tertiaryTextColor


# Snackbar colors
bgSnackbarDangerColor = Colors.with_opacity(0.3, neutralDanger)
bgSnackbarInfoColor = Colors.with_opacity(0.3, neutralInfo)
bgSnackbarSuccessColor = Colors.with_opacity(0.3, neutralSuccess)
bgSnackbarWarningColor = Colors.with_opacity(0.3, neutralWarning)
textSnackbarColor = tertiaryTextColor


# Checkbox colors
selectedBorderCheckboxColor = Colors.PURPLE_600
defaultFillCheckboxColor = Colors.GREY_300
selectedFillCheckboxColor = Colors.PURPLE_400


# Textfield colors
cursorTextfieldColor = accentTextColor
selectCursorTextfieldColor = secondaryTextColor
labelTextfieldColor = secondaryTextColor

staticBorderTextfieldColor = neutral20
selectedBorderTextfieldColor = primaryCorporateColor


# T-button colors
dissabledTButtonColor = neutral10
textColorTextButton = Colors.PURPLE_600
overlayColorTextButton = Colors.GREY_300

# E-button colors
dissabledEButtonColor = neutral10
borderEButtonColor = primaryCorporateColor
bgEButtonColor = primaryCorporateColor

# F-button
bgFloatingButtonColor = Colors.DEEP_PURPLE_100
fgFloatingButtonColor = Colors.DEEP_PURPLE_600
focusFloatingButtonColor = Colors.DEEP_PURPLE_600

# Admin page settings
bgGradientAdminColor = [Colors.WHITE, Colors.WHITE]
colorAdminAccent = Colors.PURPLE_ACCENT

# Login & Signin settings
bgAccentForm = Colors.PURPLE
accentElementForm = Colors.PURPLE_600
shadowLogForm = Colors.PURPLE_700

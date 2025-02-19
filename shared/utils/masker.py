

def mask_email(email: str) -> str:
    local, domain = email.split("@")
    masked = "•" * len(local)
    return masked + "@" + domain


def mask_username(username: str) -> str:
    if "@" in username:
        return mask_email(username)

    else:
        masked = "•" * len(username[3:])
        return username[:3] + masked


def mask_password(passsword: str) -> str:
    return "•" * len(passsword)


def mask_number(number: str) -> str:
    masked = "•" * len(number[:-4])
    return masked + number[-4:]


def mask_phone(phone: str) -> str:
    masked = "•" * len(phone[:-3])
    return masked + phone[-3:]


def mask_text(text: str) -> str:
    masked = ""
    for char in text:
        if char == " ":
            masked += " "
        else:
            masked += "•"
    if len(masked) > 120:
        return masked[:120] + "..."
    return masked

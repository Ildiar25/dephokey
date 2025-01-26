

def mask_email(email: str) -> str:
    local, domain = email.split("@")
    masked = "*" * len(local)
    return masked + "@" + domain


def mask_username(username: str) -> str:
    pass


def mask_password(passsword: str) -> str:
    return "*" * len(passsword)


def mask_number(number: str) -> str:
    masked = "*" * len(number[:-4])
    return masked + number[-4:]


def mask_phone(phone: str) -> str:
    masked = "*" * len(phone[:-3])
    return masked + phone[-3:]


def mask_text(text: str) -> str:
    if len(text) >= 20:
        return "*" * 17 + "..."
    return "*" * len(text)
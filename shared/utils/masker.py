
"""
Sensitive-data masking functions

This file provides a set of masking functions to mask sensitive data such emails, passwords, different credential types,
phone numbers, credit card numbers and different texts.

These functions are designed to protect user's privacy replacing sensitive data with masking characters (e.g: "•").

Included functions:
    mask_email: Masks the email local part.
    mask_username: Masks a username, whether it's an email or a simple name.
    mask_password: Masks the password.
    mask_number: Masks any number except the last four characters.
    mask_phone: Masks the phone number except the last three characters.
    mask_text: Masks all text except spaces.
"""

CHAR = "•"

def mask_email(email: str) -> str:
    local, domain = email.split("@")
    masked = CHAR * len(local)
    return masked + "@" + domain


def mask_username(username: str) -> str:
    if "@" in username:
        return mask_email(username)

    masked = CHAR * len(username[3:])
    return username[:3] + masked


def mask_password(passsword: str) -> str:
    return CHAR * len(passsword)


def mask_number(number: str) -> str:
    if len(number) > 10:
        masked = CHAR * len(number[:-4])
        return masked + number[-4:]

    return CHAR * len(number)


def mask_phone(phone: str) -> str:
    masked = CHAR * len(phone[:-3])
    return masked + phone[-3:]


def mask_text(text: str) -> str:
    masked = ""
    for char in text:
        if char == " ":
            masked += " "
        else:
            masked += CHAR

    if len(masked) > 120:
        return masked[:120] + "..."

    return masked

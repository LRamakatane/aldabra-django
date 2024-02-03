#!/usr/bin/env python3
"""Patient Validators"""


def validate_phone(data: dict):
    pass


def validate_email(data: dict):
    pass


def validate_address(data: dict):
    pass


def validate_contact(data: dict):
    try:
        validate_phone(data)
        validate_email(data)
        validate_address(data)
    except Exception as error:
        raise error


def validate_name(data: dict):
    pass

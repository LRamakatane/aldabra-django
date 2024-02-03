#!/usr/bin/env python3
"""Medical Record Validators"""


def validate_date_time():
    pass


def validate_provider():
    pass


def validate_chief_complaint():
    pass


def validate_diagnosis():
    pass


def validate_procedures():
    pass


def validate_medications():
    pass


def validate_encounters(data: dict):
    try:
        validate_date_time(data)
        validate_provider(data)
        validate_chief_complaint(data)
        validate_diagnosis(data)
        validate_procedures(data)
        validate_medications(data)
    except Exception as error:
        raise error


def validate_medical_history(data: dict):
    pass

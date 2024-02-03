#!/usr/bin/env python3
"""Default Data for JSON Fields"""


def default_name():
    return {
        "titles": "Dr",
        "first_name": "Aaron",
        "last_name": "Ahmid",
        "other_names": "Abiodun",
    }


def default_contact():
    return {
        "phone": "123-456-7890",
        "email": "john.doe@email.com",
        "address": {
            "street_lines": [
                "123 Main St",
            ],
            "city": "Anytown",
            "state": "CA",
            "zip": "12345",
        },
    }


def default_encounter():
    return [
        {
            "date": "2023-01-15",
            "provider": {
                "hospital": {"id": 1, "name": "St Ives"},
                "doctor": {"id": 1, "name": "Dr Smith"},
            },
            "chief_complaint": "Cough and fever",
            "diagnosis": "Upper Respiratory Infection",
            "procedures": ["Physical Examination", "Prescribed antibiotics"],
            "medications": [
                {
                    "name": "Amoxicillin",
                    "dosage": "500mg",
                    "frequency": "Twice a day",
                    "start_date": "2023-01-15",
                }
            ],
        }
    ]


def default_medical_history():
    return {"conditions": ["Hypertension"], "surgeries": ["Appendectomy"]}

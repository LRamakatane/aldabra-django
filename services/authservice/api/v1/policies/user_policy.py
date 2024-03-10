#!/usr/bin/env python
""" access control user policies
"""
from typing import List
from rest_access_policy.access_policy import AccessPolicy


class UserAccesPolicy(AccessPolicy):
    """Defines access policy for users"""

    statements: List[dict]
    statements = [
        {
            "action": ["create"],
            "principal": ["*"],
            "effect": "allow",
        },
        {
            "action": ["list"],
            "principal": ["*"],
            "effect": "allow",
        },
        {
            "action": [
                "reset_password",
                "change_password",
                "update",
                "destroy",
                "retrieve"
            ],
            "principal": ["*"],
            "effect": "allow",
            "condition": ["is_user"],
        }
    ]

    def is_user(self, request, view, action: list) -> bool:
        """Is this the user"""
        try:
            user = view.get_object()
        except AssertionError:
            return False
        return user == request.user

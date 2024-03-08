"""role.py
Module description goes here

Classes
-------
   -- Role class
"""

from django.db import models


class Role(models.Model):
    """Data Model for Manager
    ...
    Attributes
    ----------
    name:            char
    system:          ForeignKey

    Methods
    -------
    save:            saves object
    __str__:         Prints the manager's last_name
    """

    name = models.CharField(max_length=45, unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

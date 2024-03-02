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

    def __str__(self):
        return self.name


from django.db import IntegrityError, connections
from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from services.exceptions.errors import (
    ObjectAlreadyExistError,
    ObjectNotFoundError
)


def set_rollback():
    for db in connections.all():
        if db.settings_dict['ATOMIC_REQUESTS'] and db.in_atomic_block:
            db.set_rollback(True)


def exception_handler(exc, context=None):
    """
    Returns the response that should be used for any given exception.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    print(type(exc))
    if isinstance(exc, Http404):
        exc = ObjectNotFoundError()
    elif isinstance(exc, exceptions.PermissionDenied):
        exc = exceptions.PermissionDenied()
    elif isinstance(exc, IntegrityError):
        exc = ObjectAlreadyExistError()

    print(exc, 'except handler')
    if isinstance(exc, exceptions.APIException):
        print('in except handler')
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = {'detail': exc.get_full_details()}
        else:
            data = {'detail': exc.get_full_details()}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None

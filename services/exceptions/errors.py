from rest_framework.exceptions import APIException, ValidationError
from .base import TPLException, PackageValidationError, InvoiceValidationError


class LocationNotFound(TPLException):
    status_code = 404

    def __init__(self, detail=None, code=None, tpl=None):
        default_detail = "Location not found."
        default_code = "LOCATION.NOT.FOUND"

        detail = detail if detail is not None else default_detail
        code = f"{default_code}.{code}" if code is not None else default_code
        super().__init__(detail=detail, code=code)


class CannotDestroyResource(APIException):
    status_code = 403
    default_detail = "resource cannot be destroyed"
    default_code = "CANNOT.DESTROY"

    def __init__(self, detail=None, code=None):
        detail = detail if detail is not None else self.default_detail
        code = f"{self.default_code}.{code}" if code is not None else self.default_code
        super().__init__(detail=detail, code=code)


class EmployeeNotFound(APIException):
    status_code = 403
    default_detail = "Access Denied: This user may not be an employee"
    default_code = "ACCESS.DENIED.EMPLOYEE.NOT.FOUND"

    def __init__(self, detail=None, code=None):
        detail = detail if detail is not None else self.default_detail
        code = f"{self.default_code}.{code}" if code is not None else self.default_code
        super().__init__(detail=detail, code=code)


class PackageCommodityError(PackageValidationError):
    def __init__(self, detail=None, code=None):
        default = "COMMODITY"
        code = f"{default}.{code}" if code is not None else default
        super().__init__(detail=detail, code=code)


class PackageWeightError(PackageValidationError):
    def __init__(self, detail=None, code=None):
        default = "WEIGHT"
        code = f"{default}.{code}" if code is not None else default
        super().__init__(detail=detail, code=code)


class PackageItemError(PackageValidationError):
    def __init__(self, detail=None, code=None):
        default = "ITEM"
        code = f"{default}.{code}" if code is not None else default
        super().__init__(detail=detail, code=code)


class AddonItemError(PackageValidationError):
    def __init__(self, detail=None, code=None):
        default = "ADDON.ITEM"
        code = f"{default}.{code}" if code is not None else default
        super().__init__(detail=detail, code=code)


class InvoicePaymentError(InvoiceValidationError):
    status_code = 400

    def __init__(self, detail=None, code=None):
        default_detail = "Invoice payment error."
        default_code = "PAYMENT"

        detail = detail if detail is not None else default_detail
        code = f"{default_code}.{code}" if code is not None else default_code
        super().__init__(detail=detail, code=code)


class ServiceUnavailable(APIException):
    status_code = 500
    default_detail = "service is down unavailable"
    default_code = "SERVICE.UNAVAILABLE"

    def __init__(self, detail=None, code=None):
        detail = detail if detail is not None else self.default_detail
        code = f"{self.default_code}.{code}" if code is not None else self.default_code
        super().__init__(detail=detail, code=code)


class TPLNotSupported(TPLException):
    """TPL not supported"""

    status_code = 409
    default_detail = "tpl is not supported"
    default_code = "NOT.SUPPORTED"

    def __init__(self, tpl):
        detail = self.default_detail.replace("tpl", tpl)
        code = self.default_code
        super().__init__(detail=detail, code=code)


class ObjectAlreadyExistError(APIException):
    status_code = 409
    default_detail = "Object already exists"
    default_code = "OBJECT.ALREADY.EXISTS"

    def __init__(self, detail=None, code=None):
        detail = detail if detail is not None else self.default_detail
        code = f"{self.default_code}.{code}" if code is not None else self.default_code
        super().__init__(detail=detail, code=code)


class ObjectNotFoundError(APIException):
    status_code = 404
    default_detail = "Object could not be found"
    default_code = "NOT.FOUND"

    def __init__(self, detail=None, code=None):
        detail = detail if detail is not None else self.default_detail
        code = f"{code}.{self.default_code}" if code is not None else self.default_code
        super().__init__(detail=detail, code=code)


class FedexException(TPLException):
    """Exception raised for errors in the FedEx requests and responses

    Attributes:
        response -- input bad FedEx response
    """

    def __init__(self, detail=None, code=None, status_code=None):
        default = "FEDEX"
        self.status_code = status_code if status_code is not None else self.status_code
        codes = {
            400: "VALIDATION.ERROR",
            401: "AUTHENTICATION.ERROR",
            404: "RESOURCE.NOT.FOUND",
            499: "CLIENT.CLOSED",
            422: "UNPROCESSABLE.CONTENT",
            503: "SERVICE.UNAVAILABLE",
        }
        detail = detail if detail is not None else self.default_detail
        code = (
            f"{default}.{code}"
            if code is not None
            else f"{default}.{codes.get(status_code, 'SERVICE.UNAVAILABLE')}"
        )
        super().__init__(detail=detail, code=code)


class AddressValidationError(ValidationError):
    def __init__(self, detail=None, code=None):
        default = "ORDER.ADDRESS"
        code = f"{default}.{code}" if code is not None else "ORDER.ADDRESS.INVALID"
        super().__init__(detail, code=code)


class UPSException(TPLException):
    """Exception raised for errors in the UPS requests and responses

    Attributes:
        response -- input bad UPS response
    """

    def __init__(self, detail=None, code=None, status_code=None):
        default = "UPS"
        self.status_code = status_code if status_code is not None else self.status_code
        codes = {
            400: "VALIDATION.ERROR",
            401: "AUTHENTICATION.ERROR",
            404: "RESOURCE.NOT.FOUND",
            499: "CLIENT.CLOSED",
            422: "UNPROCESSABLE.CONTENT",
            503: "SERVICE.UNAVAILABLE",
        }
        detail = detail if detail is not None else self.default_detail
        code = (
            f"{default}.{code}"
            if code is not None
            else f"{default}.{codes.get(status_code, 'SERVICE.UNAVAILABLE')}"
        )
        super().__init__(detail=detail, code=code)


class DHLException(TPLException):
    """Exception raised for errors in the DHL requests and responses

    Attributes:
        response -- input bad DHL response
    """

    def __init__(self, detail=None, code=None, status_code=None):
        default = "DHL"
        self.status_code = status_code if status_code is not None else self.status_code
        codes = {
            400: "VALIDATION.ERROR",
            401: "AUTHENTICATION.ERROR",
            404: "RESOURCE.NOT.FOUND",
            499: "CLIENT.CLOSED",
            422: "UNPROCESSABLE.CONTENT",
            503: "SERVICE.UNAVAILABLE",
        }
        detail = detail if detail is not None else self.default_detail
        code = (
            f"{default}.{code}"
            if code is not None
            else f"{default}.{codes.get(status_code, 'SERVICE.UNAVAILABLE')}"
        )
        super().__init__(detail=detail, code=code)


class QuoteValidationError(ValidationError):
    # status_code = 400
    default_detail = "quote data is in invalid"
    default_code = "QUOTE.VALIDATION.ERROR"

    def __init__(self, detail=None, code=None):
        detail = detail if detail is not None else self.default_detail
        code = f"{self.default_code}.{code}" if code is not None else self.default_code
        print(detail)
        super().__init__(detail, code=code)


class InvalidShipmentID(ValidationError):
    # status_code = 400
    default_detail = "Invalid Shipment ID"
    default_code = "SHIPMENT.ID.INVALID"

    def __init__(self, detail=None, code=None):
        detail = detail if detail is not None else self.default_detail
        code = f"{code}" if code is not None else self.default_code
        super().__init__(detail, code=code)


class UnprocessableContent(APIException):
    status_code = 422
    default_detail = "could not process content"
    default_code = "UNPROCESSABLE.CONTENT"

    def __init__(self, detail=None, code=None):
        detail = detail if detail is not None else self.default_detail
        code = f"{self.default_code}.{code}" if code is not None else self.default_code
        super().__init__(detail=detail, code=code)


class APIClientException(APIException):
    default_detail = "an exception occurred while trying the request"
    default_code = "CLIENT.ERROR"

    def __init__(self, detail=None, code=None, status_code=None):
        print(detail, status_code, "In here")
        print("in handler!!!!!!!!!!!")
        self.status_code = status_code if status_code is not None else self.status_code
        detail = detail if detail is not None else self.default_detail
        code = f"{self.default_code}.{code}" if code is not None else self.default_code
        super().__init__(detail=detail, code=code)

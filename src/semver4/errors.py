class BaseError(Exception): ...

class InvalidVersionError(BaseError): ...
class InvalidVersionPartError(InvalidVersionError): ...

class NotComparableError(BaseError): ...
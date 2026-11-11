"""Error types shared across business capabilities."""
class DomainError(Exception): pass
class NotFound(DomainError): pass
class InvalidRequest(DomainError): pass
class Conflict(DomainError): pass
class PaymentDeclined(DomainError): pass

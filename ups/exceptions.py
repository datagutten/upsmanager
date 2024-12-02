class UPSError(RuntimeError):
    pass


class UPSTimeout(UPSError):
    pass


class UPSAuthenticationError(UPSError):
    pass


class UnsupportedUPSVendor(UPSError):
    pass

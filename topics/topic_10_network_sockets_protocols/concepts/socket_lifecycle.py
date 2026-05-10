"""Socket endpoint parsing helpers."""
def parse_endpoint(endpoint):
    host, sep, port = endpoint.partition(":")
    if not sep or not host or not port.isdigit():
        raise ValueError("endpoint must look like host:port")
    return host, int(port)

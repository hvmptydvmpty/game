def application(environ, start_response):
    method, path, protocol, wsgi_version, wsgi_input = (
        environ[var] for var in "REQUEST_METHOD PATH_INFO SERVER_PROTOCOL wsgi.version wsgi.input".split()
    )
    ctype, clength, cookie = (environ.get(var, "") for var in "CONTENT_TYPE CONTENT_LENGTH HTTP_Cookie".split())
    clength = int(clength) if clength else 0

    assert (1, 0) <= wsgi_version, f"WSGI 1.0 or later required, actual {wsgi_version}"

    if 16384 < clength:
        status, output = "413 Payload Too Large", ""
    else:
        status = "200 OK"
        output = f"""
WSGI version: {wsgi_version}

{method} {path}
Proto: {protocol}
Cookie: {cookie}
"""

    response_headers = [
        ('Content-Length', str(len(output))),
        ('Content-Type', 'text/plain'),
    ]

    start_response(status, response_headers)
    return [bytes(output, 'utf-8')]

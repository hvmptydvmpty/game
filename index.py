import http.cookies
import re
import uuid

NODE_COOKIE = "game_node_id"

PATH_PATTERN = re.compile(r"^/(?P<resource>session|sessions)(?:/(?P<id>\w+))?$", re.IGNORECASE)

def application(environ, start_response):
    # mandatory variables
    method, path, protocol, wsgi_version, wsgi_input = (
        environ[var] for var in "REQUEST_METHOD PATH_INFO SERVER_PROTOCOL wsgi.version wsgi.input".split()
    )
    # optional variables
    ctype, clength, query, cookies = (
        environ.get(var, "") for var in "CONTENT_TYPE CONTENT_LENGTH QUERY_STRING HTTP_COOKIE".split()
    )
    clength = int(clength) if clength else 0
    cookies = http.cookies.SimpleCookie(cookies)

    assert (1, 0) <= wsgi_version, f"WSGI 1.0 or later required, actual {wsgi_version}"

    node_id = uuid.UUID(cookies[NODE_COOKIE].value[:36]) if NODE_COOKIE in cookies else uuid.uuid1()

    if 16384 < clength:
        status, output = "413 Payload Too Large", ""
    else:
        match = PATH_PATTERN.match(path)
        if not match:
            status, output = "404 Not Found", "POST /sessions to get new one then GET or PUT /session/NNN to manipulate"
        else:
            resource = match.group("resource")
            handler = globals().get(f"{method}_{resource}".lower())
            if not callable(handler):
                status, output = "405 Method Not Allowed", ""
            else:
                content = wsgi_input.read(clength) if clength else b''
                status, output = handler(match.group("id"), content, node_id)

    response_headers = [
        ("Access-Control-Allow-Origin", "*"),
        ("Allow", "GET, POST, PUT"),
        ('Content-Length', str(len(output))),
        ('Content-Type', 'text/plain; charset=UTF-8'),
        ("Cross-Origin-Resource-Policy", "cross-origin"),
    ]
    if NODE_COOKIE not in cookies:
        response_headers.append(
            ("Set-Cookie", f"{NODE_COOKIE}={node_id}; Domain=optimaltec.com; HttpOnly; Path=/game; Secure")
        )

    start_response(status, response_headers)
    return [bytes(output, 'utf-8')]

def get_sessions(resource_id, content, node_id):
    if resource_id:
        return "400 Bad Request", "Resource id not allowed"

    return "200 OK", "List sessions: working on it..."

def post_sessions(resource_id, content, node_id):
    if resource_id:
        return "400 Bad Request", "Resource id not allowed"

    return "200 OK", "New session: working on it..."

def get_session(resource_id, content, node_id):
    if not resource_id:
        return "400 Bad Request", "Requires resource id"

    return "200 OK", f"Get session {resource_id}: working on it..."

def put_session(resource_id, content, node_id):
    if not resource_id:
        return "400 Bad Request", "Requires resource id"

    return "200 OK", f"Put session {resource_id}: working on it..."

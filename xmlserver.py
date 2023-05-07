from http.server import HTTPServer, BaseHTTPRequestHandler
import xml.dom.minidom

host = ""
port = 8080

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def add(x):
    return(x)

class XMLServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(405)
    
    def do_PUT(self):
        self.send_response(405)
    
    def do_DELETE(self):
        self.send_response(405)
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        xml_data = xml.dom.minidom.parseString(post_data)

        # Get method and parameters
        method = xml_data.getElementsByTagName("methodName")
        for i in method:
            method_name = getText(i.childNodes)
        print(method_name)
        params_node = xml_data.getElementsByTagName("i4")
        params = []
        for i in params_node:
            params.append(getText(i.childNodes))

        # math operations
        if method_name == "add":
            params_int = [int(i) for i in params]
            result = sum(params_int)
        elif method_name == "subtract":
            params_int = [int(i) for i in params]
            result = params_int[0] - sum(params_int[1:])
        elif method_name == "multiply":
            params_int = [int(i) for i in params]
            result = 1
            for p in params_int:
                result *= p
        elif method_name == "divide":
            params_int = [int(i) for i in params]
            result = params_int[0]
            for d in params_int[1:]:
                result //= d
        elif method_name == "modulo":
            params_int = [int(i) for i in params]
            result = params_int[0] % params_int[1]
        else:
            # Handle unknown method
            response_str = xml_data.toprettyxml()
            print(response_str)
            self.send_response(400)
            self.send_header("Content-type", "application/xml")
            self.end_headers()
            self.wfile.write(response_str.encode('utf-8'))
            return

        # Construct response
        response_str = """
            <?xml version="1.0"?>
            <methodResponse>
                <params>
                    <param>
                        <value><i4>{}</i4></value>
                    </param>
                </params>
            </methodResponse>
        """.format(result)

        self.send_response(200)
        self.send_header("Content-type", "application/xml")
        self.end_headers()
        self.wfile.write(response_str.encode('utf-8'))





server = HTTPServer((host, port), XMLServer)
print("Starting server...")
server.serve_forever()
server.server_close()
print("Stopping server...")
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

        # Handle math operations and exceptions
        try:
            if method_name == "add":
                params_int = [int(i) for i in params]
                # Check for overflow before performing the addition
                if any(p > (10**9 - sum(params_int[:idx])) for idx, p in enumerate(params_int, start=1)):
                    raise OverflowError("Overflow fault")
                result = sum(params_int)
            elif method_name == "subtract":
                if len(params) != 2 or not params[0].isdigit() or not params[1].isdigit():
                    raise ValueError("Illegal argument fault")
                params_int = [int(i) for i in params]
                result = params_int[0] - sum(params_int[1:])
            elif method_name == "multiply":
                params_int = [int(i) for i in params]
                result = 1
                for p in params_int:
                    result *= p
                # Check for overflow
                if result > 10**9:
                    raise OverflowError("Overflow fault")
            elif method_name == "divide":
                if len(params) != 2 or not params[0].isdigit() or not params[1].isdigit():
                    raise ValueError("Illegal argument fault")
                params_int = [int(i) for i in params]
                dividend, divisor = params_int[0], params_int[1]
                if divisor == 0:
                    raise ZeroDivisionError("Divide-by-zero fault")
                result = dividend // divisor
            elif method_name == "modulo":
                if len(params) != 2 or not params[0].isdigit() or not params[1].isdigit():
                    raise ValueError("Illegal argument fault")
                params_int = [int(i) for i in params]
                dividend, divisor = params_int[0], params_int[1]
                if divisor == 0:
                    raise ZeroDivisionError("Divide-by-zero fault")
                result = dividend % divisor
            else:
                raise ValueError("Unknown method")

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

            print(response_str)
            self.send_response(200)
            self.send_header("Content-type", "application/xml")
            self.end_headers()
            self.wfile.write(response_str.encode('utf-8'))

        except ValueError as e:
                    # Handle illegal argument fault
                    response_str = """
                        <?xml version="1.0"?>
                        <methodResponse>
                            <fault>
                                <value>
                                    <struct>
                                        <member>
                                            <name>faultCode</name>
                                            <value><int>400</int></value>
                                        </member>
                                        <member>
                                            <name>faultString</name>
                                            <value><string>{}</string></value>
                                        </member>
                                    </struct>
                                </value>
                            </fault>
                        </methodResponse>
                    """.format(str(e))

                    print(response_str)
                    self.send_response(400)
                    self.send_header("Content-type", "application/xml")
                    self.end_headers()
                    self.wfile.write(response_str.encode('utf-8'))

        except ZeroDivisionError as e:
            # Handle divide-by-zero fault
            response_str = """
                <?xml version="1.0"?>
                <methodResponse>
                    <fault>
                        <value>
                            <struct>
                                <member>
                                    <name>faultCode</name>
                                    <value><int>400</int></value>
                                </member>
                                <member>
                                    <name>faultString</name>
                                    <value><string>{}</string></value>
                                </member>
                            </struct>
                        </value>
                    </fault>
                </methodResponse>
            """.format(str(e))

            print(response_str)
            self.send_response(400)
            self.send_header("Content-type", "application/xml")
            self.end_headers()
            self.wfile.write(response_str.encode('utf-8'))

        except OverflowError as e:
            # Handle overflow fault
            response_str = """
                <?xml version="1.0"?>
                <methodResponse>
                    <fault>
                        <value>
                            <struct>
                                <member>
                                    <name>faultCode</name>
                                    <value><int>400</int></value>
                                </member>
                                <member>
                                    <name>faultString</name>
                                    <value><string>{}</string></value>
                                </member>
                            </struct>
                        </value>
                    </fault>
                </methodResponse>
            """.format(str(e))

            print(response_str)
            self.send_response(400)
            self.send_header("Content-type", "application/xml")
            self.end_headers()
            self.wfile.write(response_str.encode('utf-8'))

        except Exception as e:
            # Handle unknown method fault
            response_str = xml_data.toprettyxml()
            print(response_str)
            self.send_response(400)
            self.send_header("Content-type", "application/xml")
            self.end_headers()
            self.wfile.write(response_str.encode('utf-8'))

# Create and start the server
server = HTTPServer((host, port), XMLServer)
print("Starting server...")
server.serve_forever()
server.server_close()
print("Stopping server...")
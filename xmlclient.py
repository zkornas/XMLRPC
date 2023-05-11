import xml.etree.ElementTree as ET
import xml.dom.minidom
import requests

headers = {'Content-type': 'application/xml'}
url = 'http://localhost:8080'

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def helper(method, *args):
    xml_params = ''.join([f'<i4>{arg}</i4>' for arg in args])
    xml_data = f'''
    <?xml version="1.0"?>
    <methodCall>
        <methodName>{method}</methodName>
        <params>
            <param>
                <value>{xml_params}</value>
            </param>
        </params>
    </methodCall>
    '''
    response = requests.post(url, headers=headers, data=xml_data.strip())
    response_str = response.content.decode('utf-8').strip()
    xml_response = xml.dom.minidom.parseString(response_str)
    fault_code_node = xml_response.getElementsByTagName("struct")
    if fault_code_node:
        fault_code = xml_response.getElementsByTagName("int")[0].childNodes[0].nodeValue
        fault_string = xml_response.getElementsByTagName("string")[0].childNodes[0].nodeValue
        raise Exception(f"Fault Code: {fault_code}, Fault String: {fault_string}")
    else:
        ans = xml_response.getElementsByTagName("i4")[0].childNodes[0].nodeValue
        return int(ans)

def add(*args):
    try:
        return helper("add", *args)
    except Exception as e:
        print(f"Exception occurred: {e}")

def subtract(*args):
    try:
        return helper("subtract", *args)
    except Exception as e:
        print(f"Exception occurred: {e}")

def multiply(*args):
    try:
        return helper("multiply", *args)
    except Exception as e:
        print(f"Exception occurred: {e}")

def divide(*args):
    try:
        return helper("divide", *args)
    except Exception as e:
        print(f"Exception occurred: {e}")

def modulo(*args):
    try:
        return helper("modulo", *args)
    except Exception as e:
        print(f"Exception occurred: {e}")


print(add() == 0)
print(add(1, 2, 3, 4, 5) == 15)
print(add(2, 4) == 6)
print(subtract(12, 6) == 6)
print(multiply(3, 4) == 12)
print(multiply(1, 2, 3, 4, 5) == 120)
print(divide(10, 5) == 2)
print(modulo(10, 5) == 0)
print(f'\n')

#exceptions
print(multiply(1000000, 100000))
print(subtract('twelve', 'six'))
print(divide(10, 0))
print(add(9999999999999, 99999999999))


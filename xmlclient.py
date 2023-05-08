import xml.etree.ElementTree as ET
import xml.dom.minidom
import requests

headers = {'Content-type': 'application/xml'}
url = 'http://localhost:8080'

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
    ans = xml_response.getElementsByTagName("i4")[0].childNodes[0].nodeValue
    return int(ans)

def add(*args):
    return(helper("add", *args))

def subtract(*args):
    return(helper("subtract", *args))

def multiply(*args):
    return(helper("multiply", *args))

def divide(*args):
    return(helper("divide", *args))

def modulo(*args):
    return(helper("modulo", *args))


print(add() == 0)
print(add(1, 2, 3, 4, 5) == 15)
print(add(2, 4) == 6)
print(subtract(12, 6) == 6)
print(multiply(3, 4) == 12)
print(multiply(1, 2, 3, 4, 5) == 120)
print(divide(10, 5) == 2)
print(modulo(10, 5) == 0)
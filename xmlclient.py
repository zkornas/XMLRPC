import xml.etree.ElementTree as ET
import requests

headers = {'Content-type': 'application/xml'}
url = 'http://localhost:8080'

def add(*args):
    xml_params = ''.join([f'<i4>{arg}</i4>' for arg in args])
    xml_data = f'''
    <?xml version="1.0"?>
    <methodCall>
        <methodName>add</methodName>
        <params>
            <param>
                <value>{xml_params}</value>
            </param>
        </params>
    </methodCall>
    '''
    response = requests.post(url, headers=headers, data=xml_data)
    return response.content.decode('utf-8')
    #print(xml_data)

print(add(2, 4) == '6')

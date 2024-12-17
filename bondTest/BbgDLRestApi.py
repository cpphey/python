from flask import Flask, request, jsonify
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Bloomberg Data License API credentials and endpoint
BLOOMBERG_API_URL = "https://example.bloombergapi.com/data-license"
BLOOMBERG_USERNAME = "your_username"
BLOOMBERG_PASSWORD = "your_password"
BLOOMBERG_FIELDS = ["YLD_YTM_MID"]


# Function to create Bloomberg request XML
def create_request_xml(cusip):
    request_template = f"""
    <Request>
        <Header>
            <Username>{BLOOMBERG_USERNAME}</Username>
            <Password>{BLOOMBERG_PASSWORD}</Password>
        </Header>
        <Instrument>
            <Identifier>{cusip}</Identifier>
            <IdentifierType>CUSIP</IdentifierType>
        </Instrument>
        <Fields>
            {''.join(f'<Field>{field}</Field>' for field in BLOOMBERG_FIELDS)}
        </Fields>
    </Request>
    """
    return request_template


# Function to send request to Bloomberg Data License API
def query_bloomberg(cusip):
    headers = {'Content-Type': 'application/xml'}
    request_xml = create_request_xml(cusip)

    # Send POST request to Bloomberg API
    response = requests.post(BLOOMBERG_API_URL, headers=headers, data=request_xml)

    if response.status_code == 200:
        return parse_response_xml(response.content)
    else:
        return {"error": f"Failed to retrieve data. Status Code: {response.status_code}"}


# Function to parse Bloomberg API response XML
def parse_response_xml(response_xml):
    root = ET.fromstring(response_xml)
    data = {}

    for field in BLOOMBERG_FIELDS:
        field_element = root.find(f".//Field[@name='{field}']")
        if field_element is not None:
            data[field] = field_element.text
        else:
            data[field] = None

    return data


# REST endpoint to query Bloomberg YLD_YTM_MID@app.route('/get_yield', methods=['POST'])
def get_yield():
    try:
        request_data = request.get_json()
        cusip = request_data.get('cusip')

        if not cusip:
            return jsonify({"error": "CUSIP is required"}), 400

        result = query_bloomberg(cusip)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

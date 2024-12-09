from flask import Flask, request, jsonify
import json
import hl7
import xml.etree.ElementTree as ET
from fhir.resources.patient import Patient

app = Flask(__name__)

# Function to detect format
def detect_format(data):
    if data.strip().startswith("MSH"):  # HL7 detection
        return "HL7"
    try:
        json_data = json.loads(data)
        if "resourceType" in json_data:  # FHIR detection
            return "FHIR"
        elif "hospitalName" in json_data:  # EHR JSON detection
            return "EHR_JSON"
    except json.JSONDecodeError:
        pass
    if "<" in data and ">" in data:  # XML detection
        return "XML"
    if ":" in data:  # Plain text detection
        return "PlainText"
    return "Unknown"

# Function to create a custom JSON structure
def create_custom_json(resource_type, status, hospital_value, person_data, additional_fields=None):
    return {
        "resourceType": resource_type,
        "text": {"status": status},
        "hospital": {"identifier": {"value": hospital_value}},
        "person": {
            "firstName": person_data.get("firstName", "Unknown"),
            "lastName": person_data.get("lastName", "Unknown"),
            "gender": person_data.get("gender", "Unknown"),
            "DOB": person_data.get("DOB", "Unknown"),
            "Vitals": person_data.get("Vitals", "Unknown"),
        },
        "relatedFields": additional_fields if additional_fields else {}
    }

# Function to parse HL7 data
def parse_hl7(hl7_message):
    segments = hl7_message.strip().splitlines()
    hl7_data = {}
    for segment in segments:
        fields = segment.split('|')
        segment_name = fields[0]
        if segment_name not in hl7_data:
            hl7_data[segment_name] = []
        segment_dict = {f"{segment_name}_{i}": fields[i] for i in range(len(fields))}
        hl7_data[segment_name].append(segment_dict)

    person_data = {
        "firstName": hl7_data.get("PID", [{}])[0].get("PID_5", "Unknown").split("^")[1],
        "lastName": hl7_data.get("PID", [{}])[0].get("PID_5", "Unknown").split("^")[0],
        "gender": hl7_data.get("PID", [{}])[0].get("PID_8", "Unknown"),
        "DOB": hl7_data.get("PID", [{}])[0].get("PID_7", "Unknown"),
        "Vitals": hl7_data.get("OBX", [{}])[0].get("OBX_5", "Unknown"),
    }
    additional_fields = {key: value for key, value in hl7_data.items() if key not in ["PID", "OBX"]}

    return create_custom_json("HL7", "generated", hl7_data.get("MSH", [{}])[0].get("MSH_3", "Unknown"), person_data, additional_fields)

# Function to parse FHIR data
def parse_fhir(fhir_message):
    fhir_json = json.loads(fhir_message)
    resource_type = fhir_json.get("resourceType", "Unknown")
    person_data = {
        "firstName": fhir_json.get("name", [{}])[0].get("given", ["Unknown"])[0],
        "lastName": fhir_json.get("name", [{}])[0].get("family", "Unknown"),
        "gender": fhir_json.get("gender", "Unknown"),
        "DOB": fhir_json.get("birthDate", "Unknown"),
        "Vitals": "Normal",  # Adjust if FHIR has a vitals field
    }
    additional_fields = {key: value for key, value in fhir_json.items() if key not in ["resourceType", "name", "gender", "birthDate"]}

    return create_custom_json(resource_type, "generated", "FHIR Hospital", person_data, additional_fields)

# Function to parse EHR JSON
def parse_ehr(ehr_message):
    ehr_json = json.loads(ehr_message)
    person_data = {
        "firstName": ehr_json.get("patient", {}).get("patientName", {}).get("given", "Unknown"),
        "lastName": ehr_json.get("patient", {}).get("patientName", {}).get("family", "Unknown"),
        "gender": ehr_json.get("patient", {}).get("gender", "Unknown"),
        "DOB": ehr_json.get("patient", {}).get("birthDate", "Unknown"),
        "Vitals": "Not Provided",
    }
    additional_fields = {key: value for key, value in ehr_json.get("patient", {}).items() if key not in ["patientName", "gender", "birthDate"]}

    return create_custom_json("EHR_JSON", "generated", ehr_json.get("hospitalName", "Unknown"), person_data, additional_fields)

# Function to parse XML data
def parse_xml(xml_message):
    root = ET.fromstring(xml_message)

    def safe_find_text(node, path, default="Unknown"):
        """Safely find text for a tag in an XML node."""
        found = node.find(path)
        return found.text if found is not None else default

    person_data = {
        "firstName": safe_find_text(root, "patient/patientName/given", "Unknown"),
        "lastName": safe_find_text(root, "patient/patientName/family", "Unknown"),
        "gender": safe_find_text(root, "patient/gender", "Unknown"),
        "DOB": safe_find_text(root, "patient/birthDate", "Unknown"),
        "Vitals": safe_find_text(root, "patient/vitals", "Not Provided")
    }

    hospital_value = safe_find_text(root, "hospitalName", "Unknown")

    # Dynamically extract all additional fields under <patient>
    additional_fields = {}
    for section in root.findall("patient/*"):
        if section.tag not in ["patientName", "gender", "birthDate"]:  # Exclude already processed fields
            additional_fields[section.tag] = parse_additional_fields(section)

    return create_custom_json(
        resource_type="EHR_XML",
        status="generated",
        hospital_value=hospital_value,
        person_data=person_data,
        additional_fields=additional_fields,
    )

def parse_additional_fields(section):
    """Recursively parse additional fields in the XML."""
    if len(section) == 0:  # Leaf node
        return section.text
    result = {}
    for child in section:
        result[child.tag] = parse_additional_fields(child)
    return result

# Function to parse plain text
def parse_plain_text(plain_text):
    lines = plain_text.strip().splitlines()
    data = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            data[key.strip()] = value.strip()

    person_data = {
        "firstName": data.get("FirstName", "Unknown"),
        "lastName": data.get("LastName", "Unknown"),
        "gender": data.get("Gender", "Unknown"),
        "DOB": data.get("DOB", "Unknown"),
        "Vitals": data.get("Vitals", "Unknown"),
    }
    additional_fields = {key: value for key, value in data.items() if key not in ["FirstName", "LastName", "Gender", "DOB", "Vitals"]}

    return create_custom_json("PlainText", "generated", data.get("Hospital", "Unknown"), person_data, additional_fields)

@app.route('/convert', methods=['POST'])
def convert_to_custom_json():
    try:
        message = request.data.decode('utf-8')
        format_type = detect_format(message)

        if format_type == "HL7":
            json_output = parse_hl7(message)
        elif format_type == "FHIR":
            json_output = parse_fhir(message)
        elif format_type == "EHR_JSON":
            json_output = parse_ehr(message)
        elif format_type == "XML":
            json_output = parse_xml(message)
        elif format_type == "PlainText":
            json_output = parse_plain_text(message)
        else:
            return jsonify({"error": f"Unsupported format: {format_type}"}), 400

        return jsonify(json_output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
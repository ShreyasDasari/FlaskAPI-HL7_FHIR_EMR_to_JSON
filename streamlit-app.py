import streamlit as st
import json
import xml.etree.ElementTree as ET
import hl7  # For HL7 parsing
from fhir.resources.patient import Patient  # For handling FHIR resources


# Helper function to create custom JSON
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

# Parsing functions for each format
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

def parse_fhir(fhir_message):
    fhir_json = json.loads(fhir_message)
    resource_type = fhir_json.get("resourceType", "Unknown")
    person_data = {
        "firstName": fhir_json.get("name", [{}])[0].get("given", ["Unknown"])[0],
        "lastName": fhir_json.get("name", [{}])[0].get("family", "Unknown"),
        "gender": fhir_json.get("gender", "Unknown"),
        "DOB": fhir_json.get("birthDate", "Unknown"),
        "Vitals": "Normal",
    }
    additional_fields = {key: value for key, value in fhir_json.items() if key not in ["resourceType", "name", "gender", "birthDate"]}

    return create_custom_json(resource_type, "generated", "FHIR Hospital", person_data, additional_fields)

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

    additional_fields = {child.tag: child.text for child in root.findall("patient/*") if child.tag not in ["patientName", "gender", "birthDate"]}

    return create_custom_json("EHR_XML", "generated", hospital_value, person_data, additional_fields)

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

# Detect format
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

# Streamlit app
st.title("HealthCare Data Interoperability Wrapper")

# Real-World Impact Section
st.markdown("""
### Real-World Impact
This tool bridges the gap between disparate healthcare systems, enabling seamless data migration during software upgrades or interoperability initiatives. By converting complex formats like HL7, FHIR, XML, and Plain Text into a standardized JSON structure, it ensures:
- **Efficient data exchange** between systems.
- **Improved patient care** with timely access to critical information.
- **Simplified migrations** for hospitals and clinics switching software.
""")

# Input Section
st.subheader("Enter your healthcare data below:")
input_message = st.text_area("Paste data in HL7, FHIR, XML, Plain Text, or EHR JSON format:")

# Convert Button
if st.button("Convert"):
    format_type = detect_format(input_message)
    try:
        if format_type == "HL7":
            result = parse_hl7(input_message)
        elif format_type == "FHIR":
            result = parse_fhir(input_message)
        elif format_type == "EHR_JSON":
            result = parse_ehr(input_message)
        elif format_type == "XML":
            result = parse_xml(input_message)
        elif format_type == "PlainText":
            result = parse_plain_text(input_message)
        else:
            result = {"error": f"Unsupported format: {format_type}"}
        st.json(result)
    except Exception as e:
        st.error(f"Error: {str(e)}")

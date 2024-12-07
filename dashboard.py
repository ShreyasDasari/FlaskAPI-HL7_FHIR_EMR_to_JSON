import streamlit as st
import requests
import json
import xml.etree.ElementTree as ET

# Helper function to detect the format of the input
def detect_format(data):
    if data.strip().startswith("MSH"):  # HL7 detection
        return "HL7"
    try:
        json_data = json.loads(data)
        if "resourceType" in json_data:  # FHIR detection
            return "FHIR"
        elif "EMRType" in json_data or "hospital" in json_data:  # Hypothetical EHR detection
            return "EHR_JSON"
    except json.JSONDecodeError:
        pass
    if "<" in data and ">" in data:  # XML detection
        return "XML"
    if ":" in data:  # Plain text detection
        return "PlainText"
    return "Unknown"

# Streamlit App
st.title("HealthCare Data Interoperability Wrapper")
st.write("Convert HL7, FHIR, EHR (JSON/XML), or Plain Text to a Custom JSON format.")

# Input Fields
input_format = st.selectbox("Select Input Format", ["HL7", "FHIR", "EHR (JSON/XML)", "Plain Text"])
input_message = st.text_area("Enter your message in the selected format:")

if st.button("Convert"):
    # Validate the input format
    detected_format = detect_format(input_message)
    
    # Map the dropdown input format to the expected detected format
    format_mapping = {
        "HL7": "HL7",
        "FHIR": "FHIR",
        "EHR (JSON/XML)": ["EHR_JSON", "XML"],
        "Plain Text": "PlainText"
    }

    if detected_format not in (format_mapping[input_format] if isinstance(format_mapping[input_format], list) else [format_mapping[input_format]]):
        st.error(
            f"Invalid input format! You selected '{input_format}' but provided '{detected_format}'. "
            f"Please correct your input and try again."
        )
    else:
        # Proceed with API call if validation passes
        try:
            response = requests.post("http://127.0.0.1:5000/convert", data=input_message)
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Connection error: {e}")

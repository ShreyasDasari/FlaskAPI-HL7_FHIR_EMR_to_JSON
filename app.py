# from flask import Flask, request, jsonify

# app = Flask(__name__)

# def hl7_to_json(hl7_message):
#     # Split the HL7 message into lines (segments)
#     segments = hl7_message.strip().splitlines()
#     message_json = {}

#     # Manually parse each segment line
#     for segment in segments:
#         # Split each segment by the '|' character to isolate fields
#         fields = segment.split('|')
#         segment_name = fields[0]  # The segment type (e.g., MSH, PID, PV1)
        
#         # Initialize segment list if not already in the message JSON
#         if segment_name not in message_json:
#             message_json[segment_name] = []
        
#         # Convert segment fields to a dictionary, excluding the segment name
#         segment_dict = {f"field_{i}": fields[i] for i in range(len(fields))}
#         message_json[segment_name].append(segment_dict)

#     return message_json

# @app.route('/convert', methods=['POST'])
# def convert_hl7_to_json():
#     try:
#         # Get HL7 message from the request body
#         hl7_message = request.data.decode('utf-8')
        
#         # Convert HL7 to JSON
#         json_output = hl7_to_json(hl7_message)
        
#         return jsonify(json_output), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
import hl7
from fhir.resources.patient import Patient  # Example FHIR resource
import json

app = Flask(__name__)

# Function to detect format
def detect_format(data):
    if data.strip().startswith("MSH"):
        return "HL7"
    try:
        json_data = json.loads(data)
        if "resourceType" in json_data:
            return "FHIR"
        elif "EMRType" in json_data:  # Hypothetical key for EMR format detection
            return "EMR"
    except json.JSONDecodeError:
        pass
    return "Unknown"

# Function to parse HL7 data
def parse_hl7(hl7_message):
    segments = hl7_message.strip().splitlines()
    message_json = {}
    for segment in segments:
        fields = segment.split('|')
        segment_name = fields[0]
        if segment_name not in message_json:
            message_json[segment_name] = []
        segment_dict = {f"field_{i}": fields[i] for i in range(len(fields))}
        message_json[segment_name].append(segment_dict)
    return message_json

# Function to parse FHIR data
def parse_fhir(fhir_message):
    fhir_json = json.loads(fhir_message)
    resource_type = fhir_json["resourceType"]
    if resource_type == "Patient":
        patient = Patient.parse_obj(fhir_json)
        return patient.dict()  # Converts to a JSON-compatible dictionary
    return fhir_json  # Return as-is for other FHIR resources

# Function to parse EMR data
def parse_emr(emr_message):
    emr_json = json.loads(emr_message)
    # Custom processing for EMR data if needed
    return emr_json

@app.route('/convert', methods=['POST'])
def convert_to_json():
    try:
        # Get message from the request
        message = request.data.decode('utf-8')
        
        # Detect the format
        format_type = detect_format(message)
        
        # Parse based on the detected format
        if format_type == "HL7":
            json_output = parse_hl7(message)
        elif format_type == "FHIR":
            json_output = parse_fhir(message)
        elif format_type == "EMR":
            json_output = parse_emr(message)
        else:
            return jsonify({"error": "Unknown format"}), 400
        
        return jsonify({"format": format_type, "data": json_output}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
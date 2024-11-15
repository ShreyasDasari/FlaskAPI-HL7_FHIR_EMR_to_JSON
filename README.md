# FlaskAPI-HL7_FHIR_EMR_to_JSON

# Healthcare Data Format Conversion API

This API is designed to convert various healthcare data formats, such as HL7, FHIR, and EMR, into a standardized JSON format. Built using Flask, it automatically detects the format of incoming data and parses it accordingly, enabling easy interoperability between different healthcare systems.

## Features
- **Format Detection**: Identifies HL7, FHIR, and EMR data formats automatically.
- **Flexible Parsing**: Parses data based on the detected format, converting it into a standardized JSON structure.
- **Extensible**: Additional formats can be added by extending the `detect_format` and parsing functions.

---

## Prerequisites

Make sure you have **Python 3.6+** installed on your machine.

### Install Required Libraries

Use the following command to install the necessary libraries:
```bash
pip install Flask hl7 fhir.resources pydantic
```

- **Flask**: For creating the web API.
- **hl7**: For parsing HL7 data.
- **fhir.resources**: For handling FHIR data.
- **pydantic**: For schema validation in JSON data.

---

## Getting Started

1. **Clone the Repository**  
   Download the API code by cloning the repository or copying the code into a new file.

    ```bash
    git clone <your-repository-url>
    cd healthcare-data-api
    ```

2. **Create the API Script**  
   Save the provided Python code into a file named `app.py` in the repository directory.

3. **Run the API Server**  
   Start the Flask API server by running:

    ```bash
    python app.py
    ```

    By default, the server will run on `http://127.0.0.1:5000`.

---

## API Usage

### Endpoint: `/convert`
- **Method**: `POST`
- **Description**: Accepts healthcare data in HL7, FHIR, or EMR formats and converts it to a standardized JSON format.
- **Content-Type**: `text/plain` or `application/json` (for FHIR or EMR data)

### Request Format

Send a POST request to the `/convert` endpoint with the healthcare data in the request body.

### Example Requests

#### 1. HL7 Format
HL7 messages are sent as plain text. Here’s an example HL7 message:

**HL7 Sample Data**:
```plaintext
MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|202311111200||ADT^A01|123456|P|2.3
PID|1||123456^^^Hospital&1.2.3.4.5&ISO||Doe^John||19800101|M|||123 Main St^^City^State^12345||555-1234|||M|Non-Hispanic|123-45-6789
```

**cURL Request**:
```bash
curl -X POST http://127.0.0.1:5000/convert -H "Content-Type: text/plain" -d "MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|202311111200||ADT^A01|123456|P|2.3\nPID|1||123456^^^Hospital&1.2.3.4.5&ISO||Doe^John||19800101|M|||123 Main St^^City^State^12345||555-1234|||M|Non-Hispanic|123-45-6789"
```

**Expected JSON Output**:
```json
{
  "format": "HL7",
  "data": {
    "MSH": [
      {
        "field_0": "MSH",
        "field_1": "^~\\&",
        "field_2": "SendingApp",
        "field_3": "SendingFacility",
        "field_4": "ReceivingApp",
        "field_5": "ReceivingFacility",
        "field_6": "202311111200",
        "field_8": "ADT^A01",
        "field_9": "123456",
        "field_10": "P",
        "field_11": "2.3"
      }
    ],
    "PID": [
      {
        "field_0": "PID",
        "field_1": "1",
        "field_3": "123456^^^Hospital&1.2.3.4.5&ISO",
        "field_5": "Doe^John",
        "field_7": "19800101",
        "field_8": "M",
        "field_10": "123 Main St^^City^State^12345",
        "field_11": "555-1234",
        "field_14": "M",
        "field_15": "Non-Hispanic",
        "field_16": "123-45-6789"
      }
    ]
  }
}
```

#### 2. FHIR Format

FHIR data is usually in JSON format. Here’s an example FHIR JSON object for a patient resource:

**FHIR Sample Data**:
```json
{
  "resourceType": "Patient",
  "id": "123",
  "name": [
    {
      "family": "Doe",
      "given": ["John"]
    }
  ],
  "gender": "male",
  "birthDate": "1980-01-01"
}
```

**cURL Request**:
```bash
curl -X POST http://127.0.0.1:5000/convert -H "Content-Type: application/json" -d '{"resourceType": "Patient", "id": "123", "name": [{"family": "Doe", "given": ["John"]}], "gender": "male", "birthDate": "1980-01-01"}'
```

**Expected JSON Output**:
```json
{
  "format": "FHIR",
  "data": {
    "resourceType": "Patient",
    "id": "123",
    "name": [
      {
        "family": "Doe",
        "given": ["John"]
      }
    ],
    "gender": "male",
    "birthDate": "1980-01-01"
  }
}
```

#### 3. EMR Format (Hypothetical)

For EMR data, let’s assume a JSON format with a unique structure. Here’s an example:

**EMR Sample Data**:
```json
{
  "EMRType": "PatientRecord",
  "patientId": "123",
  "patientName": {
    "lastName": "Doe",
    "firstName": "John"
  },
  "gender": "M",
  "dob": "1980-01-01",
  "address": "123 Main St, City, State, 12345"
}
```

**cURL Request**:
```bash
curl -X POST http://127.0.0.1:5000/convert -H "Content-Type: application/json" -d '{"EMRType": "PatientRecord", "patientId": "123", "patientName": {"lastName": "Doe", "firstName": "John"}, "gender": "M", "dob": "1980-01-01", "address": "123 Main St, City, State, 12345"}'
```

**Expected JSON Output**:
```json
{
  "format": "EMR",
  "data": {
    "EMRType": "PatientRecord",
    "patientId": "123",
    "patientName": {
      "lastName": "Doe",
      "firstName": "John"
    },
    "gender": "M",
    "dob": "1980-01-01",
    "address": "123 Main St, City, State, 12345"
  }
}
```

---

## Adding Support for Additional Formats

To extend this API with more healthcare data formats:
1. **Update `detect_format` Function**: Add rules to recognize the new format.
2. **Create a New Parsing Function**: Define a new function to parse the specific data format.
3. **Integrate Parsing into Endpoint**: Update the `/convert` endpoint to handle the new format.

---

## Error Handling

If the data format is unknown, the API returns a 400 error with a message:
```json
{
  "error": "Unknown format"
}
```

---

## Example Response for Errors

If any error occurs during processing, the API returns:
```json
{
  "error": "Error message here"
}
```

This ensures that any issues are reported back to the client.

---

## License
This project is licensed under the MIT License. 

## Contributions
Contributions are welcome. Please fork this repository and submit a pull request if you would like to contribute to this project.
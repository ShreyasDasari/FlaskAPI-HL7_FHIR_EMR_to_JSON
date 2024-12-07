# HealthCare Data Interoperability Wrapper

## Overview

This **HealthCare Data Interoperability Wrapper** is a Python-based tool designed to standardize healthcare data from various formats into a unified **Custom JSON format**. It seamlessly handles **HL7**, **FHIR**, **EHR** (JSON/XML), and **Plain Text** formats, enabling interoperability between different healthcare systems. 

Additionally, a **Streamlit Dashboard** is included to provide a user-friendly interface for testing and interacting with the API.

---

## Features

1. **Multi-format Support**:
   - **HL7**: Common format used in healthcare messaging.
   - **FHIR**: Modern standard for healthcare data exchange.
   - **EHR** (JSON/XML): Electronic Health Records in structured JSON or XML.
   - **Plain Text**: Simple human-readable data entries.

2. **Custom JSON Output**:
   - A unified structure that captures essential healthcare data:
     ```json
     {
       "resourceType": "<type>",
       "text": {"status": "<status>"},
       "hospital": {"identifier": {"value": "<hospital_name>"}},
       "person": {
         "firstName": "<given_name>",
         "lastName": "<family_name>",
         "gender": "<gender>",
         "DOB": "<date_of_birth>",
         "Vitals": "<vitals_if_present>"
       },
       "relatedFields": {<additional_fields>}
     }
     ```

3. **Streamlit Dashboard**:
   - Allows users to input data in various formats.
   - Displays the converted Custom JSON output interactively.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ShreyasDasari/FlaskAPI-HL7_FHIR_EMR_to_JSON.git
   cd FlaskAPI-HL7_FHIR_EMR_to_JSON
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask API:
   ```bash
   python app.py
   ```

4. Run the Streamlit Dashboard:
   ```bash
   streamlit run dashboard.py
   ```

---

## Usage

### **API Endpoints**

- **POST /convert**
  - Input: Healthcare data in **HL7**, **FHIR**, **EHR (JSON/XML)**, or **Plain Text** format.
  - Output: Converted Custom JSON.

#### Example Request:
```bash
curl -X POST -d '<your_input>' http://127.0.0.1:5000/convert
```

---

## Input Formats and Examples

### **1. HL7 Input**
```plaintext
MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|20241206||ADT^A01|123456|P|2.3
PID|1||123456^^^HospitalMRN||Doe^John||19800515|M|||123 Main St^^City^ST^12345||(555)123-4567|||S
OBX|1|NM|Vitals|BP^Blood Pressure|120/80|mmHg|Normal|20241205
```

#### Custom JSON Output
```json
{
  "resourceType": "HL7",
  "text": {"status": "generated"},
  "hospital": {"identifier": {"value": "SendingFacility"}},
  "person": {
    "firstName": "John",
    "lastName": "Doe",
    "gender": "M",
    "DOB": "1980-05-15",
    "Vitals": "BP^Blood Pressure|120/80|mmHg|Normal"
  },
  "relatedFields": {
    "MSH": ["..."],
    "OBX": ["..."]
  }
}
```

---

### **2. FHIR Input**
```json
{
  "resourceType": "Patient",
  "id": "123456",
  "text": {"status": "generated"},
  "name": [{"family": "Doe", "given": ["John"]}],
  "gender": "male",
  "birthDate": "1980-05-15"
}
```

#### Custom JSON Output
```json
{
  "resourceType": "Patient",
  "text": {"status": "generated"},
  "hospital": {"identifier": {"value": "FHIR Hospital"}},
  "person": {
    "firstName": "John",
    "lastName": "Doe",
    "gender": "male",
    "DOB": "1980-05-15",
    "Vitals": "Normal"
  },
  "relatedFields": {
    "id": "123456"
  }
}
```

---

### **3. EHR (JSON) Input**
```json
{
  "hospitalName": "General Hospital",
  "patient": {
    "patientName": {"given": "John", "family": "Doe"},
    "gender": "male",
    "birthDate": "1980-05-15"
  }
}
```

#### Custom JSON Output
```json
{
  "resourceType": "EHR_JSON",
  "text": {"status": "generated"},
  "hospital": {"identifier": {"value": "General Hospital"}},
  "person": {
    "firstName": "John",
    "lastName": "Doe",
    "gender": "male",
    "DOB": "1980-05-15",
    "Vitals": "Not Provided"
  },
  "relatedFields": {}
}
```

---

### **4. EHR (XML) Input**
```xml
<EHR>
  <hospitalName>General Hospital</hospitalName>
  <patient>
    <patientName>
      <given>John</given>
      <family>Doe</family>
    </patientName>
    <gender>male</gender>
    <birthDate>1980-05-15</birthDate>
  </patient>
</EHR>
```

#### Custom JSON Output
```json
{
  "resourceType": "EHR_XML",
  "text": {"status": "generated"},
  "hospital": {"identifier": {"value": "General Hospital"}},
  "person": {
    "firstName": "John",
    "lastName": "Doe",
    "gender": "male",
    "DOB": "1980-05-15",
    "Vitals": "Not Provided"
  },
  "relatedFields": {}
}
```

---

### **5. Plain Text Input**
```plaintext
Hospital: General Hospital
FirstName: John
LastName: Doe
Gender: Male
DOB: 1980-05-15
Vitals: BP 120/80
```

#### Custom JSON Output
```json
{
  "resourceType": "PlainText",
  "text": {"status": "generated"},
  "hospital": {"identifier": {"value": "General Hospital"}},
  "person": {
    "firstName": "John",
    "lastName": "Doe",
    "gender": "Male",
    "DOB": "1980-05-15",
    "Vitals": "BP 120/80"
  },
  "relatedFields": {}
}
```

---

## Streamlit Dashboard

The **Streamlit Dashboard** provides an interactive interface to input data in any of the supported formats. It displays the converted **Custom JSON** output.

### Steps:
1. Run the Streamlit dashboard:
   ```bash
   streamlit run dashboard.py
   ```

2. Open your browser at the displayed URL (usually `http://localhost:8501`).

3. Select the input format (HL7, FHIR, EHR JSON/XML, Plain Text).

4. Enter your input data in the provided text area.

5. Click **Convert** to view the Custom JSON output.

---

## Contributing

Contributions are welcome! If you’d like to improve the tool:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
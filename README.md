# HealthCare Data Interoperability Wrapper

## Overview

This **HealthCare Data Interoperability Wrapper** is a transformative tool designed to standardize healthcare data from various formats into a unified **Custom JSON format**, bridging the gap between legacy systems and modern healthcare platforms. 

Deployed on **Streamlit Cloud Community**: [**Live App**](https://healthcare-data-interoperability-wrapper.streamlit.app/).

By supporting diverse healthcare data formats like **HL7**, **FHIR**, **EHR (JSON/XML)**, and **Plain Text**, this tool empowers healthcare organizations to achieve seamless data interoperability, essential for efficient care delivery and data-driven insights.

---

## Real-World Impact and Purpose

### Why This Project Matters:
1. **Healthcare Data Interoperability**: In the healthcare industry, data exists in various formats and silos. This tool facilitates seamless integration and standardization, enabling systems to "talk to each other."
2. **Simplified Migration**: During transitions between healthcare software platforms, this tool ensures that critical patient and hospital data is accurately converted into a consistent structure.
3. **Improved Patient Care**: By reducing data silos and inconsistencies, healthcare providers can access complete and accurate patient records, leading to better clinical decisions.
4. **Research and Analytics**: Standardized data empowers healthcare organizations to perform advanced analytics, improve resource allocation, and identify trends for public health planning.

### How It Helps:
- **Hospitals & Clinics**: During software migrations or system upgrades, this tool ensures no data loss or misinterpretation.
- **Developers & Analysts**: Offers a ready-to-use framework for healthcare data parsing and transformation.
- **Patients**: Enables healthcare providers to focus on patient outcomes rather than manual data entry or corrections.

This project embodies the potential of data science to solve critical real-world problems, demonstrating technical proficiency and a passion for impact—a perfect showcase for aspiring data scientists.

---

## Features

1. **Multi-format Support**:
   - **HL7**: Widely used for healthcare messaging.
   - **FHIR**: The modern standard for healthcare data exchange.
   - **EHR (JSON/XML)**: Electronic Health Records in structured JSON or XML.
   - **Plain Text**: Simple human-readable data entries.

2. **Custom JSON Output**:
   - Standardized structure designed for interoperability:
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
   - User-friendly interface for interactive data transformation.
   - Supports input in all formats and displays converted output in real-time.

4. **Deployed on Streamlit Cloud**:
   - Easily accessible via the live URL: [**Healthcare Data Interoperability Wrapper**](https://healthcare-data-interoperability-wrapper.streamlit.app/).

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

3. Run the Streamlit dashboard:
   ```bash
   streamlit run streamlit_app.py
   ```

4. Open the dashboard in your browser at `http://localhost:8501`.

---

## Usage

### Input Formats Supported:
1. **HL7**
2. **FHIR**
3. **EHR (JSON/XML)**
4. **Plain Text**

Enter data in any of these formats into the dashboard or send it to the API endpoint (`/convert`) to receive a standardized Custom JSON output.

---

## Streamlit Dashboard

The **Streamlit Dashboard** is an interactive tool for testing and visualizing the conversion process. 

**Steps:**
1. Visit the deployed app: [**Healthcare Data Interoperability Wrapper**](https://healthcare-data-interoperability-wrapper.streamlit.app/).
2. Select the input format from the dropdown.
3. Enter your data in the text area.
4. Click **Convert** to generate the output in **Custom JSON** format.

---

## Input Examples

### **HL7 Input**
```plaintext
MSH|^~\&|SendingApp|SendingFacility|ReceivingApp|ReceivingFacility|20241206||ADT^A01|123456|P|2.3
PID|1||123456^^^HospitalMRN||Doe^John||19800515|M|||123 Main St^^City^ST^12345||(555)123-4567|||S
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
    "Vitals": "Not Provided"
  },
  "relatedFields": {...}
}
```

*Additional examples for FHIR, EHR JSON/XML, and Plain Text are included in the [examples](examples/) directory.*

---

## Real-World Applications

1. **Healthcare Data Interoperability**:
   - Enables seamless communication between legacy systems and modern healthcare platforms.
   - Ensures accurate and efficient data exchange, a critical requirement for Electronic Health Record (EHR) systems.

2. **Migration and Upgrades**:
   - Simplifies the transition to new healthcare software by standardizing legacy data into a consistent structure.

3. **Healthcare Analytics**:
   - Provides structured data that can be directly fed into analytical models for insights and predictions.

---

## Contributing

Contributions are welcome! If you'd like to enhance this project:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with detailed explanations of your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

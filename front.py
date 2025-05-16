import streamlit as st
import requests

# Streamlit title and input
st.title("Marathi Grammar Checker")
st.markdown("Upload a file or enter text for Marathi grammar checking.")

# Textbox for entering Marathi text
text = st.text_area("Enter Marathi Text", height=200)

# Upload a file for grammar check
uploaded_file = st.file_uploader("Upload a .txt, .docx, or .pdf file", type=["txt", "docx", "pdf"])

API_URL = "http://localhost:5000/upload"  # Change if your backend URL is different

# Function to handle backend requests and responses
def send_request_to_backend(data=None, file=None):
    try:
        # If a file is uploaded
        if file is not None:
            files = {"file": file}
            response = requests.post(API_URL, files=files)
        else:
            # If plain text is entered
            response = requests.post(API_URL, data={"text": data})

        # Checking the status of the response
        if response.status_code == 200:
            result = response.json()  # Parse response as JSON

            # Handle results based on 'status' field
            if result.get("status") == "errors_found":
                st.error("Grammar errors found!")
                st.write("Corrected Text:")
                st.success(result["corrected_text"])

            elif result.get("status") == "no_errors":
                st.success("No errors found!")
                st.write("Your text is grammatically correct!")

            else:
                st.error("Unexpected response from server.")
                st.write(result.get("message", "Unknown error"))

        else:
            st.error(f"Request failed with status code {response.status_code}")

    except Exception as e:
        st.error(f"Error: {e}")

# Check if text or file is provided, and send it to the backend
if uploaded_file is not None:
    send_request_to_backend(file=uploaded_file)
elif text.strip():
    send_request_to_backend(data=text)
else:
    st.warning("Please enter text or upload a file to check grammar.")

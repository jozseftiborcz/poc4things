import requests

def convert_docx_to_pdf_with_adobe(docx_file, output_pdf_file):
    url = "https://api.adobe.com/apis/documentservices/job"

    # Prepare the request headers
    headers = {
        "Content-Type": "application/json"
    }

    # Prepare the request body
    payload = {
        "inputs": [
            {
                "type": "document",
                "content": {
                    "type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "data": ""
                }
            }
        ],
        "outputs": [
            {
                "type": "application/pdf"
            }
        ]
    }

    # Read the DOCX file
    with open(docx_file, "rb") as file:
        file_data = file.read()

    # Set the DOCX file data in the request payload
    payload["inputs"][0]["content"]["data"] = file_data.decode("ISO-8859-1")

    # Send the conversion request
    response = requests.post(url, headers=headers, json=payload)

    if response.ok:
        job_id = response.json()["jobId"]
        status_url = f"{url}/{job_id}"

        # Poll the status until the conversion is complete
        while True:
            status_response = requests.get(status_url, headers=headers)
            status = status_response.json()["status"]

            if status == "SUCCEEDED":
                download_url = status_response.json()["outputs"][0]["downloadUrl"]
                break
            elif status == "FAILED":
                print("Conversion failed.")
                return

        # Download the converted PDF file
        pdf_response = requests.get(download_url)
        with open(output_pdf_file, "wb") as file:
            file.write(pdf_response.content)

        print(f"Conversion successful. PDF file saved as {output_pdf_file}.")
    else:
        print(f"Conversion request failed. Status code: {response.status_code} - {response.reason}")

# Example usage
docx_file_path = "output.docx"
pdf_file_path = "output.pdf"

convert_docx_to_pdf_with_adobe(docx_file_path, pdf_file_path)


import tkinter as tk
from tkinter import filedialog, scrolledtext
import boto3
from textractcaller import call_textract_lending
from textractprettyprinter.t_pretty_print import convert_lending_from_trp2
from IPython.display import Image, display, HTML, JSON, IFrame
import trp.trp2_lending as tl
import json
import os
import pandas as pd
import subprocess

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, filename)

# def call_textract_lending(input_document, boto3_textract_client):
#     response = boto3_textract_client.start_document_analysis(
#         DocumentLocation={
#             'S3Object': {
#                 'Bucket': input_document.split('/')[2],
#                 'Name': '/'.join(input_document.split('/')[3:])
#             }
#         },
#         FeatureTypes=['FORMS', 'TABLES']
#     )
#     return response 

def upload_file():
    file_path = file_path_entry.get()
    print(f"file_path {file_path}")
    if not file_path:
        result_label.config(text="Please select a file first.")
        return

    try:
        # Set up AWS clients
        s3 = boto3.client('s3')
        textract = boto3.client('textract')

        # S3 bucket details
        bucket_name = "your-bucket-name"  # Replace with your actual bucket name
        s3_path = "idp/textract/" + os.path.basename(file_path)

        # Upload file to S3
        s3.upload_file(file_path, bucket_name, s3_path)
        print("File Uploaded...")

        # Prepare input for Textract
        input_file = f's3://{bucket_name}/{s3_path}'
        display(IFrame(input_file, 500, 600))

        # Call Textract
        # textract_json = call_textract_lending(input_document=input_file, boto3_textract_client=textract)
        textract_json = call_textract_lending(input_document=input_file, boto3_textract_client=textract)

        # Display JSON in text area
        json_output.delete('1.0', tk.END)
        json_output.insert(tk.END, json.dumps(textract_json, indent=2))

        result_label.config(text="File processed successfully. JSON output displayed below.")
    except Exception as e:
        result_label.config(text=f"An error occurred: {str(e)}")
        print(f"An error occurred: {str(e)}")
    #     # Process results
    #     results = textract_json['Results']
    #     for page in results:
    #         print(f"Page Number: {page['Page']}, Page Classification: {page['PageClassification']['PageType']}")

    #     # Save JSON output
    #     with open("lending-doc-output.json", "w") as f:
    #         json.dump(textract_json, f)

    #     result_label.config(text="File processed successfully. Check 'lending-doc-output.json' for results.")
    # except Exception as e:
    #     result_label.config(text=f"An error occurred: {str(e)}")

root = tk.Tk()
root.title("Document Upload and Process")
root.geometry("600x500")

# File path entry
file_path_entry = tk.Entry(root, width=50)
file_path_entry.pack(pady=10)

# Browse button
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

# Upload button
upload_button = tk.Button(root, text="Upload and Process", command=upload_file)
upload_button.pack(pady=10)

# Result label
result_label = tk.Label(root, text="", wraplength=580)
result_label.pack(pady=10)

# JSON output text area
json_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20)
json_output.pack(pady=10)

root.mainloop()

# # Create main window
# root = tk.Tk()
# root.title("Document Upload")
# root.geometry("400x200")

# # File path entry
# file_path_entry = tk.Entry(root, width=50)
# file_path_entry.pack(pady=10)

# # Browse button
# browse_button = tk.Button(root, text="Browse", command=browse_file)
# browse_button.pack()

# # Upload button
# upload_button = tk.Button(root, text="Upload and Process", command=upload_file)
# upload_button.pack(pady=10)

# # Result label
# result_label = tk.Label(root, text="", wraplength=380)
# result_label.pack(pady=10)

# root.mainloop()


# # Set up AWS credentials and region
# # Make sure you have AWS CLI configured or set these explicitly
# region = boto3.session.Session().region_name
# account_id = boto3.client('sts').get_caller_identity().get('Account')

# # Set up S3 bucket
# # You'll need to specify your bucket name here
# data_bucket = "sagemaker-eu-west-2-307946670775"

# os.environ["BUCKET"] = data_bucket
# os.environ["REGION"] = region

# print(f"Default Bucket: s3://{data_bucket}")

# s3 = boto3.client('s3')
# textract = boto3.client('textract', region_name=region)

# document = 'lending_package.pdf'

# # Upload document to S3 bucket
# # C:\Users\Dell\Desktop\PythonApplications\IntelligentDocumentExtraction\ImageToTextExtract\docs\Ramakrishna Resume.doc
# local_file_path = r"C:\Users\Dell\Desktop\PythonApplications\IntelligentDocumentExtraction\ImageToTextExtract\docs\Payslip_2022-03-31.pdf"
# s3_path = f"idp/textract/{local_file_path}"
# # s3_path = f"idp/textract/{document}"

# print(f"Uploading {local_file_path} to s3://{data_bucket}/{s3_path}")
# s3.upload_file(local_file_path, data_bucket, s3_path)

# input_file = f's3://{data_bucket}/{s3_path}'
# print(f"Lending Package uploaded to S3: {input_file}")

# # Call Textract
# textract_json = call_textract_lending(input_document=input_file, boto3_textract_client=textract)

# results = textract_json['Results']
    
# for page in results:
#     print(f"Page Number: {page['Page']}, Page Classification: {page['PageClassification']['PageType']}")

# # Save JSON output
# with open("lending-doc-output.json", "w") as f:
#     json.dump(textract_json, f)

# # Convert to TRP2 format
# trp2_doc: tl.TFullLendingDocument = tl.TFullLendingDocumentSchema().load(textract_json)
# lending_array = convert_lending_from_trp2(trp2_doc)

# # Write to CSV
# import csv
  
# index_fields = ['{page_classification}_{page_number_within_document_type}', 'page_number_in_document', 'key','key_confidence','value','value_confidence','key-bounding-box.top','key-bounding-box.height','key-bb.width','key-bb.left','value-bounding-box.top','value-bb.height','value-bb.width','value-bb.left'] 

# with open('analyze-lending-output.csv', 'w', newline='') as f:
#     csv_writer = csv.writer(f)
#     csv_writer.writerow(index_fields)
#     csv_writer.writerows(lending_array)

# print("Processing complete. Check 'lending-doc-output.json' and 'analyze-lending-output.csv' for results.")
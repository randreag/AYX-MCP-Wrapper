import time
import json
import re
from typing import List, Optional, Dict, Any
from src.tools import AYXMCPTools, InputData
from src.server_client.rest import ApiException
import src.server_client as server_client
import tempfile
import pprint
import os

# get job output files
def get_job_output_files(job_id: str):
    """
    Get the results of a job by its ID.
    """
    configuration = server_client.Configuration()
    jobs_api = server_client.JobsApi(server_client.ApiClient(configuration))
    try:
        # check if job exists
        job = jobs_api.jobs_get_job_v3(job_id)
        if not job:
            return "Error: Job not found"
        # check if job is completed
        if job.status != "Completed":
            return "Error: Job is not completed"
        
        temp_directory = tempfile.gettempdir()
        all_output_files = []

        for output in job.outputs:
            output_id = output.id
            file_name = output.file_name
            available_output_types = output.available_formats
            # get file name with extension from file_name
            # Extract base name without extension if it exists
            base_name = os.path.splitext(os.path.basename(file_name))[0]
            
            # Get the file extension from the file name
            raw_file_extension = os.path.splitext(os.path.basename(file_name))[1]

            # Map output format to file extension
            format_extension_map = {
                'Raw': raw_file_extension if raw_file_extension else '.txt',
                'Yxdb': '.yxdb',
                'Shp': '.shp',
                'Kml': '.kml',
                'Tab': '.tab',
                'Mif': '.mif',
                'Dbf': '.dbf',
                'Csv': '.csv',
                'Pdf': '.pdf',
                'Docx': '.docx',
                'Xlsx': '.xlsx',
                'Html': '.html',
                'Tde': '.tde',
                'Zip': '.zip'
            }

            # Get the file extension from the available output types
            # Get the extension for the first available format
            output_format = available_output_types[0] if available_output_types else 'Raw'
            file_extension = format_extension_map.get(output_format, raw_file_extension)
            file_name_with_extension = base_name + file_extension

            # get the output data
            api_response = jobs_api.jobs_get_output_file(job_id, output_id, output_format)

            # Convert to bytes if it's a string
            if isinstance(api_response, str):
                api_response_bytes = api_response.encode('utf-8')
            else:
                api_response_bytes = api_response

            with open(f"{temp_directory}/{job_id}_{output_id}_{file_name_with_extension}", "wb") as f:
                f.write(api_response_bytes)

            all_output_files.append(f"{temp_directory}/{job_id}_{output_id}_{file_name_with_extension}")

        return f"Output files saved to:  {pprint.pformat(all_output_files)} \n\n"
    
    except ApiException as e:
        return f"Error: {e}"

def main():
    """
    Main function to demonstrate workflow execution functionality.
    """
    job_id = "686547c6223c052a55003255"
    output_id = "Output"
    output_type = "Csv" # Available values : Raw, Yxdb, Shp, Kml, Tab, Mif, Dbf, Csv, Pdf, Docx, Xlsx, Html, Tde, Zip

    # Example 1: read job results
    print(f"1. Reading job results for job: {job_id}")

    job_results = get_job_output_files(job_id)
    print(job_results)

    
    print("\n=== Demo completed ===")


if __name__ == "__main__":
    main()

import os
import shutil
import zipfile
import tempfile
import src.server_client as server_client


def extract_workflow_xml(workflow_id):
    """
    Extract XML content from a workflow file.
    
    Args:
        workflow_id: The ID of the workflow
        
    Returns:
        str: The XML content of the workflow file, or error message
    """
    configuration = server_client.Configuration()
    workflows_api = server_client.WorkflowsApi(server_client.ApiClient(configuration))

    try:
        # First check if workflow exists
        api_response = workflows_api.workflows_get_workflow(workflow_id)
        if api_response is None:
            return "Error: Workflow not found"
        
        # Download the workflow file
        api_response = workflows_api.workflows_download_workflow(workflow_id)
        if api_response is None:
            return "Error: Failed to download workflow"
            
        temp_directory = tempfile.gettempdir()
        
        with open(
            f"{temp_directory}/{workflow_id}.yxz",
            "wb" if not os.path.exists(f"{temp_directory}/{workflow_id}.yxz") else "wb+",
        ) as f:
            f.write(api_response)
        
        new_directory = f"{temp_directory}/{workflow_id}"
        if os.path.exists(new_directory):
            shutil.rmtree(new_directory)
        os.makedirs(new_directory)
        
        with zipfile.ZipFile(f"{temp_directory}/{workflow_id}.yxz", "r") as zip_ref:
            zip_ref.extractall(new_directory)
        
        yxmd_files = [file for file in os.listdir(new_directory) if file.endswith(".yxmd")]
        if len(yxmd_files) == 0:
            return "Error: Workflow XML file not found after unzipping"
        
        yxmd_file = yxmd_files[0]
        # Read as binary first, then decode as UTF-8
        with open(f"{new_directory}/{yxmd_file}", "rb") as f:
            binary_content = f.read()
            try:
                # Try to decode as UTF-8
                return binary_content.decode('utf-8')
            except UnicodeDecodeError:
                # If UTF-8 fails, return the binary content as a string representation
                return binary_content
                
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Main function to demonstrate usage of extract_workflow_xml."""
    # Example usage - you would need to provide actual values
    workflow_id = "67e10abe127dd21432a1df79"
    
    try:
        xml_content = extract_workflow_xml(workflow_id)
        print("Extracted XML content:")
        print(xml_content)
    except Exception as e:
        print(f"Error extracting workflow XML: {e}")


if __name__ == "__main__":
    main()
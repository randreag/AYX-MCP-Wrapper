import os
import shutil
import zipfile
import tempfile
import src.server_client as server_client
from pprint import pprint
import xmltodict

def get_workflow_tool_list(workflow_id: str):
    """Get the list of the workflow tools and the tool properties by the workflow ID"""
    configuration = server_client.Configuration()
    workflows_api = server_client.WorkflowsApi(server_client.ApiClient(configuration))

    try:
        api_response = workflows_api.workflows_get_workflow(workflow_id)
        if api_response is None:
            return "Error: Workflow not found"
        
        # Download the workflow file
        api_response = workflows_api.workflows_download_workflow(workflow_id)
        if api_response is None:
            return "Error: Failed to download workflow"
            
        temp_directory = configuration.temp_directory
        # normalize the temp directory
        temp_directory = os.path.normpath(temp_directory)
        if not os.path.exists(temp_directory):
            os.makedirs(temp_directory)
        
        with open(
            f"{temp_directory}/{workflow_id}.yxzp",
            "wb" if not os.path.exists(f"{temp_directory}/{workflow_id}.yxzp") else "wb+",
        ) as f:
            f.write(api_response)

        new_directory = f"{temp_directory}/{workflow_id}"
        if os.path.exists(new_directory):
            shutil.rmtree(new_directory)
        os.makedirs(new_directory)
        
        with zipfile.ZipFile(f"{temp_directory}/{workflow_id}.yxzp", "r") as zip_ref:
            zip_ref.extractall(new_directory)
        
        yxmd_files = [file for file in os.listdir(new_directory) if file.endswith(".yxmd") or file.endswith(".yxwz")]
        if len(yxmd_files) == 0:
            return "Error: Workflow XML file not found after unzipping"
        
        yxmd_file = yxmd_files[0]

        # Read as binary first, then decode as UTF-8
        with open(f"{new_directory}/{yxmd_file}", "rb") as f:
            binary_content = f.read()
            try:
                # Try to decode as UTF-8
                xml_content = binary_content.decode('utf-8')
            except UnicodeDecodeError:
                # If UTF-8 fails, return the binary content as a string representation
                xml_content = binary_content

        # Parse the XML content using xmltodict
        xml_dict = xmltodict.parse(xml_content)

        # extract the tools list
        tools_list = xml_dict['AlteryxDocument']['Nodes']['Node']
        # if tools_list is a list, then we need to iterate through it
        tools_dict = {}
        if isinstance(tools_list, list):
            for tool in tools_list:
                tool_id = tool['@ToolID']
                tool_type = tool['GuiSettings']['@Plugin']
                tool_dict = tool['Properties']['Configuration']
                # Add the tool type to the tool dictionary
                tool_dict['ToolType'] = tool_type

                # Remove all properties BG_Image, Font, TextColor, FillColor, Justification, TextSize
                tool_dict.pop('BG_Image', None)
                tool_dict.pop('Font', None)
                tool_dict.pop('TextColor', None)
                tool_dict.pop('FillColor', None)
                tool_dict.pop('Justification', None)
                tool_dict.pop('TextSize', None)

                # Remove the data encoded in the tool
                tool_dict.pop('Data', None)

                tools_dict[tool_id] = tool_dict
        else:
            tool_id = tools_list['@ToolID']
            tool_type = tools_list['GuiSettings']['@Plugin']
            tool_dict = tools_list['Properties']['Configuration']
            # Add the tool type to the tool dictionary
            tool_dict['ToolType'] = tool_type

            # Remove all properties BG_Image, Font, TextColor, FillColor, Justification, TextSize
            tool_dict.pop('BG_Image', None)
            tool_dict.pop('Font', None)
            tool_dict.pop('TextColor', None)
            tool_dict.pop('FillColor', None)
            tool_dict.pop('Justification', None)
            tool_dict.pop('TextSize', None)

            # Remove the data encoded in the tool
            tool_dict.pop('Data', None)

            # Add the tool dictionary to the tools dictionary
            tools_dict[tool_id] = tool_dict
        return tools_dict
                
    except Exception as e:
        return f"Error: {str(e)}"


def main():
    """Main function to demonstrate usage of extract_workflow_xml."""
    # Example usage - you would need to provide actual values
    workflow_id = "686e0d65c04bebdd09cdda5e"
    
    try:
        tools_dict = get_workflow_tool_list(workflow_id)
        print("Tools dictionary:")
        pprint(tools_dict)
    except Exception as e:
        print(f"Error extracting workflow XML: {e}")


if __name__ == "__main__":
    main()
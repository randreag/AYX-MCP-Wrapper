import time
import json
import re
from typing import List, Optional, Dict, Any
from src.tools import AYXMCPTools, InputData
from src.server_client.rest import ApiException

def main():
    """
    Main function to demonstrate workflow execution functionality.
    """
    workflow_id = "686358e9c04bebdd09cc95f1"
    # Example 1: Execute workflow without parameters
    print(f"1. Executing workflow: {workflow_id}")
    
    # Example input data (uncomment and modify as needed)
    # input_data = [
    #     InputData(name="parameter1", value="value1"),
    #     InputData(name="parameter2", value="value2")
    # ]

    tools = AYXMCPTools()
    
    execution_result = tools.execute_workflow_with_monitoring(
        workflow_id=workflow_id,
        input_data=None,  # Set to None for workflows without parameters
        wait_for_completion=True,
        timeout_seconds=300,  # 5 minutes timeout
        poll_interval_seconds=10
    )

    print(execution_result)
    
    # if execution_result["success"]:
    #     print("✅ Workflow executed successfully!")
    #     print(f"Job ID: {execution_result['job_id']}")
    #     print(f"Status: {execution_result['status']}")
    #     print(f"Execution time: {execution_result.get('execution_time_seconds', 'N/A')} seconds")
        
    #     if "job_messages" in execution_result:
    #         print("\nJob messages:")
    #         print(execution_result["job_messages"])
    # else:
    #     print("❌ Workflow execution failed!")
    #     print(f"Error: {execution_result['error']}")
    #     if execution_result.get('job_id'):
    #         print(f"Job ID: {execution_result['job_id']}")
    
    # print("\n" + "="*50 + "\n")
    
    # # Example 2: Execute workflow with parameters (commented out)
    # print("2. Example: Executing workflow with parameters")
    # print("(This example is commented out - uncomment and modify as needed)")
    
    # # Uncomment and modify the following code to execute a workflow with parameters:
    # """
    # # Example workflow with parameters
    # parameterized_workflow_id = "your-parameterized-workflow-id"
    
    # input_data = [
    #     InputData(name="input_file", value="/path/to/input.csv"),
    #     InputData(name="output_file", value="/path/to/output.csv"),
    #     InputData(name="filter_value", value="active")
    # ]
    
    # param_execution_result = execute_workflow_with_monitoring(
    #     workflow_id=parameterized_workflow_id,
    #     input_data=input_data,
    #     wait_for_completion=True,
    #     timeout_seconds=600,  # 10 minutes timeout
    #     poll_interval_seconds=5
    # )
    
    # if param_execution_result["success"]:
    #     print("✅ Parameterized workflow executed successfully!")
    #     print(f"Job ID: {param_execution_result['job_id']}")
    # else:
    #     print("❌ Parameterized workflow execution failed!")
    #     print(f"Error: {param_execution_result['error']}")
    # """
    
    print("\n=== Demo completed ===")


if __name__ == "__main__":
    main()

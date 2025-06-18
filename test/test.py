import unittest
from src.main import (
    get_all_collections,
    get_collection_by_id,
    create_collection,
    update_collection_name_or_owner,
    add_workflow_to_collection,
    remove_workflow_from_collection,
    add_schedule_to_collection,
    remove_schedule_from_collection,
    delete_collection,
    get_all_workflows,
    get_workflow_by_id,
    update_workflow_name_or_comment,
    transfer_workflow,
    get_workflow_jobs,
    execute_workflow,
    get_all_users,
    get_user_by_id,
    get_user_by_email,
    get_user_by_name,
    get_user_by_first_name,
    get_all_user_assets,
    get_user_assets_by_type,
    update_user_details,
    transfer_all_assets,
    deactivate_user,
    reset_user_password,
    get_all_job_messages,
    get_job_by_id,
    get_all_schedules,
    get_schedule_by_id,
    deactivate_schedule,
    activate_schedule,
    update_schedule_name_or_comment,
    change_schedule_owner,
    get_all_credentials,
    get_credential_by_id,
    lookup_connection,
    get_connection_by_id,
    download_workflow_package_file,
    get_workflow_xml,
)
import os
import tempfile
from pydantic import BaseModel


class TestInputData(BaseModel):
    name: str
    value: str


class TestMCPTools(unittest.TestCase):
    def setUp(self):
        # Initialize any test setup here
        self.test_workflow_id = "67e10abe127dd21432a1df79"
        self.test_collection_id = "bbbeb4bcbf7347eca5dccc0bc8d9fb7d"
        self.test_user_id = "67f406f7a15a3c043e696465"
        self.test_schedule_id = "67e97c3cf1790000fd000482"
        self.test_credential_id = "test_credential_id"
        self.test_connection_id = "test_connection_id"
        self.test_job_id = "test_job_id"

    def test_collections_tools(self):
        # Test get_all_collections
        result = get_all_collections()
        self.assertIsNotNone(result)

        # Test get_collection_by_id
        result = get_collection_by_id(self.test_collection_id)
        self.assertIsNotNone(result)

        # Test create_collection
        result = create_collection("Test Collection")
        self.assertIsNotNone(result)

        # Test update_collection_name_or_owner
        result = update_collection_name_or_owner(self.test_collection_id, "Updated Name", self.test_user_id)
        self.assertIsNotNone(result)

        # Test add_workflow_to_collection
        result = add_workflow_to_collection(self.test_collection_id, self.test_workflow_id)
        self.assertIsNotNone(result)

        # Test remove_workflow_from_collection
        result = remove_workflow_from_collection(self.test_collection_id, self.test_workflow_id)
        self.assertIsNotNone(result)

        # Test add_schedule_to_collection
        result = add_schedule_to_collection(self.test_collection_id, self.test_schedule_id)
        self.assertIsNotNone(result)

        # Test remove_schedule_from_collection
        result = remove_schedule_from_collection(self.test_collection_id, self.test_schedule_id)
        self.assertIsNotNone(result)

        # Test delete_collection
        result = delete_collection(self.test_collection_id)
        self.assertIsNotNone(result)

    def test_workflows_tools(self):
        # Test get_all_workflows
        result = get_all_workflows()
        self.assertIsNotNone(result)

        # Test get_workflow_by_id
        result = get_workflow_by_id(self.test_workflow_id)
        self.assertIsNotNone(result)

        # Test update_workflow_name_or_comment
        result = update_workflow_name_or_comment(self.test_workflow_id, "Updated Name", "Updated Comment")
        self.assertIsNotNone(result)

        # Test transfer_workflow
        result = transfer_workflow(self.test_workflow_id, self.test_user_id)
        self.assertIsNotNone(result)

        # Test get_workflow_jobs
        result = get_workflow_jobs(self.test_workflow_id)
        self.assertIsNotNone(result)

        # Test execute_workflow
        input_data = [TestInputData(name="test", value="value")]
        result = execute_workflow(self.test_workflow_id, input_data)
        self.assertIsNotNone(result)

    def test_users_tools(self):
        # Test get_all_users
        result = get_all_users()
        self.assertIsNotNone(result)

        # Test get_user_by_id
        result = get_user_by_id(self.test_user_id)
        self.assertIsNotNone(result)

        # Test get_user_by_email
        result = get_user_by_email("test@example.com")
        self.assertIsNotNone(result)

        # Test get_user_by_name
        result = get_user_by_name("Test")
        self.assertIsNotNone(result)

        # Test get_user_by_first_name
        result = get_user_by_first_name("Test")
        self.assertIsNotNone(result)

        # Test get_all_user_assets
        result = get_all_user_assets(self.test_user_id)
        self.assertIsNotNone(result)

        # Test get_user_assets_by_type
        result = get_user_assets_by_type(self.test_user_id, "Workflow")
        self.assertIsNotNone(result)

        # Test update_user_details
        result = update_user_details(self.test_user_id, "New First", "New Last", "new@example.com")
        self.assertIsNotNone(result)

        # Test transfer_all_assets
        result = transfer_all_assets(self.test_user_id, self.test_user_id, True, True, True)
        self.assertIsNotNone(result)

        # Test deactivate_user
        result = deactivate_user(self.test_user_id)
        self.assertIsNotNone(result)

        # Test reset_user_password
        result = reset_user_password(self.test_user_id)
        self.assertIsNotNone(result)

    def test_jobs_tools(self):
        # Test get_all_job_messages
        result = get_all_job_messages(self.test_job_id)
        self.assertIsNotNone(result)

        # Test get_job_by_id
        result = get_job_by_id(self.test_job_id)
        self.assertIsNotNone(result)

    def test_schedules_tools(self):
        # Test get_all_schedules
        result = get_all_schedules()
        self.assertIsNotNone(result)

        # Test get_schedule_by_id
        result = get_schedule_by_id(self.test_schedule_id)
        self.assertIsNotNone(result)

        # Test deactivate_schedule
        result = deactivate_schedule(self.test_schedule_id)
        self.assertIsNotNone(result)

        # Test activate_schedule
        result = activate_schedule(self.test_schedule_id)
        self.assertIsNotNone(result)

        # Test update_schedule_name_or_comment
        result = update_schedule_name_or_comment(self.test_schedule_id, "Updated Name", "Updated Comment")
        self.assertIsNotNone(result)

        # Test change_schedule_owner
        result = change_schedule_owner(self.test_schedule_id, self.test_user_id)
        self.assertIsNotNone(result)

    def test_credentials_tools(self):
        # Test get_all_credentials
        result = get_all_credentials()
        self.assertIsNotNone(result)

        # Test get_credential_by_id
        result = get_credential_by_id(self.test_credential_id)
        self.assertIsNotNone(result)

    def test_connections_tools(self):
        # Test lookup_connection
        result = lookup_connection(self.test_connection_id)
        self.assertIsNotNone(result)

        # Test get_connection_by_id
        result = get_connection_by_id(self.test_connection_id)
        self.assertIsNotNone(result)

    def test_workflow_file_tools(self):
        # Test download_workflow_package_file
        temp_dir = tempfile.gettempdir()
        result = download_workflow_package_file(self.test_workflow_id, temp_dir)
        self.assertIsNotNone(result)
        self.assertTrue(os.path.exists(f"{temp_dir}/{self.test_workflow_id}.yxz"))

        # Test get_workflow_xml
        result = get_workflow_xml(self.test_workflow_id)
        self.assertIsNotNone(result)
        self.assertTrue(isinstance(result, str))


if __name__ == "__main__":
    unittest.main()

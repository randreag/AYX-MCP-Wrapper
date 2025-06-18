#!/usr/bin/env python3
from __future__ import print_function
import src.server_client
from src.server_client.rest import ApiException
from pprint import pprint
import os


def main():
    """Main entry point of the program."""

    # Configure OAuth2 access token for authorization: oauth2
    configuration = src.server_client.Configuration()
    configuration.client_id = os.getenv("ALTERYX_CLIENT_ID")
    configuration.client_secret = os.getenv("ALTERYX_CLIENT_SECRET")

    # create an instance of the API class
    api_instance = src.server_client.CollectionsApi(src.server_client.ApiClient(configuration))

    try:
        # Add a schedule to an existing collection.
        api_response = api_instance.collections_get_collections()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CollectionsApi->collections_add_schedule_to_collection: %s\n" % e)


if __name__ == "__main__":
    main()

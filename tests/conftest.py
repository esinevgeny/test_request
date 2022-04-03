import pytest
import json

PATH_TO_RESP_FILE_GET = '../responses/responses_get.json'
PATH_TO_RESP_FILE_POST = '../responses/responses_post.json'

# Keys for requests for testing link
GET = 'get'
POST = 'post'

responses = {}


@pytest.fixture(scope="module", autouse=True)
def read_response_file_before_testing():
    """
    Read expected responses from file
    :return: dict with expecred responses
    :type: dict
    """
    global responses
    for file, req in ((PATH_TO_RESP_FILE_GET, GET),
                      (PATH_TO_RESP_FILE_POST, POST)
                      ):
        try:
            with open(file, "r") as read_file:
                data = json.load(read_file)
            responses.update({req: data})
        except EnvironmentError:
            print("Can't read conf file")
            break


@pytest.fixture()
def get_expected_responses():
    """
    Fixture to return global response dict
    :return: dict witj expected responses
    :type: dict
    """
    return responses


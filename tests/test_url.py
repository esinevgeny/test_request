import requests
import json
import pytest
import urllib.parse

PATH_TO_RESP_FILE_GET = '../responses/responses_get.json'
PATH_TO_RESP_FILE_POST = '../responses/responses_post.json'

# Keys for requests for testing link
GET = 'get'
POST = 'post'

responses = {}

# Test link defines
BASE_URL = 'https://reqres.in/'
PATH_TO_RESP_FILE_GET = '../responses/responses_get.json'
PATH_TO_RESP_FILE_POST = '../responses/responses_post.json'
PASS_RESPONSE = 200
PASS_CREATE_RESPONSE = 201
ERR_RESPONSE = 404
ERR_MISS_PWD_RESPONSE = 400
DELETE_RESPONSE = 204

# Define json sections names
SINGLE_USER = 'single_user'
USERS_LIST = 'users_list'
EMPTY = 'empty'
LIST_RESOURCES = 'list_resources'
SINGLE_RESOURCE = 'single_resource'
DELAYED_RESPONSE = 'delayed_response'
CREATE = 'create'
REGISTER = 'register'
REGISTER_MISSING_PWD = 'missing_pwd'
LOGIN = 'login'


@pytest.fixture(scope="module", autouse=True)
def setup():
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


@pytest.fixture(scope='module', autouse=True)
def teardown():
    yield
    print("here is teardown operation")


@pytest.mark.parametrize(
    "test_url,request_name,test_name,test_vals",
    [('api/users/2', SINGLE_USER, 'get single user', [PASS_RESPONSE]),
     ('api/users?page=2', USERS_LIST, 'get users list', [PASS_RESPONSE]),
     ('/api/users/23', EMPTY, 'single user not found', [ERR_RESPONSE]),
     ('api/unknown', LIST_RESOURCES, 'list resources', [PASS_RESPONSE]),
     ('api/unknown/2', SINGLE_RESOURCE, 'single resource', [PASS_RESPONSE]),
     ('api/unknown/23', EMPTY, 'single resource not found', [ERR_RESPONSE]),
     ('/api/users?delay=3', DELAYED_RESPONSE, 'delayed response', [PASS_RESPONSE])
     ])
def test_get_request(test_url, request_name, test_name, test_vals):
    """
    Check GET request to test url with different combinations of input data
    :param test_url: the test url
    :param request_name: suburl for get request
    :param test_name: test name for print
    :param test_vals: expected response code
    :return: None
    """
    print(f"Performing {test_name} test")
    full_url = urllib.parse.urljoin(BASE_URL, test_url)
    expected_response = responses.get(GET)[request_name]
    response = requests.get(full_url)
    assert response.status_code == test_vals[0], f'Unexpected return code from get request: {full_url}'
    assert json.loads(response.text) == expected_response, 'Unexpected response'


create_request = {
    "name": "morpheus",
    "job": "leader"
}

register_request = {
    "email": "eve.holt@reqres.in",
    "password": "pistol"
}

register_w_pwd_request = {
    "email": "sydney@fife"
}

login_request = {
    "email": "eve.holt@reqres.in",
    "password": "cityslicka"
}

login_w_pwd_request = {
    "email": "peter@klaven"
}

update_user_request = {
    "name": "morpheus",
    "job": "zion resident"
}


@pytest.mark.parametrize(
    "test_url,request_name,test_name,expected_code,post_data",
    [('api/users', CREATE, 'create user', PASS_CREATE_RESPONSE, create_request),
     ('api/register', REGISTER, 'register user', PASS_RESPONSE, register_request),
     ('api/register', REGISTER_MISSING_PWD, 'register user without pwd', ERR_MISS_PWD_RESPONSE, register_w_pwd_request),
     ('api/login', LOGIN, 'login', PASS_RESPONSE, login_request),
     ('api/login', REGISTER_MISSING_PWD, 'login without pwd', ERR_MISS_PWD_RESPONSE, login_w_pwd_request)
     ])
def test_post_request(test_url, request_name, test_name, expected_code, post_data):
    """
    Check GET request to test url with different combinations of input data
    :param test_url: the test url
    :param request_name: suburl for get request
    :param test_name: test name for print
    :param expected_code: expected response code
    :param post_data: dict with post data
    :return: None
    """
    print(f"Performing {test_name} test")
    full_url = urllib.parse.urljoin(BASE_URL, test_url)
    response = requests.post(full_url, json=post_data)
    assert response.status_code == expected_code, f'Unexpected return code from get request: {full_url}'
    response_data = json.loads(response.text)
    if response_data.get('createdAt'):
        keys = post_data.keys()
        for key in keys:
            assert post_data.get(key) == response_data.get(key)
    else:
        expected_response = responses.get(POST)[request_name]
        assert response_data == expected_response, 'Unexpected response'


def test_put_request():
    """
    Check PUT request to test url
    :return: None
    """
    print(f"Performing update user test using put request")
    full_url = urllib.parse.urljoin(BASE_URL, 'api/users/2')
    response = requests.put(full_url, json=update_user_request)
    assert response.status_code == PASS_RESPONSE, f'Unexpected return code from get request: {full_url}'
    response_data = json.loads(response.text)
    keys = update_user_request.keys()
    for key in keys:
        assert update_user_request.get(key) == response_data.get(key)


def test_patch_request():
    """
    Check PATCH request to test url
    :return: None
    """
    print(f"Performing update user test using patch request")
    full_url = urllib.parse.urljoin(BASE_URL, 'api/users/2')
    response = requests.patch(full_url, json=update_user_request)
    assert response.status_code == PASS_RESPONSE, f'Unexpected return code from get request: {full_url}'
    response_data = json.loads(response.text)
    keys = update_user_request.keys()
    for key in keys:
        assert update_user_request.get(key) == response_data.get(key)


@pytest.mark.delete
def test_delete_request():
    """
    Check DELETE request to test url
    :return: None
    """
    print(f"Performing delete request")
    full_url = urllib.parse.urljoin(BASE_URL, 'api/users/2')
    response = requests.delete(full_url)
    assert response.status_code == DELETE_RESPONSE, f'Unexpected return code from get request: {full_url}'


if __name__ == '__main__':
    pytest.main()

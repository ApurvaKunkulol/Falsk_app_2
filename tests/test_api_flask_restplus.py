import json
import random
import string


# Tests for User creation.
def test_create_user_successful_post(mocker, api_client):
    """
        Description: With proper input.
    """
    first_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=7))
    last_name = "".join(random.choices(string.ascii_uppercase + string.digits, k=7))
    input_value = {
        "firstname": first_name,
        "lastname": last_name,
        "email": "{fname}.{lname}@gmail.com".format(fname=first_name, lname=last_name),
        "designation": "student",
        "address": "someplace, somecountry.",
        "website": "https://someURL.com",
        "qualification": "M. Phil (History)"
    }

    sample_result = api_client.post("/hello_api/create", data=json.dumps(input_value),
                                    headers={'Content-Type': 'application/json'})

    assert sample_result.json.get("status") == "success"


def test_create_user_no_input(mocker, api_client):
    """
        Description: No input provided.
    """
    sample_result = api_client.post("/hello_api/create", data="", headers={'Content-Type': 'application/json'})
    assert sample_result.json.get("status") == "error"


def test_create_user_witout_email(mocker, api_client):
    """
        Description: User information without email.
    """
    input_value = {
        "firstname": "xyz",
        "lastname": "lmn",
        "designation": "student",
        "address": "someplace, somecountry.",
        "website": "https://someURL.com",
        "qualification": "M. Phil (History)"
    }
    sample_result = api_client.post("/hello_api/create", data=json.dumps(input_value),
                                    headers={'Content-Type': 'application/json'})
    assert sample_result.json.get("status") == "error"


def test_create_user_with_existing_user(mocker, api_client):
    """
    Description: Testing the method by sending information of an already existing user.
    """
    input_value = {
        "firstname": "xyz",
        "lastname": "lmn",
        "email": "xyz.lmn@gmail.com",
        "designation": "student",
        "address": "someplace, somecountry.",
        "website": "https://someURL.com",
        "qualification": "M. Phil (History)"
    }
    sample_result = api_client.post("/hello_api/create", data=json.dumps(input_value),
                                    headers={'Content-Type': 'application/json'})
    assert sample_result.json.get("status") == "error"


# Test get, edit and delete functionalities.

def test_get_user_correct_input(mocker, api_client):
    """
        Description: Provide proper input and test whether the user is retrieved.
    """

    test_email = "xyz.lmn@gmail.com"
    sample_result = api_client.get("/hello_api/{}".format(test_email))
    sample_result = json.loads(sample_result.json)
    print("Sample Result: {}".format(sample_result))
    status = sample_result.get("status")
    assert status == "success"
    info = sample_result.get("user_info")
    assert info.get("firstname") == "xyz"
    assert info.get("lastname") == "lmn"


def test_get_user_no_existing_user(mocker, api_client):
    """
        Description: Should return error in case the user doesn't exist.
    """
    test_email = "firstname.lastname@gmail.com"
    sample_result = api_client.get("/hello_api/{}".format(test_email))
    status = sample_result.json.get("status")
    assert status == "error"
    description = sample_result.json.get("description")
    assert description == "No user found with the given email."


def test_get_user_improper_email(mocker, api_client):
    """
        Description: Should return error in case the email is not formatted properly.
    """
    test_email = "firstname.lastname_mail.com"
    sample_result = api_client.get("/hello_api/{}".format(test_email))
    status = sample_result.json.get("status")
    assert status == "error"
    description = sample_result.json.get("description")
    assert description == "Email is not in proper format."


def test_put_incorrect_email(mocker, api_client):
    """
    Description: Should return correct status after updation.
    """
    test_email = "xyz.lmn_mail.com"
    sample_result = api_client.put("/hello_api/{}".format(test_email))
    status = sample_result.json.get("status")
    assert status == "error"
    description = sample_result.json.get("description")
    assert description == "Email is not in proper format."


def test_put_no_user_info(mocker, api_client):
    """
    Description: Should return correct status after updation.
    """
    test_email = "xyz.lmn@gmail.com"

    sample_result = api_client.put("/hello_api/{}".format(test_email), data=json.dumps({}),
                                   headers={"Content-Type": "application/json"})
    status = sample_result.json.get("status")
    assert status == "error"
    description = sample_result.json.get("description")
    assert description == "Please supply information to update."


def test_put_correct_user_info(mocker, api_client):
    """
    Description: Should return correct status after updation.
    """
    test_email = "kunkulol.apurva@gmail.com"
    test_updated_info = {
        "updated_info": {
            "firstname" : "Apurva",
            "lastname" : "Kunkulol",
            "email": "kunkulol.apurva@gmail.com",
            "designation" : "Sr. Engineer",
            "address" : "India.",
            "website" : "https://someOtherURL.com",
            "qualification" : "M. Arch (Restoration Architecture)",
            "organisation": "ABC Surveyors and loss assesors."
        }
    }

    sample_result = api_client.put("/hello_api/{}".format(test_email), data=json.dumps(test_updated_info),
                                   headers={"Content-type": "application/json"})
    status = sample_result.json.get("status")
    assert status == "success"
    description = sample_result.json.get("description")
    assert description == "Record updated successfully."


def test_delete_correct_email(mocker, api_client):
    """
    Description: Test deletion with proper user info provided
    """
    test_email = "pqr.abc@gmail.com"
    input_value = {
        "firstname": "pqr",
        "lastname": "abc",
        "email": test_email,
        "designation": "student",
        "address": "someplace, somecountry.",
        "website": "https://someURL.com",
        "qualification": "M. Phil (History)"
    }

    api_client.post("/hello_api/create", data=json.dumps(input_value), headers={'Content-Type': 'application/json'})
    sample_result = api_client.delete("/hello_api/{}".format(test_email))
    status = sample_result.json.get("status")
    assert status == "success"
    description = sample_result.json.get("description")
    assert description == "Successfully deleted information for user {}.".format(test_email)


def test_delete_incorrect_email(mocker, api_client):
    """
    Description: Test deletion with proper user info provided
    """
    test_email = "pqr.abc_gmail.com"
    sample_result = api_client.delete("/hello_api/{}".format(test_email))
    status = sample_result.json.get("status")
    assert status == "error"
    description = sample_result.json.get("description")
    assert description == "Validation Error. There was an error validating the email {}".format(test_email)


def test_delete_no_user(mocker, api_client):
    """
    Description: Test deletion with proper user info provided
    """
    test_email = "pqr.ijh@gmail.com"
    sample_result = api_client.delete("/hello_api/{}".format(test_email))
    status = sample_result.json.get("status")
    assert status == "error"
    description = sample_result.json.get("description")
    assert description == "User does not exist for email {}.".format(test_email)




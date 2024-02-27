import json

import pytest

from trip_duration import app


@pytest.fixture()
def apigw_event_average_duration():
    """Generates API Gateway Event for GET /trip-durations/average"""
    return {
        "body": "",
        "resource": "/trip-durations/average",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/trip-durations/average",
            "httpMethod": "GET",
            "stage": "prod",
        },
        "queryStringParameters": {
            "startTime": "1698266696468",
            "endTime": "1698267092113",
        },
        "headers": {},
        "pathParameters": {},
        "httpMethod": "GET",
        "path": "/trip-durations/average",
    }


def test_average_trip_duration(apigw_event_average_duration):
    expected_response = {
        "averageDuration": "15 minutes",
        "totalTrips": 320,
        "queryParameters": {
            "startTime": "1698266696468",
            "endTime": "1698267092113",
        },
    }

    ret = app.lambda_handler(apigw_event_average_duration, "")
    actual_response = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert (
        actual_response == expected_response
    ), "The actual response does not match the expected response"

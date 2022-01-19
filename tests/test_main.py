from unittest.mock import patch

import pytest as pytest

import main


@pytest.mark.parametrize(
    "input_postcode, expected_output",
    [
        ("SN159AJ", "SN15"),
        ("SN15", "SN15"),
        ("SN15 9AJ", "SN15"),
        ("SN1 59AJ", "SN15"),
    ]
)
def test_get_outward_postcode(input_postcode, expected_output):
    assert main.get_outward_postcode(postcode=input_postcode) == expected_output


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data
    test_data = [
        {
            "url": "https://api.carbonintensity.org.uk/regional/postcode/AB1",
            "response": (MockResponse({"data": [{"data": [{"intensity": {"forecast": 111}}]}]}, 200))
        },
        {
            "url": "https://api.carbonintensity.org.uk/regional/intensity/2021-08-25T12:35Z/2021-08-26T12:35Z/"
                   "postcode/AB1",
            "response": (MockResponse({"data": [{"data": [{"intensity": {"forecast": 222}}]}]}, 200))
        },
    ]

    for data in test_data:
        if "url" in kwargs and kwargs["url"] == data["url"] or len(args) > 0 and args[0] == data["url"]:
            return data["response"]

    # Give some debug info
    print("GET args and kwargs", args, kwargs)
    return MockResponse(None, 404)


@patch("main.requests.get", side_effect=mocked_requests_get)
def test_get_intensity_for_postcode(mock_get):

    assert main.get_intensity_for_postcode(
        postcode="AB12CD"
    ) == 111
    assert main.get_intensity_for_postcode(
        postcode="AB1"
    ) == 111
    assert main.get_intensity_for_postcode(
        postcode="AB1",
        from_date="2021-08-25T12:35Z",
        to_date="2021-08-26T12:35Z"
    ) == 222



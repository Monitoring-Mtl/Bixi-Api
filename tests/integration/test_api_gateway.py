import pytest

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going
to test.
"""


class TestApiGateway:

    @pytest.fixture()
    def api_gateway_url(self):
        """Get the API Gateway URL from Cloudformation Stack outputs"""

    def test_api_gateway(self, api_gateway_url):
        """Call the API Gateway endpoint and check the response"""

from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


class ResponseBuilder(object):
    """API response builder."""

    def __init__(self):
        self.results = {}
        self.status_code = 1
        self.status_message = ""
        self.errors = ""
        self.status = status.HTTP_200_OK
        self.additional_details = {}

    def fail(self):
        self.status_code = -1
        return self

    """
    This enables app to handle messages differently
    than error code -1. In general cases use fail()
    only. Use this when you specifically wants app
    to handle this error message differently.
    """

    def fail_handle_differently(self):
        self.status_code = -2
        return self

    def message(self, status_message):
        self.status_message = status_message
        return self

    def error_message(self, status_message):
        self.errors = status_message
        return self

    def success(self):
        self.status_code = 1
        return self

    def ok_200(self):
        self.status = status.HTTP_200_OK
        return self

    def accepted_202(self):
        self.status = status.HTTP_202_ACCEPTED
        return self

    def not_found_404(self):
        self.status = status.HTTP_404_NOT_FOUND
        return self

    def bad_request_400(self):
        self.status = status.HTTP_400_BAD_REQUEST
        return self

    def user_unauthorized_401(self):
        self.status = status.HTTP_401_UNAUTHORIZED
        self.status_message = "User Unauthorized"
        return self

    def user_forbidden_403(self):
        self.status = status.HTTP_403_FORBIDDEN
        return self

    def internal_error_500(self):
        self.status = status.HTTP_500_INTERNAL_SERVER_ERROR
        return self

    def result_object(self, result, additional_details={}):
        self.results = result
        self.additional_details = additional_details
        return self

    def get_404_not_found_response(self, message):
        self.not_found_404()
        self.message(message)
        self.success()
        return self.get_response()

    def get_response(self):
        content = self.get_json()
        return Response(content, status=self.status)

    def get_json(self):
        response = {
            "status-code": self.status_code,
            "status-message": self.status_message,
            "errors": self.errors,
            "data": self.results,
        }

        if self.additional_details:
            response["additional_details"] = self.additional_details
        return response

    def get_json_response(self):
        content = self.get_json()
        return JsonResponse(content)

    def set_status(self, status):
        self.status = status
        return self

    @staticmethod
    def return_failed_json_response(message):
        return ResponseBuilder().ok_200().fail().message(message).get_json_response()

    def get_ok200_fail_response(self, message):
        return self.ok_200().fail().message(message).get_response()

    def get_success_200_response(self, message):
        return self.ok_200().success().message(message).get_response()

    def get_internal_server_error_500_response(self, message):
        return self.internal_error_500().fail().message(message).get_response()

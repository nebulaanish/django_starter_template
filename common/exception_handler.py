import logging
import traceback
from typing import Any, Dict

from rest_framework.response import Response
from rest_framework.views import exception_handler

from common.contants.exception_messges import exception_messages
from common.builders.response_builder import ResponseBuilder

logger = logging.getLogger(__name__)


def custom_exception_handler(exc: Exception, context: Dict[str, Any]) -> Response:
    """Handle custom exception for Django REST framework.

    Args
        exc (Exception): The exception that was raised.
        context (Dict[str, Any]): Additional context for the exception.

    Returns
        Response: The DRF response object with the custom error message.

    """
    response = exception_handler(exc, context)

    view = context.get("view", None)
    view_name = view.__class__.__name__ if view else "Unknown View"
    request = context.get("request", None)
    method = request.method if request else "Unknown Method"
    path = request.path if request else "Unknown Path"

    response_builder = ResponseBuilder()

    if response is not None:
        status_code = response.status_code
        default_message = str(exc)
    else:
        status_code = 500
        default_message = "An internal error occurred"

    details = getattr(exc, "detail", default_message)
    message = default_message
    exception_class = exc.__class__.__name__

    if exception_class in exception_messages:
        message = exception_messages[exception_class]
    response_builder.fail().set_status(status_code).message(message).error_message(
        details
    ).result_object(details)

    logger.error(
        "%s in %s [%s %s]: %s\n%s",
        message,
        view_name,
        method,
        path,
        details,
        traceback.format_exc(),
    )

    if response is not None:
        response_builder.set_status(response.status_code)
        response.data = response_builder.get_json()
    else:
        response = response_builder.get_response()

    return response

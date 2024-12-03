import logging
from typing import Any, Optional

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from common.builders.response_builder import ResponseBuilder

logger = logging.getLogger(__name__)


class CustomJSONRenderer(JSONRenderer):
    """Custom JSON Renderer to handle API response formatting."""

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[dict] = None,
    ) -> bytes:
        """Render the data into JSON format, using custom response formatting.

        Args
            data (Any): The response data to be rendered.
            accepted_media_type (Optional[str]): The accepted media type.
            renderer_context (Optional[dict]): The context for the renderer.

        Returns
            bytes: The rendered JSON response.

        """
        response_builder = ResponseBuilder()

        response: Response = renderer_context.get("response")
        response_status = response.status_code

        if response_status >= 400:
            return super().render(data, accepted_media_type, renderer_context)

        message = renderer_context.get("message", "")
        response_builder.success().message(message).result_object(data)

        if response_status == 200:
            response_builder.ok_200()
        elif response_status == 202:
            response_builder.accepted_202()

        logger.info("Message: %s", message)
        return super().render(
            response_builder.get_json(), accepted_media_type, renderer_context
        )

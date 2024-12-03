from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.contants.response_messges import RESPONSE_STATUS_MESSAGES


class BaseModelViewset(viewsets.ModelViewSet):
    permission_classes = []
    response_message_text = "base"

    def get_renderer_context(self):
        renderer_context = super().get_renderer_context()
        renderer_context["message"] = (
            RESPONSE_STATUS_MESSAGES.get(
                self.action, self.kwargs.get("renderer_message", "")
            )
            .format(self.response_message_text)
            .capitalize()
        )
        return renderer_context

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({}, status=status.HTTP_200_OK)


class HealthCheckView(APIView):
    serializer_class = None

    def get(self, request):
        """Check the health of the application."""
        return Response()

    def get_renderer_context(self):
        """Get the context to render the response."""
        renderer_context = super().get_renderer_context()
        renderer_context["message"] = "Health Check Passed"

        return renderer_context

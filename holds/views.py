from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import handler
from .serializers import (
    CaptureHoldSerializer,
    CreateHoldSerializer,
    HoldSerializer,
    ReleaseHoldSerializer
)

class CreateHoldView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateHoldSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hold = handler.create_hold_handler(
            actor_user=request.user,
            **serializer.validated_data,
        )

        response_serializer = HoldSerializer(hold)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

class ReleaseHoldView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, hold_id):
        serializer = ReleaseHoldSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hold = handler.release_hold_handler(
            actor_user=request.user,
            hold_id=hold_id,
            **serializer.validated_data,
        )

        response_serializer = HoldSerializer(hold)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

class CaptureHoldView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, hold_id):
        serializer = CaptureHoldSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hold = handler.capture_hold_handler(
            actor_user=request.user,
            hold_id=hold_id,
            **serializer.validated_data,
        )

        response_serializer = HoldSerializer(hold)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
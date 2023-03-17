from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event, Performence
from events.serializers import (
    EventSerializer,
    ExportEventSerializer,
    PerformenceSerializer,
)
from events.tasks import export_events


class CreateEventView(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class UpdateEventView(UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


@method_decorator(cache_page(settings.CACHE_TIME), "get")
class ListEventView(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


@method_decorator(cache_page(settings.CACHE_TIME), "get")
@extend_schema(
    parameters=[
        OpenApiParameter(
            "sort",
            description="Order of sorting for performence entries",
            required=False,
            type=str,
        )
    ]
)
class RetriveEventView(RetrieveAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        asc = self.request.GET.get("sort", True)
        sort_by = "start" if asc else "-start"
        return Event.objects.all().order_by("start", f"performences__{sort_by}")


@method_decorator(cache_page(settings.CACHE_TIME), "get")
class PerformenceView(ListAPIView):
    queryset = Performence.objects.all()
    serializer_class = PerformenceSerializer


class ExportEventsView(APIView):
    serializer_class = ExportEventSerializer

    def post(self, request):
        export_events.delay(request.data["url"])
        return Response({"status": "generating csv file"})


class ManagePerformeceView(CreateAPIView, UpdateAPIView, DestroyAPIView):
    queryset = Performence.objects.all()
    serializer_class = PerformenceSerializer

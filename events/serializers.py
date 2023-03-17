from rest_framework.serializers import CharField, ModelSerializer, Serializer

from events.models import Artist, Event, Performence


class ArtistSerializer(ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class PerformenceSerializer(ModelSerializer):
    artist = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = Performence
        fields = "__all__"


class EventSerializer(ModelSerializer):
    performences = PerformenceSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ["performences", "name", "start", "end"]


class ExportEventSerializer(Serializer):
    url = CharField()

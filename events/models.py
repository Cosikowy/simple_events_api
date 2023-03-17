from django.core.exceptions import ValidationError
from django.db import models


class DatesMixin(models.Model):
    start = models.DateTimeField(blank=True)
    end = models.DateTimeField(blank=True)

    class Meta:
        abstract = True

    def clean(self):
        if self.start > self.end:
            raise ValidationError("Start date must be before end date")


class MusicGenres(models.TextChoices):
    rock = "rock", "rock music"
    alternative = "alternative", "alternative music"
    hardstyle = "hardstyle", "hardstyle music"
    hardcore = "hardcore", "hardcore music"
    lofi = "lofi", "lofi music"


# Create your models here.
class Event(DatesMixin, models.Model):
    name = models.CharField(max_length=100, verbose_name="Event name", unique=True)

    def __str__(self) -> str:
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=100, verbose_name="Artist name", unique=True)
    music_genre = models.CharField(
        max_length=100,
        verbose_name="Music genre",
        blank=True,
        null=True,
        choices=MusicGenres.choices,
    )

    def __str__(self) -> str:
        return self.name


class Performence(DatesMixin, models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="performences"
    )
    artist = models.ManyToManyField(Artist, related_name="performences")

    def __str__(self) -> str:
        return f"{self.event.name} {self.start} - {self.end} with {[s.name for s in self.artist.all()]}"

    def save(self, **kwargs):
        event = self.event
        if self.start < event.start:
            raise ValidationError("Start date must be equal or after event starts")
        if self.end > event.end:
            raise ValidationError("End date must be equal or before event ends")
        performences = list(self.event.performences.all().order_by("start"))
        performences.append(self)
        performences.sort(key=lambda x: x.start)
        if len(performences) > 0:
            self.validate_overlaping(performences)
        return super().save(**kwargs)

    def validate_overlaping(self, performences):
        for idx, obj in enumerate(performences[1:], 1):
            prev = performences[idx - 1]
            if prev.end > obj.start:
                raise ValidationError("Perfomences can not overlap")

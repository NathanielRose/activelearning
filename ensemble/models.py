import math
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class MediaFile(models.Model):
    """A media file which can be labelled or made predictions against"""

    name = models.CharField(unique=True, max_length=255)
    url = models.CharField(unique=True, max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Subtitle(models.Model):
    """Optional subtitles for a MediaFile"""

    name = models.CharField(unique=True, max_length=255, null=False)
    url = models.CharField(unique=True, max_length=255, null=False)
    media_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)


class Classification(models.Model):
    """A classification which an object can be labelled as in a MediaFile"""

    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name


################################################################################
# Labels
################################################################################


def generate_timecode(ms: int) -> str:
    """
    Convert a duration in seconds to ISO8601 hh:mm:ss.sss format
    """
    hours = math.floor(ms / (60 * 60 * 1000))
    minutes = math.floor(ms / (60 * 1000)) % 60
    seconds = math.floor(ms / 1000) % 60
    milliseconds = ms % 1000
    return (
        str(hours).rjust(2, "0")
        + ":"
        + str(minutes).rjust(2, "0")
        + ":"
        + str(seconds).rjust(2, "0")
        + "."
        + str(milliseconds).rjust(3, "0")
    )


class Label(models.Model):
    """Abstract base class for a Label
    https://docs.djangoproject.com/en/2.1/topics/db/models/#abstract-base-classes
    Contains information which all label types should carry
    """

    class Meta:
        abstract = True

    media_file = models.ForeignKey(MediaFile, on_delete=models.CASCADE)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE)
    file = models.CharField(max_length=255, null=True, blank=True)


class AudioLabel(Label):
    """
    A 3D label which instead of using a 3D segment of a single frame (impossible
    with audio), captures a series of frames of time.
    """

    time = models.IntegerField(
        validators=[MinValueValidator(0)], verbose_name="Time (milliseconds)"
    )
    duration = models.IntegerField(validators=[MinValueValidator(0)])

    def timecode(self):
        return generate_timecode(self.time)

    def __str__(self):
        return (
            str(self.classification)
            + "_"
            + generate_timecode(self.time)
            + "-"
            + generate_timecode(self.time + self.duration)
        )


class ImageLabel(Label):
    """
    A 3D bounding box for a single image
    """

    x = models.FloatField(validators=[MinValueValidator(0)])
    y = models.FloatField(validators=[MinValueValidator(0)])
    width = models.FloatField(validators=[MinValueValidator(0)])
    height = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return (
            str(self.classification)
            + "_"
            + str(self.x)
            + "_"
            + str(self.y)
            + "_"
            + str(self.width)
            + "_"
            + str(self.height)
        )


class VideoLabel(ImageLabel):
    """
    An image label which belongs to a single frame of a timed media (video)
    """

    time = models.IntegerField(
        validators=[MinValueValidator(0)], verbose_name="Time (milliseconds)"
    )

    def timecode(self):
        return generate_timecode(self.time)

    def __str__(self):
        return (
            str(self.classification)
            + "_"
            + str(self.time)
            + "_"
            + str(self.x)
            + "_"
            + str(self.y)
            + "_"
            + str(self.width)
            + "_"
            + str(self.height)
        )


################################################################################
# Models
################################################################################
class Model(models.Model):
    """
    Any model currently available to the Ensemble
    """

    name = models.CharField(unique=True, max_length=255)
    classifications = models.ManyToManyField(Classification)

    def __str__(self):
        return self.name


class ModelVersion(models.Model):
    """
    Represents the state/version of a given model.
    Capturing the meta-information about a model as it changes of time/training.
    """

    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    version = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return str(self.model) + "_" + str(self.version)


################################################################################
# Prediction
################################################################################
class Prediction(models.Model):
    """
    A prediction is a label with additional information.
    There is a prediction type for every kind of label
    - The ModelVersion it was generated from
    - The confidence of the prediction
    """

    class Meta:
        abstract = True

    confidence = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(1)]
    )
    model_version = models.ForeignKey(ModelVersion, on_delete=models.CASCADE)

    def __str__(self):
        return super().__str__() + self.confidence


class ImagePrediction(ImageLabel, Prediction):  # type: ignore
    pass


class VideoPrediction(VideoLabel, Prediction):  # type: ignore
    pass


class AudioPrediction(AudioLabel, Prediction):  # type: ignore
    pass

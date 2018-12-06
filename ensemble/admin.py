from django.contrib import admin

from .models import (
    AudioLabel,
    AudioPrediction,
    Classification,
    ImageLabel,
    ImagePrediction,
    MediaFile,
    Model,
    ModelVersion,
    VideoPrediction,
    Subtitle,
)

# Register your models here.
admin.site.register(AudioPrediction)
admin.site.register(Classification)
admin.site.register(ImagePrediction)
admin.site.register(MediaFile)
admin.site.register(Model)
admin.site.register(ModelVersion)
admin.site.register(VideoPrediction)
admin.site.register(Subtitle)

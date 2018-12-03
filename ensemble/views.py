import json
import os
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import MediaFile, ImagePrediction, AudioPrediction, VideoPrediction

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the labels index.")


def predictions(request, prediction_id: int):
    response = "response for prediction %s"
    return HttpResponse(response % prediction_id)


def files_index(request):
    file_list = get_list_or_404(MediaFile)
    context = {"file_list": file_list}
    return render(request, "media_files/index.html", context)


def files_show(request, file_id: int):
    file = get_object_or_404(MediaFile, pk=file_id)
    # image_labels = file.imagelabel_set.all()
    # imageprediction_set.all() will not work here because of the way the predictions sub-class labels

    image_predictions = ImagePrediction.objects.filter(media_file__id=file_id)
    video_predictions = VideoPrediction.objects.filter(media_file__id=file_id)
    audio_predictions = AudioPrediction.objects.filter(media_file__id=file_id)
    data = {
        "title": file.name,
        "sourceUrl": file.url,
        "predictions": sorted(
            [
                {
                    "confidence": p.confidence,
                    "classifier": p.classification.name,
                    "x": p.x,
                    "y": p.y,
                    "width": p.width,
                    "height": p.height,
                }
                for p in image_predictions
            ]
            + [
                {
                    "confidence": p.confidence,
                    "classifier": p.classification.name,
                    "time": p.time,
                    "x": p.x,
                    "y": p.y,
                    "width": p.width,
                    "height": p.height,
                }
                for p in video_predictions
            ]
            + [
                {
                    "confidence": p.confidence,
                    "classifier": p.classification.name,
                    "time": p.time,
                    "duration": p.duration,
                }
                for p in audio_predictions
            ],
            key=lambda p: p["time"],
        ),
    }

    return render(
        request,
        "media_files/show.html",
        {
            "file": file,
            "image_predictions": image_predictions,
            "audio_predictions": audio_predictions,
            "video_predictions": video_predictions,
            "data": data,
        },
    )

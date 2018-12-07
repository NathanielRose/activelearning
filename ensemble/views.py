import json
import os
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    MediaFile,
    ImagePrediction,
    AudioPrediction,
    VideoPrediction,
    VideoLabel,
    AudioLabel,
    Subtitle,
)

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

    video_labels = VideoLabel.objects.filter(
        media_file__id=file_id, videoprediction__isnull=True
    )
    audio_labels = AudioLabel.objects.filter(
        media_file__id=file_id, audioprediction__isnull=True
    )
    image_predictions = ImagePrediction.objects.filter(media_file__id=file_id)
    video_predictions = VideoPrediction.objects.filter(media_file__id=file_id)
    audio_predictions = AudioPrediction.objects.filter(media_file__id=file_id)
    subtitles = Subtitle.objects.filter(media_file__id=file_id)
    data = {
        "title": file.name,
        "subtitles": [s for s in subtitles],
        "labels": [
            {
                "classifier": l.classification.name,
                "time": l.time,
                "x": l.x,
                "y": l.y,
                "width": l.width,
                "height": l.height,
            }
            for l in video_labels
        ]
        + [
            {
                "classifier": l.classification.name,
                "time": l.time,
                "duration": l.duration,
            }
            for l in audio_labels
        ],
        "predictions": sorted(
            [
                {
                    "confidence": p.confidence,
                    "classifier": p.classification.name,
                    "model": str(p.model_version),
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
                    "model": str(p.model_version),
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
                    "model": str(p.model_version),
                    "time": p.time,
                    "duration": p.duration,
                }
                for p in audio_predictions
            ],
            key=lambda p: p["time"],
        ),
    }
    if file.url:
        data["sourceUrl"] = file.url

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


def files_compare(request, file_id: int):
    file = get_object_or_404(MediaFile, pk=file_id)

    # Ground truths
    ground_truth_timecodes = {}
    for label in list(
        VideoLabel.objects.filter(media_file__id=file_id, videoprediction__isnull=True)
    ) + list(
        AudioLabel.objects.filter(media_file__id=file_id, audioprediction__isnull=True)
    ):
        timecode = label.timecode()
        if timecode not in ground_truth_timecodes:
            ground_truth_timecodes[timecode] = []
        label_data = {
            "type": "audio" if hasattr(label, "duration") else "video",
            "file": label.file,
            "tag": label.classification.name,
        }
        if hasattr(label, "duration"):
            label_data["duration"] = label.duration
        else:
            label_data["box"] = {
                "x1": label.x,
                "y1": label.y,
                "x2": label.x + label.width,
                "y2": label.y + label.height,
            }
        ground_truth_timecodes[timecode].append(label_data)

    # Predictions
    video_predictions = VideoPrediction.objects.filter(media_file__id=file_id)
    audio_predictions = AudioPrediction.objects.filter(media_file__id=file_id)

    model_versions = list(
        set(
            [p.model_version for p in video_predictions]
            + [p.model_version for p in audio_predictions]
        )
    )

    predictions_data = []
    for model_version in model_versions:
        is_video_model = (
            VideoPrediction.objects.filter(
                media_file__id=file_id, model_version__id=model_version.id
            ).count()
            > 0
        )
        timecodes = {}

        for prediction in list(
            VideoPrediction.objects.filter(
                media_file__id=file_id, model_version__id=model_version.id
            )
        ) + list(
            AudioPrediction.objects.filter(
                media_file__id=file_id, model_version__id=model_version.id
            )
        ):
            timecode = prediction.timecode()
            if timecode not in timecodes:
                timecodes[timecode] = []
            prediction_dict = {
                "file": prediction.file,
                "tag": prediction.classification.name,
                "score": prediction.confidence,
            }
            if hasattr(prediction, "duration"):
                prediction_dict["duration"] = prediction.duration
            else:
                prediction_dict["box"] = (
                    {
                        "x1": prediction.x,
                        "x2": prediction.width + prediction.x,
                        "y1": prediction.y,
                        "y2": prediction.height + prediction.y,
                    },
                )
            timecodes[timecode].append(prediction_dict)

        inference_data = {
            "title": file.name,
            "url": file.url,
            "modelType": model_version.model.name,
            "modelVersion": model_version.version,
            "modelDescription": model_version.description,
            "modelClass": "video" if is_video_model else "audio",
            "timecodes": timecodes,
        }
        predictions_data.append(inference_data)

    return JsonResponse(
        {
            "groundTruth": {
                "title": file.name,
                "url": file.url,
                "timecodes": ground_truth_timecodes,
            },
            "predictions": predictions_data,
        }
    )

"""
Command to parse and add an ensemble JSON to the database.
Any Models, ModelVersions, Classifications, Predictions/Lables, will be created if needed.
"""

import json
from django.core.management.base import BaseCommand
from ensemble.models import (
    Classification,
    Model,
    ModelVersion,
    MediaFile,
    VideoLabel,
    AudioLabel,
    VideoPrediction,
    AudioPrediction,
)


class Command(BaseCommand):
    help = "Import an Ensemble JSON into database"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("json-path", nargs="+", type=str)

    def handle(self, *args, **options):
        # print(args)
        # print(options)
        def timecode_to_ms(timecode):
            """Convert a timecode in format <hr>:<min>:<secs>.<ms> to number of milliseconds"""
            parts = timecode.split(":")
            hours = int(parts[0]) * 3600000
            minutes = int(parts[1]) * 60000
            milliseconds = float(parts[2]) * 1000
            return hours + minutes + milliseconds

        for path in options["json-path"]:
            with open(path) as json_data:
                j = json.load(json_data)

                # Create/Get MediaFile
                movie, _ = MediaFile.objects.update_or_create(
                    name=j["title"],
                    defaults={
                        "url": j["url"] if "url" in j else None,
                        "description": j["description"] if "description" in j else None,
                    },
                )

                if "modelType" in j:
                    # Inference Flow
                    model, _ = Model.objects.get_or_create(name=j["modelType"])
                    model_version, _ = ModelVersion.objects.get_or_create(
                        model=model,
                        version=j["modelVersion"] if "modelVersion" in j else None,
                        description=j["modelDescription"]
                        if "modelDescription" in j
                        else None,
                    )

                    for timecode, predictions in j["timecodes"].items():
                        for p in predictions:
                            classification, _ = Classification.objects.get_or_create(
                                name=p["tag"]
                            )
                            model.classifications.add(classification)
                            is_video = True if "box" in p else False

                            if is_video:
                                box = p["box"]
                                video_p = VideoPrediction.objects.create(
                                    media_file=movie,
                                    file=p["file"] if p["file"] else None,
                                    classification=classification,
                                    confidence=float(p["score"]),
                                    model_version=model_version,
                                    time=timecode_to_ms(timecode),
                                    x=float(box["x1"]) if box else 0,
                                    y=float(box["y1"]) if box else 0,
                                    width=(float(box["x2"]) - float(box["x1"]))
                                    if box
                                    else 0,
                                    height=(float(box["y2"]) - float(box["y1"]))
                                    if box
                                    else 0,
                                )
                                print("Created VideoPrediction: " + str(video_p))
                            else:
                                audio_p = AudioPrediction.objects.create(
                                    media_file=movie,
                                    file=p["file"] if p["file"] else None,
                                    classification=classification,
                                    confidence=float(p["score"]),
                                    model_version=model_version,
                                    time=timecode_to_ms(timecode),
                                    duration=10000,
                                )
                                print("Created AudioPrediction: " + str(audio_p))
                else:
                    # Ground-truth flow
                    for timecode, predictions in j["timecodes"].items():
                        for p in predictions:
                            classification, _ = Classification.objects.get_or_create(
                                name=p["tag"]
                            )
                            is_video = True if "box" in p else False
                            if is_video:
                                box = p["box"]
                                video_label = VideoLabel.objects.create(
                                    media_file=movie,
                                    file=p["file"] if p["file"] else None,
                                    classification=classification,
                                    time=timecode_to_ms(timecode),
                                    x=float(box["x1"]) if box else 0,
                                    y=float(box["y1"]) if box else 0,
                                    width=(float(box["x2"]) - float(box["x1"]))
                                    if box
                                    else 0,
                                    height=(float(box["y2"]) - float(box["y1"]))
                                    if box
                                    else 0,
                                )
                                print("Created VideoLabel: " + str(video_label))
                            else:
                                audio_label = AudioLabel.objects.create(
                                    media_file=movie,
                                    file=p["file"] if p["file"] else None,
                                    classification=classification,
                                    time=timecode_to_ms(timecode),
                                    duration=10000,
                                )
                                print("Created AudioLabel: " + str(audio_label))

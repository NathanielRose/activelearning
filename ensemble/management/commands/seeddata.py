"""
Test data scaffolding.
Read: https://docs.djangoproject.com/en/dev/howto/custom-management-commands/
"""
import json
from random import randint
from django.core.management.base import BaseCommand, CommandError
from ensemble.models import (
    Classification,
    Model,
    ModelVersion,
    MediaFile,
    VideoPrediction,
    AudioPrediction,
)


class Command(BaseCommand):
    help = "Scaffold some test data for ensemble"

    def handle(self, *args, **options):
        gunshot = Classification(name="GUNSHOT")
        gunshot.save()
        audioset_model = Model(name="audioset")
        audioset_model.save()
        audioset_model.classifications.add(gunshot)
        audioset_model_trained = ModelVersion(
            model=audioset_model, version="0.01alpha2"
        )
        audioset_model_trained.save()

        for movie in json.loads(self.__movie_json, strict=False):
            media_file = MediaFile(
                name=movie["title"],
                url=movie["sources"][0],
                description=movie["description"],
            )
            media_file.save()

            video_predictions = [
                self.__generate_random_video_prediction(
                    media_file, gunshot, audioset_model_trained
                )
                for _ in range(1000)
            ]
            audio_predictions = [
                self.__generate_random_audio_prediction(
                    media_file, gunshot, audioset_model_trained
                )
                for _ in range(1000)
            ]

            # VideoPrediction.objects.bulk_create(video_predictions)
            # AudioPrediction.objects.bulk_create(audio_predictions)
            for prediction in video_predictions + audio_predictions:
                prediction.save()

    def __generate_random_video_prediction(self, media_file, classification, model):
        """
        Generate a random gunshot video prediction for the video
        """
        x = randint(0, 1280)
        y = randint(0, 720)
        width = randint(1, 1280 - x + 1)
        height = randint(1, 720 - y + 1)
        return VideoPrediction(
            media_file=media_file,
            classification=classification,
            confidence=randint(0, 100),
            model_version=model,
            time=randint(0, 600000),
            x=x,
            y=y,
            width=width,
            height=height,
        )

    def __generate_random_audio_prediction(self, media_file, classification, model):
        """
        Generate a random 10 second audio prediction for a gunshot
        """
        return AudioPrediction(
            media_file=media_file,
            classification=classification,
            confidence=randint(0, 100),
            model_version=model,
            time=randint(0, 600000),
            duration="10000",
        )

    __movie_json = """
    [
    {
        "description": "Big Buck Bunny tells the story of a giant rabbit with a heart bigger than himself. When one sunny day three rodents rudely harass him, something snaps... and the rabbit ain't no bunny anymore! In the typical cartoon tradition he prepares the nasty rodents a comical revenge.\n\nLicensed under the Creative Commons Attribution license\nhttp://www.bigbuckbunny.org",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
        ],
        "subtitle": "By Blender Foundation",
        "thumb": "images/BigBuckBunny.jpg",
        "title": "Big Buck Bunny"
    },
    {
        "description": "The first Blender Open Movie from 2006",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"
        ],
        "subtitle": "By Blender Foundation",
        "thumb": "images/ElephantsDream.jpg",
        "title": "Elephant Dream"
    },
    {
        "description": "HBO GO now works with Chromecast -- the easiest way to enjoy online video on your TV. For when you want to settle into your Iron Throne to watch the latest episodes. For $35.\nLearn how to use Chromecast with HBO GO and more at google.com/chromecast.",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
        ],
        "subtitle": "By Google",
        "thumb": "images/ForBiggerBlazes.jpg",
        "title": "For Bigger Blazes"
    },
    {
        "description": "Introducing Chromecast. The easiest way to enjoy online video and music on your TV—for when Batman's escapes aren't quite big enough. For $35. Learn how to use Chromecast with Google Play Movies and more at google.com/chromecast.",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"
        ],
        "subtitle": "By Google",
        "thumb": "images/ForBiggerEscapes.jpg",
        "title": "For Bigger Escape"
    },
    {
        "description": "Introducing Chromecast. The easiest way to enjoy online video and music on your TV. For $35.  Find out more at google.com/chromecast.",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"
        ],
        "subtitle": "By Google",
        "thumb": "images/ForBiggerFun.jpg",
        "title": "For Bigger Fun"
    },
    {
        "description": "Introducing Chromecast. The easiest way to enjoy online video and music on your TV—for the times that call for bigger joyrides. For $35. Learn how to use Chromecast with YouTube and more at google.com/chromecast.",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4"
        ],
        "subtitle": "By Google",
        "thumb": "images/ForBiggerJoyrides.jpg",
        "title": "For Bigger Joyrides"
    },
    {
        "description": "Introducing Chromecast. The easiest way to enjoy online video and music on your TV—for when you want to make Buster's big meltdowns even bigger. For $35. Learn how to use Chromecast with Netflix and more at google.com/chromecast.",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4"
        ],
        "subtitle": "By Google",
        "thumb": "images/ForBiggerMeltdowns.jpg",
        "title": "For Bigger Meltdowns"
    },
    {
        "description": "Sintel is an independently produced short film, initiated by the Blender Foundation as a means to further improve and validate the free/open source 3D creation suite Blender. With initial funding provided by 1000s of donations via the internet community, it has again proven to be a viable development model for both open 3D technology as for independent animation film.\nThis 15 minute film has been realized in the studio of the Amsterdam Blender Institute, by an international team of artists and developers. In addition to that, several crucial technical and creative targets have been realized online, by developers and artists and teams all over the world.\nwww.sintel.org",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4"
        ],
        "subtitle": "By Blender Foundation",
        "thumb": "images/Sintel.jpg",
        "title": "Sintel"
    },
    {
        "description": "Smoking Tire takes the all-new Subaru Outback to the highest point we can find in hopes our customer-appreciation Balloon Launch will get some free T-shirts into the hands of our viewers.",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4"
        ],
        "subtitle": "By Garage419",
        "thumb": "images/SubaruOutbackOnStreetAndDirt.jpg",
        "title": "Subaru Outback On Street And Dirt"
    },
    {
        "description": "Tears of Steel was realized with crowd-funding by users of the open source 3D creation tool Blender. Target was to improve and test a complete open and free pipeline for visual effects in film - and to make a compelling sci-fi film in Amsterdam, the Netherlands.  The film itself, and all raw material used for making it, have been released under the Creatieve Commons 3.0 Attribution license. Visit the tearsofsteel.org website to find out more about this, or to purchase the 4-DVD box with a lot of extras.  (CC) Blender Foundation - http://www.tearsofsteel.org",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4"
        ],
        "subtitle": "By Blender Foundation",
        "thumb": "images/TearsOfSteel.jpg",
        "title": "Tears of Steel"
    },
    {
        "description": "The Smoking Tire heads out to Adams Motorsports Park in Riverside, CA to test the most requested car of 2010, the Volkswagen GTI. Will it beat the Mazdaspeed3's standard-setting lap time? Watch and see...",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/VolkswagenGTIReview.mp4"
        ],
        "subtitle": "By Garage419",
        "thumb": "images/VolkswagenGTIReview.jpg",
        "title": "Volkswagen GTI Review"
    },
    {
        "description": "The Smoking Tire is going on the 2010 Bullrun Live Rally in a 2011 Shelby GT500, and posting a video from the road every single day! The only place to watch them is by subscribing to The Smoking Tire or watching at BlackMagicShine.com",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4"
        ],
        "subtitle": "By Garage419",
        "thumb": "images/WeAreGoingOnBullrun.jpg",
        "title": "We Are Going On Bullrun"
    },
    {
        "description": "The Smoking Tire meets up with Chris and Jorge from CarsForAGrand.com to see just how far $1,000 can go when looking for a car.The Smoking Tire meets up with Chris and Jorge from CarsForAGrand.com to see just how far $1,000 can go when looking for a car.",
        "sources": [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WhatCarCanYouGetForAGrand.mp4"
        ],
        "subtitle": "By Garage419",
        "thumb": "images/WhatCarCanYouGetForAGrand.jpg",
        "title": "What care can you get for a grand?"
    }
    ]
    """

from django.test import TestCase
from .models import MediaFile, Classification, Model, ModelVersion

# Create your tests here.


class HelloWorldTestCase(TestCase):
    def setUp(self):
        MediaFile.objects.create(name="Deadpool 1", url="/some/local/video1.mp4")
        MediaFile.objects.create(name="Deadpool 2", url="/some/local/video2.mp4")
        gunshot = Classification.objects.create(name="gunshot")
        lstm = Model.objects.create(name="AudioSet LSTM")
        transfer = Model.objects.create(name="AudioSet LSTM Transfer Learning")
        lstm.classifications.add(gunshot)
        transfer.classifications.add(gunshot)

    def test_model_classification_relation(self):
        """Both models have a gunshot classifier"""
        lstm = Model.objects.get(name="AudioSet LSTM")
        transfer = Model.objects.get(name="AudioSet LSTM Transfer Learning")
        gunshot = Classification.objects.get(name="gunshot")
        self.assertTrue(lstm.classifications.all()[0] == gunshot)
        self.assertTrue(transfer.classifications.all()[0] == gunshot)

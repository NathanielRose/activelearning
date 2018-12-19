from django.core.management.base import BaseCommand, CommandError
from subprocess import call
from os import path


class Command(BaseCommand):
    help = "Build the front end for the ensemble visualization (REQUIRED for visualization to work)."

    def handle(self, *args, **options):
        ensemble_path = path.join("ensemble", "static", "ensemble", "foxmovieensemble")
        # Install node_modules
        call(["npm", "--prefix", ensemble_path, "install"])

        # production build
        call(["npm", "run", "--prefix", ensemble_path, "build"])

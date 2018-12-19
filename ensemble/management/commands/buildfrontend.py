from django.core.management.base import BaseCommand, CommandError
from subprocess import run
import os
from os import path


class Command(BaseCommand):
    help = "Build the front end for the ensemble visualization (REQUIRED for visualization to work)."

    def handle(self, *args, **options):
        ensemble_path = path.join(
            os.getcwd(), "ensemble", "static", "ensemble", "foxmovieensemble"
        )
        # Install node_modules
        run("npm install", cwd=ensemble_path, shell=True)

        # production build
        run("npm run build", cwd=ensemble_path, shell=True)

from django.core.management.base import BaseCommand, CommandError
from subprocess import call


class Command(BaseCommand):
    help = "Build the front end for the ensemble visualization (REQUIRED for visualization to work)."

    def handle(self, *args, **options):
        # Install node_modules
        call(
            ["npm", "--prefix", "ensemble/static/ensemble/foxmovieensemble", "install"]
        )

        # production build
        call(
            [
                "npm",
                "run",
                "--prefix",
                "ensemble/static/ensemble/foxmovieensemble",
                "build",
            ]
        )

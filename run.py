import os
import sys
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Inspektorat-Prov.-Sultra.settings")

def main():
    execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8000"])

if __name__ == "__main__":
    main()


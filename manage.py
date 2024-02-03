#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import find_dotenv, load_dotenv
import environ

load_dotenv(find_dotenv())


def main():
    """Run administrative tasks."""
    configuration = os.getenv("ENV", "development").title()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", configuration)

    if configuration in ("Local", "Dev"):
        environ.Env.read_env("config/envs/.env.dev")
    elif configuration in ("Staging", "Beta"):
        environ.Env.read_env("config/envs/.env.staging")
    elif configuration in ("Prod", "Production"):
        environ.Env.read_env("config/envs/.env.prod")
    else:
        print("Unable to get .env file for that environment!")
        sys.exit(1)

    try:
        print(f"loading {configuration} settings, sit tight :) ...")
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

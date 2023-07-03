# Invisible East - Django Project

This document outlines key concepts of the Django project and is primarily designed for technical staff working on the development of the project (e.g. software engineers and system admins).


## Django Project

The project is called 'invisible-east-website', but project files are stored in the 'core' folder. Please refer to core/settings.py for further details.


## Django Apps

Apps include:

- **account** - custom user accounts and auth (overrides the default Django account and auth functionality)
- **general** - this is for general sections of the website that don't require a data model (e.g. about page, cookies page, accessibility page, etc.)
- **corpus** - the main project data, managed via the admin dashboard and presented to users through a public interface
- **help** - content to help users to use the website, e.g. PDFs with screenshots, video tutorials, etc.


## Django Admin

The provided Django Admin feature is utilised within this Django project, to allow the research project team to perform CRUD operations on the database using an intuitive web interface.


## Unit Tests

There are a series of automated unit tests located in each Django app folder as 'tests.py'

To prepare the project for testing with test data:

- Create a directory called 'fixtures' in each Django app directory
- For each app, run: python manage.py dumpdata [app name] > [app name]/fixtures/testdata.json

To perform the tests:

- Run: python manage.py test
- Use the feedback given by Django for any failed tests to fix issues
- Repeat this until returns a 100% pass rate


## PEP8 and Flake8

This project should comply with PEP8, which is tested using Flake8:

- Run 'pip install flake8' to install (if not already installed)
- cd to project root directory and run 'flake8' to perform the tests
- There's a .flake8 file in the repo root directory, used to customise Flake8 tests


## Database

This project is designed to work with a PostgreSQL database. Remember to name this database in local_settings.py (see Settings section of this document for more details)


## Settings

There are 2 settings related files:

- settings.py (for general project settings, regardless of environment and containing publicly accessible information)
- local_settings.py (for settings specific to that environment (e.g. dev/test/production) and for private information (e.g. API keys))

local_settings.py is ignored from Git as it contains private information that shouldn't be shared with others. Instead, the file local_settings.example.py is stored in Git to show you what information your own local_settings.py needs to contain. local_settings.test.py is used in the CI and should never be used on a production system. The steps you must take to configure local_settings.py are:

- Create a local_settings.py file
- Copy and paste the content from local_settings.example.py into local_settings.py
- Customise this content by following the guide in local_settings.example.py
- Do not delete or modify local_settings.example.py, as this will be kept in Git to help others

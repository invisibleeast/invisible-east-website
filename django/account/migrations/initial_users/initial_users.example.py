# Copy this initial_users.example.py file within this initial_users dir as initial_users.py

"""
A list of default users to add to the database upon initial creation

This data is used in account/migrations/0002_initial_data.py

Data is kept in this separate file to keep users' details confidental
as this file is ignored from git
"""

from django.contrib.auth.hashers import make_password

TEMP_PW = make_password('SET_A_DEFAULT_PASSWORD')

# Example users - replace with actual users (or leave as an empty list if not needed)
INITIAL_USERS = [
    {
        "first_name": "Joe",
        "last_name": "Bloggs",
        "email": "joe.bloggs@uni.ac.uk",
        "role": "admin",
        "password": TEMP_PW
    },
    {
        "first_name": "Jane",
        "last_name": "Bloggs",
        "email": "jane.bloggs@uni.ac.uk",
        "role": "collaborator",
        "password": TEMP_PW
    },
]

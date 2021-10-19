from rest_framework.validators import ValidationError
import re
from django.conf import settings
import requests


pattern = r'^(\+?998)?([. \-])?(9[0-9])([. \-])?(\d){3}([. \-])?(\d){2}([. \-])?(\d){2}$'


def validate_phone_number(phone_number):
    '''Function that checks if given phone number valid
    Depends on [re - python regular expression library]
        - returns False if phone number is not correct and msg
        - returns True if phone number is correect and msg is the phone number given
    '''
    if not phone_number:
        raise ValidationError("phone number cannot be null")

    if not re.match(pattern, phone_number):
        raise ValidationError("phone number did not match the pattern!")
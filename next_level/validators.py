from django.core.exceptions import ValidationError


def validate_all_characters_is_alphanumeric(value):
    for ch in value:
        if not ch.isalnum() and ch != ' ':
            raise ValidationError('Title must contain only letters and digits!')


def validate_post_title_contains_only_allowed_characters(value):
    allowed_characters = [',', '-', '(', ')', "'"]

    for ch in value:
        if not ch.isalnum() and ch != ' ' and ch not in allowed_characters:
            raise ValidationError("Title must contain only letters and digits or any of these symbols ,-()'")


def validate_username_contains_allowed_characters(value):

    for character in value:
        if not character.isalnum() and character != '-' and character != '_':
            raise ValidationError('Username must contain only letters, digits, "-" and "_"')


def validate_names_contain_only_letters(value):
    for character in value:
        if not character.isalpha():
            raise ValidationError('Names must contain only letters')


def validate_image_sile_less_than_5mb(image_object):
    if image_object.size > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")

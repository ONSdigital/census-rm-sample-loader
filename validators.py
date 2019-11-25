from typing import Iterable


class Invalid(Exception):
    pass


def max_length(max_len: int):
    def validate(value):
        if len(value) > max_len:
            raise Invalid(f'Value has length {len(value)}, exceeds maximum length of {max_len}')

    return validate


def unique():
    previous_values = set()

    def validate(value):
        if value in previous_values:
            raise Invalid(f'Value "{value}" is not unique')
        previous_values.add(value)

    return validate


def mandatory():
    def validate(value):
        if not value:
            raise Invalid(f'Empty mandatory value')

    return validate


def numeric():
    def validate(value):
        if value and not value.isnumeric():
            raise Invalid(f'Value "{value}" is non numeric')

    return validate


def latitude_longitude(max_precision: int, max_scale: int):
    def validate(value):
        try:
            float(value)
        except ValueError:
            raise Invalid(f'Value "{value}" is not a valid float')
        integer, decimal = value.split('.')
        integer = integer.strip('-')
        scale = len(decimal)
        precision = len(integer) + len(decimal)
        errors = []
        if precision > max_precision:
            errors.append(f'Value has precision {precision}, exceeds max of {max_precision}')
        if scale > max_scale:
            errors.append(f'Value has scale {scale}, exceeds max of {max_scale}')
        if errors:
            raise Invalid(f"{','.join(errors)}, Value = {value}")

    return validate


def in_set(valid_value_set: set):
    def validate(value):
        if value not in valid_value_set:
            raise Invalid(f'Value "{value}" is not valid')

    return validate


def set_equal(expected_set):
    def validate(value: Iterable) -> None:
        value_as_set = set(value)
        if value_as_set != expected_set:
            raise Invalid((f"Values don't match expected set, "
                           f'missing values: {expected_set.difference(value_as_set)}, '
                           f'unexpected values: {value_as_set.difference(expected_set)}'))

    return validate

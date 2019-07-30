from typing import Iterable


class ValidationError(Exception):
    pass


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Validator:
    def __call__(self, value) -> None:
        return self.validate(value)

    def validate(self, value) -> None:
        pass


class MaxLength(Validator):
    def __init__(self, max_length):
        self.max_length = max_length

    def validate(self, value):
        if not len(value) <= self.max_length:
            raise ValidationError(f'Value has length {len(value)}, exceeds maximum length of {self.max_length}')


class Unique(Validator):
    def __init__(self):
        self.previous_values = set()

    def validate(self, value):
        if value in self.previous_values:
            raise ValidationError(f'Value "{value}" is not unique')
        self.previous_values.add(value)


class Mandatory(Validator, metaclass=Singleton):
    def validate(self, value):
        if not value:
            raise ValidationError(f'Empty mandatory value')


class IsNumeric(Validator, metaclass=Singleton):
    def validate(self, value):
        if value and not value.isnumeric():
            raise ValidationError(f'Value "{value}" is non numeric')


class IsFloat(Validator, metaclass=Singleton):
    def validate(self, value) -> None:
        try:
            float(value)
        except ValueError:
            raise ValidationError(f'Value "{value}" is not a valid float')


class MaxDecimalPrecision(Validator):
    def __init__(self, max_decimal_precision):
        self.max_decimal_precision = max_decimal_precision

    def validate(self, value) -> None:
        integer, decimal = value.split('.')
        integer = integer.strip('-')
        precision = len(integer) + len(decimal)
        if precision > self.max_decimal_precision:
            raise ValidationError(
                f'Value {value} as a precision of {precision},'
                f' exceeds max of {self.max_decimal_precision}')


class MaxDecimalScale(Validator):
    def __init__(self, max_decimal_scale):
        self.max_decimal_scale = max_decimal_scale

    def validate(self, value) -> None:
        scale = len(value.split('.')[1])
        if scale > self.max_decimal_scale:
            raise ValidationError(
                f'Value {value} as a scale of {scale},'
                f' exceeds max of {self.max_decimal_scale}')


class InSet(Validator):
    def __init__(self, valid_value_set):
        self.value_set = valid_value_set

    def validate(self, value) -> None:
        if value not in self.value_set:
            raise ValidationError(f'Value "{value}" is not valid')


class SetEqual(Validator):
    def __init__(self, expected_set):
        self.expected_set = expected_set

    def validate(self, value: Iterable) -> None:
        value_as_set = set(value)
        if value_as_set != self.expected_set:
            raise ValidationError((f"Values don't match expected set, "
                                   f'missing values: {self.expected_set.difference(value_as_set)},'
                                   f' unexpected values: {value_as_set.difference(self.expected_set)}'))

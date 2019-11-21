from validr import validator, Invalid, Compiler


class ValidationError(Exception):
    pass


@validator(accept=str, output=str)
def numeric_str_validator(compiler, maxlen=None, minlen=0):
    def validate(value):
        if maxlen:
            assert len(value) <= maxlen
        assert len(value) >= minlen
        if value and not value.isnumeric():
            raise Invalid(f'Value "{value}" is non numeric')

    return validate


@validator(accept=str, output=str)
def in_set_validator(compiler, items):
    item_set = set(items.split(','))

    def validate(value):
        if value in item_set:
            return value
        raise Invalid(f'value must be one of {item_set}')

    return validate


@validator(accept=str, output=str)
def globally_unique_str_validator(compiler, maxlen=None, minlen=0):
    previous_values = set()

    def validate(value):
        if maxlen:
            assert len(value) <= maxlen
        assert len(value) >= minlen
        if value in previous_values:
            raise Invalid(f'Value "{value}" is not unique')
        previous_values.add(value)

    return validate


COMPILER = Compiler(validators={
    "numeric_str": numeric_str_validator,
    "in_set": in_set_validator,
    "globally_unique_str": globally_unique_str_validator,
})

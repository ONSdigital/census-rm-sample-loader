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


@validator(accept=str, output=str)
def decimal_validator(compiler, max_scale=None, max_precision=None):
    def validate(value):
        integer, decimal = value.split('.')
        scale = len(decimal)
        integer = integer.strip('-')
        precision = len(integer) + len(decimal)
        failures = []
        if precision > max_precision:
            failures.append(f'Value {value} has precision {precision}, exceeds max of {max_precision}')
        if scale > max_scale:
            failures.append(f'Value {value} has scale {scale}, exceeds max of {max_scale}')
        if failures:
            raise Invalid(', '.join(failures))

    return validate


COMPILER = Compiler(validators={
    "numeric_str": numeric_str_validator,
    "in_set": in_set_validator,
    "globally_unique_str": globally_unique_str_validator,
    "decimal": decimal_validator,
})

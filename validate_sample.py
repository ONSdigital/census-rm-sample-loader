import argparse
import csv

ARID = set()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    return parser.parse_args()


def validate_sample_file(sample_file_path):
    with open(sample_file_path) as sample_file:
        return load_sample(sample_file)


def load_sample(sample_file):
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    for count, sample_row in enumerate(sample_file_reader, 2):
        validate_arid(count, sample_row)
        validate_estab_arid(count, sample_row)
        validate_uprn(count, sample_row)
        validate_address_type(count, sample_row)
        validate_estab_type(count, sample_row)
        validate_address_level(count, sample_row)
        validate_abp_code(count, sample_row)
        validate_org_name(count, sample_row)
        validate_address_line(count, sample_row)
        validate_town_name(count, sample_row)
        validate_postcode(count, sample_row)


def validate_arid(count, sample_row):
    arid = sample_row['ARID']
    maximum_length = 21
    _check_length('ARID', arid, count, maximum_length)
    if sample_row['ARID'] in ARID:
        print(f'Line {count}: ARID: {arid} is duplicated in sample file.')
    else:
        ARID.add(sample_row['ARID'])


def validate_estab_arid(count, sample_row):
    estab_arid = sample_row['ESTAB_ARID']
    maximum_length = 21
    _check_length('ESTAB_ARID', estab_arid, count, maximum_length)


def validate_uprn(count, sample_row):
    uprn = sample_row['UPRN']
    maximum_length = 12
    _check_length('UPRN', uprn, count, maximum_length)
    if not uprn.isnumeric():
        print(f'Line {count}: UPRN: {uprn} is not a valid integer.')


def validate_address_type(count, sample_row):
    address_type = sample_row['ADDRESS_TYPE']
    maximum_length = 3
    _check_length('ADDRESS_TYPE', address_type, count, maximum_length)
    if address_type not in {"HH", "CE", "SPG"}:
        print(f'Line {count}: ADDRESS_TYPE: {address_type} is not valid.')


def validate_estab_type(count, sample_row):
    estab_type = sample_row['ESTAB_TYPE']
    maximum_length = 30
    _check_length('ESTAB_TYPE', estab_type, count, maximum_length)


def validate_address_level(count, sample_row):
    address_level = sample_row['ADDRESS_LEVEL']
    maximum_length = 1
    _check_length('ADDRESS_LEVEL', address_level, count, maximum_length)
    if address_level not in {"E", "U"}:
        print(f'Line {count}: ADDRESS_LEVEL: {address_level} is not valid.')


def validate_abp_code(count, sample_row):
    abp_code = sample_row['ABP_CODE']
    maximum_length = 6
    _check_length('ABP_CODE', abp_code, count, maximum_length)


def validate_org_name(count, sample_row):
    org_name = sample_row['ORGANISATION_NAME']
    maximum_length = 60
    _check_length('ORGANISATION_NAME', org_name, count, maximum_length)


def validate_address_line(count, sample_row):
    maximum_length = 60
    for column in ['ADDRESS_LINE1', 'ADDRESS_LINE2', 'ADDRESS_LINE3']:
        address_line = sample_row[column]
        _check_length(column, address_line, count, maximum_length)


def validate_town_name(count, sample_row):
    town_name = sample_row['TOWN_NAME']
    maximum_length = 30
    _check_length('TOWN_NAME', town_name, count, maximum_length)


def validate_postcode(count, sample_row):
    postcode = sample_row['POSTCODE']
    maximum_length = 8
    _check_length('POSTCODE', postcode, count, maximum_length)


def _check_length(name, value, count, maximum_length):
    if len(value) > maximum_length:
        print(f'Line {count}: {name}: {value} exceeds maximum length of {maximum_length}.')


def main():
    args = parse_arguments()
    validate_sample_file(args.sample_file_path)


if __name__ == "__main__":
    main()

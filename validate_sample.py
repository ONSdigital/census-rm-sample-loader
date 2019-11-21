import argparse
import csv
from collections import namedtuple

from validators import MaxLength, Unique, ValidationError, Mandatory, IsNumeric, InSet, SetEqual, IsFloat, \
    MaxDecimalScale, MaxDecimalPrecision

ARID = set()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    return parser.parse_args()


args = parse_arguments()

ESTAB_TYPES = {
    'Household',
    'Sheltered Accommodation',
    'Hall of Residence',
    'Care Home',
    'Boarding School',
    'Hotel',
    'Hostel',
    'Residential Caravanner',
    'Gypsy Roma Traveller',
    'Residential Boater'}

TREATMENT_CODES = {
    'HH_LF2R1E', 'HH_LF2R2E', 'HH_LF2R3AE', 'HH_LF2R3BE', 'HH_LF3R1E', 'HH_LF3R2E', 'HH_LF3R3AE', 'HH_LF3R3BE',
    'HH_LFNR1E', 'HH_LFNR2E', 'HH_LFNR3AE', 'HH_LFNR3BE', 'HH_LF2R1W', 'HH_LF2R2W', 'HH_LF2R3AW', 'HH_LF2R3BW',
    'HH_LF3R1W', 'HH_LF3R2W', 'HH_LF3R3AW', 'HH_LF3R3BW', 'HH_LFNR1W', 'HH_LFNR2W', 'HH_LFNR3AW', 'HH_LFNR3BW',
    'HH_1LSFN', 'HH_2LEFN', 'HH_QF2R1E', 'HH_QF2R2E', 'HH_QF2R3AE', 'HH_QF3R1E', 'HH_QF3R2E', 'HH_QF3R3AE',
    'HH_QFNR1E', 'HH_QFNR2E', 'HH_QFNR3AE', 'HH_QF2R1W', 'HH_QF2R2W', 'HH_QF2R3AW', 'HH_QF3R1W', 'HH_QF3R2W',
    'HH_QF3R3AW', 'HH_QFNR1W', 'HH_QFNR2W', 'HH_QFNR3AW', 'HH_3QSFN'}

COLUMN_VALIDATORS = {
    'ARID': (Mandatory(), MaxLength(21), Unique()),
    'ESTAB_ARID': (Mandatory(), MaxLength(21)),
    'UPRN': (Mandatory(), MaxLength(12), IsNumeric()),
    'ADDRESS_TYPE': (Mandatory(), InSet({"HH", "CE", "SPG"})),
    'ESTAB_TYPE': (Mandatory(), InSet(ESTAB_TYPES)),
    'ADDRESS_LEVEL': (Mandatory(), InSet({'E', 'U'})),
    'ABP_CODE': (Mandatory(), MaxLength(6)),
    'ORGANISATION_NAME': (MaxLength(60),),
    'ADDRESS_LINE1': (Mandatory(), MaxLength(60)),
    'ADDRESS_LINE2': (MaxLength(60),),
    'ADDRESS_LINE3': (MaxLength(60),),
    'TOWN_NAME': (Mandatory(), MaxLength(30)),
    'POSTCODE': (Mandatory(), MaxLength(8)),
    'LATITUDE': (Mandatory(), IsFloat(), MaxDecimalScale(7), MaxDecimalPrecision(9)),
    'LONGITUDE': (Mandatory(), IsFloat(), MaxDecimalScale(7), MaxDecimalPrecision(10)),
    'OA': (Mandatory(), MaxLength(9)),
    'LSOA': (Mandatory(), MaxLength(9)),
    'MSOA': (Mandatory(), MaxLength(9)),
    'LAD': (Mandatory(), MaxLength(9)),
    'REGION': (Mandatory(), MaxLength(9)),
    'HTC_WILLINGNESS': (Mandatory(), MaxLength(9), InSet({'0', '1', '2', '3', '4', '5'})),
    'HTC_DIGITAL': (Mandatory(), MaxLength(9), InSet({'0', '1', '2', '3', '4', '5'})),
    'FIELDCOORDINATOR_ID': (MaxLength(7),),
    'FIELDOFFICER_ID': (MaxLength(10),),
    'TREATMENT_CODE': (Mandatory(), MaxLength(10), InSet(TREATMENT_CODES)),
    'CE_EXPECTED_CAPACITY': (MaxLength(4), IsNumeric()),
}

ValidationFailure = namedtuple('ValidationFailure', ('line_number', 'column', 'description'))


def validate_fieldnames(fieldnames):
    valid_header = set(COLUMN_VALIDATORS.keys())
    try:
        SetEqual(valid_header)(fieldnames)
    except ValidationError as err:
        return ValidationFailure(1, None, str(err))


def find_validation_failures(sample_file_reader) -> list:
    failures = []
    for line_number, row in enumerate(sample_file_reader, 2):
        failures.extend(find_row_validation_failures(line_number, row))
    return failures


def find_row_validation_failures(line_number, row):
    failures = []
    for column, validators in COLUMN_VALIDATORS.items():
        for validator in validators:
            try:
                validator(row[column])
            except ValidationError as validation_failure:
                failures.append(ValidationFailure(line_number, column, validation_failure))
    return failures


def validate_sample_file(sample_file_path) -> list:
    try:
        with open(sample_file_path, encoding="utf-8") as sample_file:
            sample_file_reader = csv.DictReader(sample_file, delimiter=',')
            header_failures = validate_fieldnames(sample_file_reader.fieldnames)
            if header_failures:
                return [header_failures]
            return find_validation_failures(sample_file_reader)
    except UnicodeDecodeError as err:
        return [ValidationFailure(None, None, f'Invalid file encoding, requires utf-8, error: {err}')]


def main():
    failures = validate_sample_file(args.sample_file_path)
    if failures:
        print(f'{len(failures)} validation failure(s):')
        for failure in failures:
            failure_log = (f'line: {failure.line_number}, column: {failure.column}, description: {failure.description}'
                           if failure.column else
                           f'line: Header, description: {failure.description}'
                           if failure.line_number else
                           failure.description)
            print(failure_log)
        print(f'{args.sample_file_path} is not valid ❌')
        exit(1)
    print(f'Success! {args.sample_file_path} passed validation ✅')


if __name__ == "__main__":
    main()

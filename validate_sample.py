import argparse
import csv
from collections import namedtuple

from validr import T, Invalid

from validators import ValidationError, COMPILER

ARID = set()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    return parser.parse_args()


ESTAB_TYPES = ','.join({
    'Household',
    'Sheltered Accommodation',
    'Hall of Residence',
    'Care Home',
    'Boarding School',
    'Hotel',
    'Hostel',
    'Residential Caravanner',
    'Gypsy Roma Traveller',
    'Residential Boater'})

TREATMENT_CODES = ','.join({
    'HH_LF2R1E', 'HH_LF2R2E', 'HH_LF2R3AE', 'HH_LF2R3BE', 'HH_LF3R1E', 'HH_LF3R2E', 'HH_LF3R3AE', 'HH_LF3R3BE',
    'HH_LFNR1E', 'HH_LFNR2E', 'HH_LFNR3AE', 'HH_LFNR3BE', 'HH_LF2R1W', 'HH_LF2R2W', 'HH_LF2R3AW', 'HH_LF2R3BW',
    'HH_LF3R1W', 'HH_LF3R2W', 'HH_LF3R3AW', 'HH_LF3R3BW', 'HH_LFNR1W', 'HH_LFNR2W', 'HH_LFNR3AW', 'HH_LFNR3BW',
    'HH_1LSFN', 'HH_2LEFN', 'HH_QF2R1E', 'HH_QF2R2E', 'HH_QF2R3AE', 'HH_QF3R1E', 'HH_QF3R2E', 'HH_QF3R3AE',
    'HH_QFNR1E', 'HH_QFNR2E', 'HH_QFNR3AE', 'HH_QF2R1W', 'HH_QF2R2W', 'HH_QF2R3AW', 'HH_QF3R1W', 'HH_QF3R2W',
    'HH_QF3R3AW', 'HH_QFNR1W', 'HH_QFNR2W', 'HH_QFNR3AW', 'HH_3QSFN'})

SAMPLE_ROW_VALIDATOR = COMPILER.compile(
    T.dict(
        ARID=T.globally_unique_str.minlen(1).maxlen(21),
        ESTAB_ARID=T.str.minlen(1).maxlen(21),
        UPRN=T.numeric_str.minlen(1).maxlen(12),
        ADDRESS_TYPE=T.in_set("HH,CE,SPG"),
        ESTAB_TYPE=T.in_set(ESTAB_TYPES),
        ADDRESS_LEVEL=T.in_set('E,U'),
        ABP_CODE=T.str.minlen(1).maxlen(6),
        ORGANISATION_NAME=T.str.optional(True).maxlen(60),
        ADDRESS_LINE1=T.str.minlen(1).maxlen(60),
        ADDRESS_LINE2=T.str.optional(True).maxlen(60),
        ADDRESS_LINE3=T.str.optional(True).maxlen(60),
        TOWN_NAME=T.str.minlen(1).maxlen(30),
        POSTCODE=T.str.minlen(1).maxlen(8),
        LATITUDE=T.float,  # (Mandatory(), IsFloat(), MaxDecimalScale(7), MaxDecimalPrecision(9)),
        LONGITUDE=T.float,  # (Mandatory(), IsFloat(), MaxDecimalScale(7), MaxDecimalPrecision(10)),
        OA=T.str.minlen(1).maxlen(9),
        LSOA=T.str.minlen(1).maxlen(9),
        MSOA=T.str.minlen(1).maxlen(9),
        LAD=T.str.minlen(1).maxlen(9),
        REGION=T.str.minlen(1).maxlen(9),
        HTC_WILLINGNESS=T.in_set('0,1,2,3,4,5'),
        HTC_DIGITAL=T.in_set('0,1,2,3,4,5'),
        FIELDCOORDINATOR_ID=T.str.optional(True).maxlen(7),
        FIELDOFFICER_ID=T.str.optional(True).maxlen(10),
        TREATMENT_CODE=T.in_set(TREATMENT_CODES),
        CE_EXPECTED_CAPACITY=T.numeric_str.optional(True).maxlen(4),
    )
)

ValidationFailure = namedtuple('ValidationFailure', ('line_number', 'description'))


def validate_fieldnames(fieldnames):
    valid_header = {'ARID', 'ESTAB_ARID', 'UPRN', 'ADDRESS_TYPE', 'ESTAB_TYPE', 'ADDRESS_LEVEL', 'ABP_CODE',
                    'ORGANISATION_NAME', 'ADDRESS_LINE1', 'ADDRESS_LINE2', 'ADDRESS_LINE3', 'TOWN_NAME', 'POSTCODE',
                    'LATITUDE', 'LONGITUDE', 'OA', 'LSOA', 'MSOA', 'LAD', 'REGION', 'HTC_WILLINGNESS',
                    'HTC_DIGITAL', 'FIELDCOORDINATOR_ID', 'FIELDOFFICER_ID', 'TREATMENT_CODE',
                    'CE_EXPECTED_CAPACITY'}

    try:
        valid_header == fieldnames
    except ValidationError as err:
        return ValidationFailure(1, str(err))


def find_validation_failures(sample_file_reader) -> list:
    failures = []
    for line_number, row in enumerate(sample_file_reader, 2):
        failures.extend(find_row_validation_failures(line_number, row))
        if not line_number % 10000:
            print(f"Validation progress: {str(line_number).rjust(9)} lines checked, "
                  f"Failures: {len(failures)}", end='\r', flush=True)
    return failures


def find_row_validation_failures(line_number, row):
    failures = []
    try:
        SAMPLE_ROW_VALIDATOR(row)
    except Invalid as validation_failure:
        failures.append(ValidationFailure(line_number, validation_failure))
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
        return [ValidationFailure(None, f'Invalid file encoding, requires utf-8, error: {err}')]


def main():
    args = parse_arguments()
    failures = validate_sample_file(args.sample_file_path)
    if failures:
        print(f'{len(failures)} validation failure(s):')
        for failure in failures:
            failure_log = (f'line: {failure.line_number}, description: {failure.description}'
                           if failure.line_number else
                           failure.description)
            print(failure_log)
        print(f'{args.sample_file_path} is not valid ❌')
        exit(1)
    print(f'Success! {args.sample_file_path} passed validation ✅')


if __name__ == "__main__":
    main()

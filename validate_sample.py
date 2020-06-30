import argparse
import csv
from collections import namedtuple

from validators import max_length, Invalid, mandatory, numeric, in_set, latitude_longitude, set_equal, \
    no_padding_whitespace, region_matches_treatment_code, ce_u_has_expected_capacity, estab_type_in_list

ValidationFailure = namedtuple('ValidationFailure', ('line_number', 'column', 'description'))


class SampleValidator:
    TREATMENT_CODES = {
        'HH_LF2R1E', 'HH_LF2R2E', 'HH_LF2R3AE', 'HH_LF2R3BE', 'HH_LF3R1E', 'HH_LF3R2E', 'HH_LF3R3AE', 'HH_LF3R3BE',
        'HH_LFNR1E', 'HH_LFNR2E', 'HH_LFNR3AE', 'HH_LFNR3BE', 'HH_LF2R1W', 'HH_LF2R2W', 'HH_LF2R3AW', 'HH_LF2R3BW',
        'HH_LF3R1W', 'HH_LF3R2W', 'HH_LF3R3AW', 'HH_LF3R3BW', 'HH_LFNR1W', 'HH_LFNR2W', 'HH_LFNR3AW', 'HH_LFNR3BW',
        'HH_1LSFN', 'HH_2LEFN', 'HH_QF2R1E', 'HH_QF2R2E', 'HH_QF2R3AE', 'HH_QF3R1E', 'HH_QF3R2E', 'HH_QF3R3AE',
        'HH_QFNR1E', 'HH_QFNR2E', 'HH_QFNR3AE', 'HH_QF2R1W', 'HH_QF2R2W', 'HH_QF2R3AW', 'HH_QF3R1W', 'HH_QF3R2W',
        'HH_QF3R3AW', 'HH_QFNR1W', 'HH_QFNR2W', 'HH_QFNR3AW', 'HH_3QSFN', 'SPG_QDHSE', 'SPG_QDHSW', 'SPG_LPHUE',
        'SPG_QDHUE', 'SPG_VDNEE', 'CE_QDIEE', 'SPG_VDNEW', 'CE_QDIEW', 'SPG_LPHUW', 'SPG_QDHUW', 'CE_LDIUE', 'CE_LDIUW'}

    def __init__(self):
        self.schema = {
            'UPRN': [mandatory(), max_length(12), numeric(), no_padding_whitespace()],
            'ESTAB_UPRN': [mandatory(), max_length(12), numeric(), mandatory(), no_padding_whitespace()],
            'ADDRESS_TYPE': [mandatory(), in_set({'HH', 'CE', 'SPG'}), no_padding_whitespace()],
            'ESTAB_TYPE': [mandatory(), estab_type_in_list(), max_length(255), no_padding_whitespace()],
            'ADDRESS_LEVEL': [mandatory(), in_set({'E', 'U'}), no_padding_whitespace()],
            'ABP_CODE': [mandatory(), max_length(6), no_padding_whitespace()],
            'ORGANISATION_NAME': [max_length(60), no_padding_whitespace()],
            'ADDRESS_LINE1': [mandatory(), max_length(60), no_padding_whitespace()],
            'ADDRESS_LINE2': [max_length(60), no_padding_whitespace()],
            'ADDRESS_LINE3': [max_length(60), no_padding_whitespace()],
            'TOWN_NAME': [mandatory(), max_length(30), no_padding_whitespace()],
            'POSTCODE': [mandatory(), max_length(8), no_padding_whitespace()],
            'LATITUDE': [mandatory(), latitude_longitude(max_scale=7, max_precision=9), no_padding_whitespace()],
            'LONGITUDE': [mandatory(), latitude_longitude(max_scale=7, max_precision=10), no_padding_whitespace()],
            'OA': [mandatory(), max_length(9), no_padding_whitespace()],
            'LSOA': [mandatory(), max_length(9), no_padding_whitespace()],
            'MSOA': [mandatory(), max_length(9), no_padding_whitespace()],
            'LAD': [mandatory(), max_length(9), no_padding_whitespace()],
            'REGION': [mandatory(), max_length(9), no_padding_whitespace(), region_matches_treatment_code()],
            'HTC_WILLINGNESS': [mandatory(), in_set({'0', '1', '2', '3', '4', '5'}), no_padding_whitespace()],
            'HTC_DIGITAL': [mandatory(), in_set({'0', '1', '2', '3', '4', '5'}), no_padding_whitespace()],
            'FIELDCOORDINATOR_ID': [max_length(10), no_padding_whitespace()],
            'FIELDOFFICER_ID': [max_length(13), no_padding_whitespace()],
            'TREATMENT_CODE': [mandatory(), in_set(self.TREATMENT_CODES), no_padding_whitespace()],
            'CE_EXPECTED_CAPACITY': [numeric(), max_length(4), no_padding_whitespace(), ce_u_has_expected_capacity()],
            'CE_SECURE': [mandatory(), in_set({'0', '1'}), no_padding_whitespace()],
            'PRINT_BATCH': [numeric(), max_length(2), no_padding_whitespace()]
        }

    def find_header_validation_failures(self, header):
        valid_header = set(self.schema.keys())
        try:
            set_equal(valid_header)(header)
        except Invalid as invalid:
            return ValidationFailure(line_number=1, column=None, description=str(invalid))

    def find_row_validation_failures(self, line_number, row):
        failures = []
        for column, validators in self.schema.items():
            for validator in validators:
                try:
                    validator(row[column], row=row)
                except Invalid as invalid:
                    failures.append(ValidationFailure(line_number, column, invalid))
        return failures

    def find_sample_validation_failures(self, sample_file_reader) -> list:
        failures = []
        for line_number, row in enumerate(sample_file_reader, 2):
            failures.extend(self.find_row_validation_failures(line_number, row))
            if not line_number % 10000:
                print(f"Validation progress: {str(line_number).rjust(8)} lines checked, "
                      f"Failures: {len(failures)}", end='\r', flush=True)
        print(f"Validation progress: {str(line_number).rjust(8)} lines checked, "
              f"Failures: {len(failures)}")
        return failures

    def validate(self, sample_file_path) -> list:
        try:
            with open(sample_file_path, encoding="utf-8") as sample_file:
                sample_file_reader = csv.DictReader(sample_file, delimiter=',')
                header_failures = self.find_header_validation_failures(sample_file_reader.fieldnames)
                if header_failures:
                    return [header_failures]
                return self.find_sample_validation_failures(sample_file_reader)
        except UnicodeDecodeError as err:
            return [
                ValidationFailure(line_number=None, column=None,
                                  description=f'Invalid file encoding, requires utf-8, error: {err}')]


def build_failure_log(failure):
    return (f'line: {failure.line_number}, column: {failure.column}, description: {failure.description}'
            if failure.column else
            f'line: Header, description: {failure.description}'
            if failure.line_number else
            failure.description)


def print_failures_summary(failures, print_limit):
    for failure in failures[:print_limit]:
        print(build_failure_log(failure))
    response = input(f'Showing first {print_limit} of {len(failures)}. '
                     f'Show remaining {len(failures) - print_limit} [Y/n]?\n')
    if response.lower() in {'y', 'yes'}:
        for failure in failures[print_limit:]:
            print(build_failure_log(failure))


def print_failures(failures, print_limit=20):
    print(f'{len(failures)} validation failure(s):')
    if len(failures) > print_limit:
        print_failures_summary(failures, print_limit)
    else:
        for failure in failures:
            print(build_failure_log(failure))


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    return parser.parse_args()


def main():
    args = parse_arguments()
    failures = SampleValidator().validate(args.sample_file_path)
    if failures:
        print_failures(failures)
        print(f'{args.sample_file_path} is not valid ❌')
        exit(1)
    print(f'Success! {args.sample_file_path} passed validation ✅')


if __name__ == "__main__":
    main()

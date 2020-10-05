import argparse
import csv
from collections import namedtuple

from validators import max_length, Invalid, mandatory, numeric, in_set, latitude_longitude, set_equal, \
    no_padding_whitespace, region_matches_treatment_code, ce_u_has_expected_capacity, \
    ce_e_has_expected_capacity, alphanumeric_postcode, no_pipe_character, latitude_longitude_range, \
    alphanumeric_plus_hyphen_field_values

ValidationFailure = namedtuple('ValidationFailure', ('line_number', 'column', 'description'))


class SampleValidator:
    TREATMENT_CODES = {
        'HH_LP1E', 'HH_LP1W', 'HH_LP2E', 'HH_LP2W', 'HH_QP3E', 'HH_QP3W', 'HH_1ALSFN', 'HH_2BLEFN',
        'HH_2CLEFN', 'HH_3DQSFN', 'HH_3EQSFN', 'HH_3FQSFN', 'HH_3GQSFN', 'HH_4HLPCVN', 'HH_SPGLNFN', 'HH_SPGQNFN',
        'CE_LDIEE', 'CE_LDIEW', 'CE_LDIUE', 'CE_LDIUW', 'CE_QDIEE', 'CE_QDIEW', 'CE_LDCEE', 'CE_LDCEW',
        'CE_1QNFN', 'CE_2LNFN', 'CE_3LSNFN', 'SPG_LPHUE', 'SPG_LPHUW', 'SPG_QDHUE', 'SPG_QDHUW', 'SPG_VDNEE',
        'SPG_VDNEW'}

    ESTAB_TYPES = {'HALL OF RESIDENCE', 'CARE HOME', 'HOSPITAL', 'HOSPICE', 'MENTAL HEALTH HOSPITAL',
                   'MEDICAL CARE OTHER', 'BOARDING SCHOOL', 'LOW/MEDIUM SECURE MENTAL HEALTH',
                   'HIGH SECURE MENTAL HEALTH', 'HOTEL', 'YOUTH HOSTEL', 'HOSTEL', 'MILITARY SLA', 'MILITARY US SLA',
                   'RELIGIOUS COMMUNITY', 'RESIDENTIAL CHILDRENS HOME', 'EDUCATION OTHER', 'PRISON',
                   'IMMIGRATION REMOVAL CENTRE', 'APPROVED PREMISES', 'ROUGH SLEEPER', 'STAFF ACCOMMODATION',
                   'CAMPHILL', 'HOLIDAY PARK', 'HOUSEHOLD', 'SHELTERED ACCOMMODATION', 'RESIDENTIAL CARAVAN',
                   'RESIDENTIAL BOAT', 'GATED APARTMENTS', 'MOD HOUSEHOLDS', 'FOREIGN OFFICES', 'CASTLES', 'GRT SITE',
                   'MILITARY SFA', 'EMBASSY', 'ROYAL HOUSEHOLD', 'CARAVAN', 'MARINA', 'TRAVELLING PERSONS',
                   'TRANSIENT PERSONS', 'MIGRANT WORKERS', 'MILITARY US SFA'}

    def __init__(self):
        self.schema = {
            'UPRN': [mandatory(), max_length(13), numeric(), no_padding_whitespace()],
            'ESTAB_UPRN': [mandatory(), max_length(13), numeric(), no_padding_whitespace()],
            'ADDRESS_TYPE': [mandatory(), in_set({'HH', 'CE', 'SPG'}), no_padding_whitespace()],
            'ESTAB_TYPE': [mandatory(), in_set(self.ESTAB_TYPES)],
            'ADDRESS_LEVEL': [mandatory(), in_set({'E', 'U'}), no_padding_whitespace()],
            'ABP_CODE': [mandatory(), max_length(6), no_padding_whitespace(), no_pipe_character()],
            'ORGANISATION_NAME': [max_length(60), no_padding_whitespace(), no_pipe_character()],
            'ADDRESS_LINE1': [mandatory(), max_length(60), no_padding_whitespace(), no_pipe_character()],
            'ADDRESS_LINE2': [max_length(60), no_padding_whitespace(), no_pipe_character()],
            'ADDRESS_LINE3': [max_length(60), no_padding_whitespace(), no_pipe_character()],
            'TOWN_NAME': [mandatory(), max_length(30), no_padding_whitespace(), no_pipe_character()],
            'POSTCODE': [mandatory(), max_length(8), no_padding_whitespace(),
                         alphanumeric_postcode(), no_pipe_character()],
            'LATITUDE': [mandatory(), latitude_longitude(max_scale=7, max_precision=9),
                         no_padding_whitespace(), no_pipe_character(), latitude_longitude_range()],
            'LONGITUDE': [mandatory(), latitude_longitude(max_scale=7, max_precision=8),
                          no_padding_whitespace(), no_pipe_character(), latitude_longitude_range()],
            'OA': [mandatory(), max_length(9), no_padding_whitespace(), no_pipe_character()],
            'LSOA': [mandatory(), max_length(9), no_padding_whitespace(), no_pipe_character()],
            'MSOA': [mandatory(), max_length(9), no_padding_whitespace(), no_pipe_character()],
            'LAD': [mandatory(), max_length(9), no_padding_whitespace(), no_pipe_character()],
            'REGION': [mandatory(), max_length(9), no_padding_whitespace(),
                       region_matches_treatment_code(), no_pipe_character()],
            'HTC_WILLINGNESS': [mandatory(), in_set({'0', '1', '2', '3', '4', '5'})],
            'HTC_DIGITAL': [mandatory(), in_set({'0', '1', '2', '3', '4', '5'})],
            'FIELDCOORDINATOR_ID': [mandatory(), max_length(10), no_padding_whitespace(), no_pipe_character(),
                                    alphanumeric_plus_hyphen_field_values()],
            'FIELDOFFICER_ID': [mandatory(), max_length(13), no_padding_whitespace(), no_pipe_character(),
                                alphanumeric_plus_hyphen_field_values()],
            'TREATMENT_CODE': [mandatory(), in_set(self.TREATMENT_CODES)],
            'CE_EXPECTED_CAPACITY': [numeric(), max_length(4), no_padding_whitespace(),
                                     ce_u_has_expected_capacity(),
                                     ce_e_has_expected_capacity()],
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

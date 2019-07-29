import argparse
import csv

ARID = set()


VALID_ESTABLISHMENT_TYPES = {
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


VALID_TREATMENT_CODES = {
    'HH_LF2R1E', 'HH_LF2R2E', 'HH_LF2R3AE', 'HH_LF2R3BE', 'HH_LF3R1E', 'HH_LF3R2E', 'HH_LF3R3AE', 'HH_LF3R3BE',
    'HH_LFNR1E', 'HH_LFNR2E', 'HH_LFNR3AE', 'HH_LFNR3BE', 'HH_LF2R1W', 'HH_LF2R2W', 'HH_LF2R3AW', 'HH_LF2R3BW',
    'HH_LF3R1W', 'HH_LF3R2W', 'HH_LF3R3AW', 'HH_LF3R3BW', 'HH_LFNR1W', 'HH_LFNR2W', 'HH_LFNR3AW', 'HH_LFNR3BW',
    'HH_1LSFN', 'HH_2LEFN', 'HH_QF2R1E', 'HH_QF2R2E', 'HH_QF2R3AE', 'HH_QF3R1E', 'HH_QF3R2E', 'HH_QF3R3AE',
    'HH_QFNR1E', 'HH_QFNR2E', 'HH_QFNR3AE', 'HH_QF2R1W', 'HH_QF2R2W', 'HH_QF2R3AW', 'HH_QF3R1W', 'HH_QF3R2W',
    'HH_QF3R3AW', 'HH_QFNR1W', 'HH_QFNR2W', 'HH_QFNR3AW', 'HH_3QSFN'}


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    return parser.parse_args()


args = parse_arguments()
error_count = 0


def validate_header_row(fieldnames):
    valid_header = ['ARID', 'ESTAB_ARID', 'UPRN', 'ADDRESS_TYPE', 'ESTAB_TYPE', 'ADDRESS_LEVEL', 'ABP_CODE',
                    'ORGANISATION_NAME', 'ADDRESS_LINE1', 'ADDRESS_LINE2', 'ADDRESS_LINE3', 'TOWN_NAME', 'POSTCODE',
                    'LATITUDE', 'LONGITUDE', 'OA', 'LSOA', 'MSOA', 'LAD', 'REGION', 'HTC_WILLINGNESS',
                    'HTC_DIGITAL', 'FIELDCOORDINATOR_ID', 'FIELDOFFICER_ID', 'TREATMENT_CODE',
                    'CE_EXPECTED_CAPACITY']

    if not set(fieldnames) == set(valid_header):
        print(f'Header is invalid.')
        exit(-1)


def validate_sample_file(sample_file_path):
    try:
        with open(sample_file_path, encoding="utf-8") as sample_file:
            return load_sample(sample_file)
    except UnicodeDecodeError as err:
        print(f'Invalid file encoding, requires utf-8, error: {err}')
        exit(-1)


def load_sample(sample_file):
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    validate_header_row(sample_file_reader.fieldnames)
    for line_number, sample_row in enumerate(sample_file_reader, 2):
        validate_arid(line_number, sample_row)
        validate_estab_arid(line_number, sample_row)
        validate_uprn(line_number, sample_row)
        validate_address_type(line_number, sample_row)
        validate_estab_type(line_number, sample_row)
        validate_address_level(line_number, sample_row)
        validate_abp_code(line_number, sample_row)
        validate_org_name(line_number, sample_row)
        validate_address_line(line_number, sample_row)
        validate_town_name(line_number, sample_row)
        validate_postcode(line_number, sample_row)
        validate_longitude_latitude(line_number, sample_row, 'LATITUDE', max_scale=7, max_precision=10)
        validate_longitude_latitude(line_number, sample_row, 'LONGITUDE', max_scale=7, max_precision=9)
        validate_oa(line_number, sample_row)
        validate_lsoa(line_number, sample_row)
        validate_msoa(line_number, sample_row)
        validate_lad(line_number, sample_row)
        validate_region(line_number, sample_row)
        validate_htc_willingness(line_number, sample_row)
        validate_htc_digital(line_number, sample_row)
        validate_fieldcordinator_id(line_number, sample_row)
        validate_fieldofficer_id(line_number, sample_row)
        validate_treatment_code(line_number, sample_row)
        validate_ce_expected_capacity(line_number, sample_row)


def validate_arid(line_number, sample_row):
    global error_count
    column = 'ARID'
    maximum_length = 21
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)
    if sample_row[column] in ARID:
        print(f'Line {line_number}: {column}: {sample_row[column]} is duplicated in sample file.')
        error_count += 1
    else:
        ARID.add(sample_row[column])


def validate_estab_arid(line_number, sample_row):
    column = 'ESTAB_ARID'
    maximum_length = 21
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_uprn(line_number, sample_row):
    global error_count
    column = 'UPRN'
    maximum_length = 12
    if _check_mandatory_value_exists(line_number, column, mandatory=False, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)
        uprn = sample_row[column]
        if not uprn.isnumeric() and uprn != '':
            print(f'Line {line_number}: {column}: {sample_row[column]} is not a valid integer.')
            error_count += 1


def validate_address_type(line_number, sample_row):
    global error_count
    column = 'ADDRESS_TYPE'
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        address_type = sample_row[column]
        if address_type not in {"HH", "CE", "SPG"}:
            print(f'Line {line_number}: {column}: {sample_row[column]} is not valid.')
            error_count += 1


def validate_estab_type(line_number, sample_row):
    column = 'ESTAB_TYPE'
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        _is_valid_estab_type(line_number, sample_row[column])


def validate_address_level(line_number, sample_row):
    global error_count
    column = 'ADDRESS_LEVEL'
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        if sample_row[column] not in {"E", "U"}:
            print(f'Line {line_number}: {column}: {sample_row[column]} is not valid.')
            error_count += 1


def validate_abp_code(line_number, sample_row):
    column = 'ABP_CODE'
    maximum_length = 6
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_org_name(line_number, sample_row):
    column = 'ORGANISATION_NAME'
    maximum_length = 60
    if _check_mandatory_value_exists(line_number, column, mandatory=False, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_address_line(line_number, sample_row):
    maximum_length = 60
    # only address line 1 is mandatory
    column = 'ADDRESS_LINE1'
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        for column in ['ADDRESS_LINE1', 'ADDRESS_LINE2', 'ADDRESS_LINE3']:
            address_line = sample_row[column]
            _check_length(column, address_line, line_number, maximum_length)


def validate_town_name(line_number, sample_row):
    column = 'TOWN_NAME'
    maximum_length = 30
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_postcode(line_number, sample_row):
    column = 'POSTCODE'
    maximum_length = 8
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_longitude_latitude(line_number, sample_row, column, max_scale, max_precision):
    # Precision is the total number of digits and scale is the total number of digits after the decimal point
    global error_count
    numeric = True
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        num, decimal = sample_row[column].split(".")
        if num[0] == '-':
            num = num[1:]
        precision = len(num) + len(decimal)
        scale = len(decimal)
        try:
            float(sample_row[column])
        except ValueError:
            numeric = False
        if precision > max_precision or scale > max_scale or not numeric:
            print(f'Line {line_number}: {column}: {sample_row[column]} is not valid. '
                  f'Value needs to be numeric with max precision of {max_precision} and max scale of {max_scale}')
            error_count += 1


def validate_oa(line_number, sample_row):
    column = 'OA'
    maximum_length = 9
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_lsoa(line_number, sample_row):
    column = 'LSOA'
    maximum_length = 9
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_msoa(line_number, sample_row):
    column = 'MSOA'
    maximum_length = 9
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_lad(line_number, sample_row):
    column = 'LAD'
    maximum_length = 9
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_region(line_number, sample_row):
    column = 'REGION'
    maximum_length = 9
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_htc_willingness(line_number, sample_row):
    global error_count
    column = 'HTC_WILLINGNESS'
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        htc_willingness = sample_row[column]
        if htc_willingness.isnumeric and len(htc_willingness) == 1:
            return
        print(f'Line {line_number}: {column} {htc_willingness} is not valid.')
        error_count += 1


def validate_htc_digital(line_number, sample_row):
    global error_count
    column = 'HTC_DIGITAL'
    if _check_mandatory_value_exists(line_number, column, mandatory=True, sample_row=sample_row):
        htc_digital = sample_row[column]
        if htc_digital.isnumeric and len(htc_digital) == 1:
            return
        print(f'Line {line_number}: {column} {htc_digital} is not valid.')
        error_count += 1


def validate_fieldcordinator_id(line_number, sample_row):
    column = 'FIELDCOORDINATOR_ID'
    maximum_length = 7
    if _check_mandatory_value_exists(line_number, column, mandatory=False, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_fieldofficer_id(line_number, sample_row):
    column = 'FIELDOFFICER_ID'
    maximum_length = 10
    if _check_mandatory_value_exists(line_number, column, mandatory=False, sample_row=sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)


def validate_treatment_code(line_number, sample_row):
    column = 'TREATMENT_CODE'
    maximum_length = 10
    mandatory = True
    if _check_mandatory_value_exists(line_number, column, mandatory, sample_row):
        _check_length(column, sample_row[column], line_number, maximum_length)
        _is_valid_treatment_code(line_number, sample_row[column])


def validate_ce_expected_capacity(line_number, sample_row):
    global error_count
    column = 'CE_EXPECTED_CAPACITY'
    maximum_length = 4
    if _check_mandatory_value_exists(line_number, column, mandatory=False, sample_row=sample_row):
        value = sample_row[column]
        _check_length(column, value, line_number, maximum_length)
        if not value == "" and not value.isnumeric():
            print(f'Line {line_number}: {column}: {value} is not a valid integer.')
            error_count += 1


def _check_mandatory_value_exists(line_number, column, mandatory, sample_row):
    global error_count
    # check value is not empty
    value = sample_row[column]
    if mandatory and not value:
        print(f'Line {line_number}: {column} is empty.')
        error_count += 1
        return False
    return True


def _check_length(name, value, line_number, maximum_length):
    global error_count
    if len(value) > maximum_length:
        print(f'Line {line_number}: {name}: {value} exceeds maximum length of {maximum_length}.')
        error_count += 1


def _is_valid_treatment_code(line_number, treatment_code):
    global error_count
    if treatment_code not in VALID_TREATMENT_CODES:
        print(f'Line {line_number}: TREATMENT_CODE: {treatment_code} is invalid.')
        error_count += 1


def _is_valid_estab_type(line_number, estab_type):
    global error_count
    if estab_type not in VALID_ESTABLISHMENT_TYPES:
        print(f'Line {line_number}: ESTAB_TYPE: {estab_type} is invalid.')
        error_count += 1


def main():
    validate_sample_file(args.sample_file_path)
    if error_count == 0:
        print(f'Sample file is OK.')
    else:
        print(f'{error_count} error(s) found in sample file')
        exit(-1)


if __name__ == "__main__":
    main()

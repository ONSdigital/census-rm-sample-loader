import argparse
import csv


ARID = set()

VALID_ESTABLISHMENT_TYPES = set(
    ['Household'
     'Sheltered Accommodation',
     'Hall of Residence',
     'Care Home',
     'Boarding School',
     'Hotel',
     'Hostel',
     'Residential Caravanner',
     'Gypsy Roma Traveller',
     'Residential Boater'])

# do we need all now?
VALID_TREATMENT_CODES = set(
    ['HH_LF2R1E', 'HH_LF2R2E', 'HH_LF2R3AE', 'HH_LF2R3BE', 'HH_LF3R1E', 'HH_LF3R2E', 'HH_LF3R3AE', 'HH_LF3R3BE',
     'HH_LFNR1E', 'HH_LFNR2E', 'HH_LFNR3AE', 'HH_LFNR3BE', 'HH_LF2R1W', 'HH_LF2R2W', 'HH_LF2R3AW', 'HH_LF2R3BW',
     'HH_LF3R1W', 'HH_LF3R2W', 'HH_LF3R3AW', 'HH_LF3R3BW', 'HH_LFNR1W', 'HH_LFNR2W', 'HH_LFNR3AW', 'HH_LFNR3BW',
     'HH_1LSFN', 'HH_2LEFN', 'HH_QF2R1E', 'HH_QF2R2E', 'HH_QF2R3AE', 'HH_QF3R1E', 'HH_QF3R2E', 'HH_QF3R3AE',
     'HH_QFNR1E', 'HH_QFNR2E', 'HH_QFNR3AE', 'HH_QF2R1W', 'HH_QF2R2W', 'HH_QF2R3AW', 'HH_QF3R1W', 'HH_QF3R2W',
     'HH_QF3R3AW', 'HH_QFNR1W', 'HH_QFNR2W', 'HH_QFNR3AW', 'HH_3QSFN'])

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
        validate_latitude(count, sample_row)
        validate_longitude(count, sample_row)
        validate_oa(count, sample_row)
        validate_lsoa(count, sample_row)
        validate_msoa(count, sample_row)
        validate_lad(count, sample_row)
        validate_region(count, sample_row)
        validate_htc_willingness(count, sample_row)
        validate_htc_digital(count, sample_row)
        validate_fieldcordinator_id(count, sample_row)
        validate_fieldofficer_id(count, sample_row)
        validate_treatment_code(count, sample_row)
        validate_ce_expected_capacity(count, sample_row)


def validate_arid(count, sample_row):
    column = 'ARID'
    maximum_length = 21
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        arid = sample_row[column]
        _check_length(column, arid, count, maximum_length)
        if arid in ARID:
            print(f'Line {count}: {column}: {arid} is duplicated in sample file.')
        else:
            ARID.add(sample_row[column])


def validate_estab_arid(count, sample_row):
    column = 'ESTAB_ARID'
    maximum_length = 21
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        estab_arid = sample_row[column]
        _check_length(column, estab_arid, count, maximum_length)


def validate_uprn(count, sample_row):
    column = 'UPRN'
    maximum_length = 12
    mandatory = False
    if _check_column_exists(column, mandatory, sample_row):
        uprn = sample_row[column]
        _check_length(column, uprn, count, maximum_length)
        if not uprn.isnumeric():
            print(f'Line {count}: {column}: {uprn} is not a valid integer.')


def validate_address_type(count, sample_row):
    column = 'ADDRESS_TYPE'
    maximum_length = 3
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        address_type = sample_row[column]
        _check_length(column, address_type, count, maximum_length)
        if address_type not in {"HH", "CE", "SPG"}:
            print(f'Line {count}: {column}: {address_type} is not valid.')


def validate_estab_type(count, sample_row):
    column = 'ESTAB_TYPE'
    maximum_length = 30
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        estab_type = sample_row[column]
        _check_length(column, estab_type, count, maximum_length)
        _is_valid_estab_type(count, estab_type)


def validate_address_level(count, sample_row):
    column = 'ADDRESS_LEVEL'
    maximum_length = 1
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        address_level = sample_row[column]
        _check_length(column, address_level, count, maximum_length)
        if address_level not in {"E", "U"}:
            print(f'Line {count}: {column}: {address_level} is not valid.')


def validate_abp_code(count, sample_row):
    column = 'ABP_CODE'
    maximum_length = 6
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        abp_code = sample_row[column]
        _check_length(column, abp_code, count, maximum_length)


def validate_org_name(count, sample_row):
    column = 'ORGANISATION_NAME'
    maximum_length = 60
    mandatory = False
    if _check_column_exists(column, mandatory, sample_row):
        org_name = sample_row[column]
        _check_length('ORGANISATION_NAME', org_name, count, maximum_length)


def validate_address_line(count, sample_row):
    maximum_length = 60
    for column in ['ADDRESS_LINE1', 'ADDRESS_LINE2', 'ADDRESS_LINE3']:
        # only address line 1 is mandatory
        if _check_column_exists(column, column == 'ADDRESS_LINE1', sample_row):
            address_line = sample_row[column]
            _check_length(column, address_line, count, maximum_length)


def validate_town_name(count, sample_row):
    column = 'TOWN_NAME'
    maximum_length = 30
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        town_name = sample_row[column]
        _check_length(column, town_name, count, maximum_length)


def validate_postcode(count, sample_row):
    column = 'POSTCODE'
    maximum_length = 8
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        postcode = sample_row[column]
        _check_length(column, postcode, count, maximum_length)


def validate_latitude(count, sample_row):
    # must be between -90 and 90 but we are not validating
    column = 'LATITUDE'
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        latitude = sample_row[column]
        scale, precision = latitude.split(".")
        if scale[0] == '-':
            scale = scale[1:]
        if scale.isnumeric() and len(scale) <= 10:
            if precision.isnumeric() and len(precision) <= 7:
                return
        print(f'Line {count}: {column}: {latitude} is not valid.')


def validate_longitude(count, sample_row):
    # must be between -180 and 180 but we are not validating
    column = 'LONGITUDE'
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        longitude = sample_row[column]
        scale, precision = longitude.split(".")
        if scale[0] == '-':
            scale = scale[1:]
        if scale.isnumeric() and len(scale) <= 9:
            if precision.isnumeric() and len(precision) <= 7:
                return
        print(f'Line {count}: {column}: {longitude} is not valid.')


def validate_oa(count, sample_row):
    column = 'OA'
    maximum_length = 9
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        oa = sample_row[column]
        _check_length(column, oa, count, maximum_length)


def validate_lsoa(count, sample_row):
    column = 'LSOA'
    maximum_length = 9
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        lsoa = sample_row[column]
        _check_length(column, lsoa, count, maximum_length)


def validate_msoa(count, sample_row):
    column = 'MSOA'
    maximum_length = 9
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        msoa = sample_row[column]
        _check_length(column, msoa, count, maximum_length)


def validate_lad(count, sample_row):
    column = 'LAD'
    maximum_length = 9
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        lad = sample_row[column]
        _check_length(column, lad, count, maximum_length)


def validate_region(count, sample_row):
    column = 'REGION'
    maximum_length = 9
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        region = sample_row[column]
        _check_length(column, region, count, maximum_length)


def validate_htc_willingness(count, sample_row):
    column = 'HTC_WILLINGNESS'
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        htc_willingness = sample_row[column]
        if htc_willingness.isnumeric and len(htc_willingness) == 1:
            return
        print(f'Line {count}: {column} {htc_willingness} is not valid.')


def validate_htc_digital(count, sample_row):
    column = 'HTC_DIGITAL'
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        htc_digital = sample_row[column]
        if htc_digital.isnumeric and len(htc_digital) == 1:
            return
        print(f'Line {count}: {column} {htc_digital} is not valid.')


def validate_fieldcordinator_id(count, sample_row):
    column = 'FIELDCOORDINATOR_ID'
    maximum_length = 7
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        fieldcordinator_id = sample_row[column]
        _check_length(column, fieldcordinator_id, count, maximum_length)


def validate_fieldofficer_id(count, sample_row):
    column = 'FIELDOFFICER_ID'
    maximum_length = 10
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        fieldofficer_id = sample_row[column]
        _check_length(column, fieldofficer_id, count, maximum_length)


def validate_treatment_code(count, sample_row):
    column = 'TREATMENT_CODE'
    maximum_length = 10
    mandatory = True
    if _check_column_exists(column, mandatory, sample_row):
        treatment_code = sample_row[column]
        _check_length(column, treatment_code, count, maximum_length)
        _is_valid_treatment_code(count, treatment_code)


def validate_ce_expected_capacity(count, sample_row):
    column = 'CE_EXPECTED_CAPACITY'
    maximum_length = 4
    mandatory = False
    if _check_column_exists(column, mandatory, sample_row):
        value = sample_row[column]
        _check_length(column, value, count, maximum_length)
        if not value.isnumeric():
            print(f'Line {count}: {column}: {value} is not a valid integer.')


def _check_column_exists(column, mandatory, sample_row):
    if column not in sample_row:
        if mandatory:
            print(f'{column} does not exist in file.')
        return False
    else:
        return True


def _check_length(name, value, count, maximum_length):
    trimmed_value = value.strip()
    if len(trimmed_value) > maximum_length:
        print(f'Line {count}: {name}: {value} exceeds maximum length of {maximum_length}.')


def _is_valid_treatment_code(count, treatment_code):
    if treatment_code not in VALID_TREATMENT_CODES:
        print(f'Line {count}: TREATMENT_CODE: {treatment_code} is invalid.')


def _is_valid_estab_type(count, estab_type):
    if estab_type not in VALID_ESTABLISHMENT_TYPES:
        print(f'Line {count}: ESTAB_TYPE: {estab_type} is invalid.')


def main():
    args = parse_arguments()
    validate_sample_file(args.sample_file_path)


if __name__ == "__main__":
    main()

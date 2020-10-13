import argparse
import csv
import logging
import os
import sys
from typing import Iterable

from generate_sample_file import SampleGenerator

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
SampleGen = SampleGenerator()
SampleGen.ESTAB_TYPES = ['HALL OF RESIDENCE', 'CARE HOME', 'HOSPITAL', 'HOSPICE', 'MENTAL HEALTH HOSPITAL',
                         'MEDICAL CARE OTHER', 'BOARDING SCHOOL', 'HOTEL',
                         'YOUTH HOSTEL', 'HOSTEL', 'EDUCATION OTHER', 'PRISON', 'STAFF ACCOMMODATION', 'CAMPHILL',
                         'HOLIDAY PARK', 'HOUSEHOLD', 'RESIDENTIAL CARAVAN', 'RESIDENTIAL BOAT', 'GATED APARTMENTS',
                         'FOREIGN OFFICES', 'CASTLES', 'EMBASSY', 'CARAVAN', 'MARINA']
SampleGen.read_words()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    return parser.parse_args()


def redact_sample_file(sample_file_path, output_file_path):
    with open(sample_file_path) as sample_file:
        redact_sample(sample_file, output_file_path)
    sample_file.close()


def redact_sample(sample_file: Iterable[str], output_file_path):
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    _redact_sample_units(sample_file_reader, output_file_path)


def _redact_sample_units(sample_file_reader: Iterable[str], output_file_path,
                         sample_unit_log_frequency=50000):
    logger.info('Redacting sample...')

    with open(output_file_path, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=SampleGenerator.FIELDNAMES)
        writer.writeheader()

        for count, sample_row in enumerate(sample_file_reader, 1):
            redacted_sample_row = _redact_sample_row(sample_row)
            _write_row(writer, redacted_sample_row)

            if count % sample_unit_log_frequency == 0:
                logger.info(f'{count} sample units redacted')

    logger.info('All sample units have been redacted')


def _redact_sample_row(sample_row):
    sample_row['HTC_WILLINGNESS'] = SampleGen.get_random_htc()
    sample_row['HTC_DIGITAL'] = SampleGen.get_random_htc()
    if sample_row['ESTAB_TYPE'] in ['MILITARY US SFA', 'MILITARY SFA', 'MILITARY US SLA', 'ROYAL HOUSEHOLD',
                                    'MOD HOUSEHOLDS', 'HIGH SECURE MENTAL HEALTH', 'ROUGH SLEEPER', 'TRANSIENT PERSONS',
                                    'TRAVELLING PERSONS', 'GRT SITE', 'MIGRANT WORKERS', 'IMMIGRATION REMOVAL CENTRE',
                                    'SHELTERED ACCOMMODATION', 'APPROVED PREMISES', 'RESIDENTIAL CHILDRENS HOME',
                                    'RELIGIOUS COMMUNITY', 'LOW/MEDIUM SECURE MENTAL HEALTH']:
        sample_row['ESTAB_TYPE'] = SampleGen.get_random_estab_type()
        sample_row['ADDRESS_LINE1'] = SampleGen.get_random_address_line()
        sample_row['ADDRESS_LINE2'] = ''
        sample_row['ADDRESS_LINE3'] = ''
        sample_row['TOWN_NAME'] = SampleGen.get_random_post_town()
        sample_row['POSTCODE'] = SampleGen.get_random_post_code()
        sample_row['LATITUDE'] = SampleGen.get_random_lat_or_long()
        sample_row['LONGITUDE'] = SampleGen.get_random_lat_or_long()

    return sample_row


def _write_row(writer, sample_row):
    writer.writerow({
        'UPRN': sample_row['UPRN'],
        'ESTAB_UPRN': sample_row['ESTAB_UPRN'],
        'ADDRESS_TYPE': sample_row['ADDRESS_TYPE'],
        'ESTAB_TYPE': sample_row['ESTAB_TYPE'],
        'ADDRESS_LEVEL': sample_row['ADDRESS_LEVEL'],
        'ABP_CODE': sample_row['ABP_CODE'],
        'ORGANISATION_NAME': sample_row['ORGANISATION_NAME'],
        'ADDRESS_LINE1': sample_row['ADDRESS_LINE1'],
        'ADDRESS_LINE2': sample_row['ADDRESS_LINE2'],
        'ADDRESS_LINE3': sample_row['ADDRESS_LINE3'],
        'TOWN_NAME': sample_row['TOWN_NAME'],
        'POSTCODE': sample_row['POSTCODE'],
        'LATITUDE': sample_row['LATITUDE'],
        'LONGITUDE': sample_row['LONGITUDE'],
        'OA': sample_row['OA'],
        'LSOA': sample_row['LSOA'],
        'MSOA': sample_row['MSOA'],
        'LAD': sample_row['LAD'],
        'REGION': sample_row['REGION'],
        'HTC_WILLINGNESS': sample_row['HTC_WILLINGNESS'],
        'HTC_DIGITAL': sample_row['HTC_DIGITAL'],
        'TREATMENT_CODE': sample_row['TREATMENT_CODE'],
        'FIELDCOORDINATOR_ID': sample_row['FIELDCOORDINATOR_ID'],
        'FIELDOFFICER_ID': sample_row['FIELDOFFICER_ID'],
        'CE_EXPECTED_CAPACITY': sample_row['CE_EXPECTED_CAPACITY'],
        'CE_SECURE': sample_row['CE_SECURE'],
        'PRINT_BATCH': sample_row['PRINT_BATCH']})


def main():
    log_level = os.getenv('LOG_LEVEL')
    logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)], level=log_level or logging.ERROR)
    logger.setLevel(log_level or logging.INFO)
    args = parse_arguments()
    output_file_path = 'sample_files/' + args.sample_file_path.split('/')[-1].split('.csv')[0] + '_redacted.csv'
    redact_sample_file(args.sample_file_path, output_file_path)


if __name__ == "__main__":
    main()

import argparse
import csv
import json
import logging
import os
import sys
import uuid
from typing import Iterable
from rabbit_context import RabbitContext

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    parser.add_argument('collection_exercise_id', help='collection exercise ID', type=str)
    parser.add_argument('action_plan_id', help='action plan ID', type=str)
    parser.add_argument('load_from_line_number', help='load sample from specified line number', type=int, default=1)
    return parser.parse_args()


def load_sample_file(sample_file_path, collection_exercise_id, action_plan_id, load_from_line_number, **kwargs):
    with open(sample_file_path) as sample_file:
        return load_sample(sample_file, collection_exercise_id, action_plan_id, load_from_line_number, **kwargs)


def load_sample(sample_file: Iterable[str], collection_exercise_id: str, action_plan_id: str,
                load_from_line_number: int, **kwargs):
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    return _load_sample_units(action_plan_id, collection_exercise_id, sample_file_reader, load_from_line_number,
                              **kwargs)


def _load_sample_units(action_plan_id: str, collection_exercise_id: str, sample_file_reader: Iterable[str],
                       load_from_line_number: int, **kwargs):
    sample_units = {}

    with RabbitContext(**kwargs) as rabbit:
        logger.info(f'Loading sample units to queue {rabbit.queue_name}')

        logger.info(f'loading from line {load_from_line_number}')

        for count, sample_row in enumerate(sample_file_reader, 1):

            if count < load_from_line_number:
                continue

            sample_unit_id = uuid.uuid4()

            try:
                rabbit.publish_message(_create_case_json(sample_row, collection_exercise_id=collection_exercise_id,
                                                         action_plan_id=action_plan_id),
                                       content_type='application/json')

                if count % 100 == 0:
                    logger.info(f'{count} sample units loaded')
                    rabbit.commit()

            except Exception as e:
                logging.error(f"Failed after correctly loading: {count} lines, restart at {count + 1}")
                logging.exception(e)
                raise e

            sample_unit = {
                f'sampleunit:{sample_unit_id}': _create_sample_unit_json(sample_unit_id, sample_row)}
            sample_units.update(sample_unit)

    logger.info(f'All sample units have been added to the queue {rabbit.queue_name}')

    return sample_units


def _create_case_json(sample_row, collection_exercise_id, action_plan_id) -> str:
    create_case = {'arid': sample_row['ARID'], 'estabArid': sample_row['ESTAB_ARID'], 'uprn': sample_row['UPRN'],
                   'addressType': sample_row['ADDRESS_TYPE'], 'estabType': sample_row['ESTAB_TYPE'],
                   'addressLevel': sample_row['ADDRESS_LEVEL'], 'abpCode': sample_row['ABP_CODE'],
                   'organisationName': sample_row['ORGANISATION_NAME'],
                   'addressLine1': sample_row['ADDRESS_LINE1'], 'addressLine2': sample_row['ADDRESS_LINE2'],
                   'addressLine3': sample_row['ADDRESS_LINE3'], 'townName': sample_row['TOWN_NAME'],
                   'postcode': sample_row['POSTCODE'], 'latitude': sample_row['LATITUDE'],
                   'longitude': sample_row['LONGITUDE'], 'oa': sample_row['OA'],
                   'lsoa': sample_row['LSOA'], 'msoa': sample_row['MSOA'],
                   'lad': sample_row['LAD'], 'region': sample_row['REGION'],
                   'htcWillingness': sample_row['HTC_WILLINGNESS'], 'htcDigital': sample_row['HTC_DIGITAL'],
                   'fieldCoordinatorId': sample_row['FIELDCOORDINATOR_ID'],
                   'fieldOfficerId': sample_row['FIELDOFFICER_ID'],
                   'treatmentCode': sample_row['TREATMENT_CODE'],
                   'ceExpectedCapacity': sample_row['CE_EXPECTED_CAPACITY'],
                   'collectionExerciseId': collection_exercise_id,
                   'actionPlanId': action_plan_id}

    return json.dumps(create_case)


def _create_sample_unit_json(sample_unit_id, sample_unit) -> str:
    sample_unit = {'id': str(sample_unit_id), 'attributes': sample_unit}
    return json.dumps(sample_unit)


def main():
    log_level = os.getenv('LOG_LEVEL')
    logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)], level=log_level or logging.ERROR)
    logger.setLevel(log_level or logging.INFO)
    args = parse_arguments()
    load_sample_file(args.sample_file_path, args.collection_exercise_id, args.action_plan_id,
                     args.load_from_line_number)


if __name__ == "__main__":
    main()

import csv
import json
import os
from unittest import TestCase
from unittest.mock import patch

from load_sample import load_sample_file


@patch('sample_loader.RabbitContext')
@patch('sample_loader.RedisPipelineContext')
class TestLoadSample(TestCase):
    def setUp(self):
        self.current_file_path = os.path.dirname(__file__)

    def test_load_sample_file_publishes_case_to_rabbit(self, _, patch_rabbit):
        sample_file_path = f'{self.current_file_path}/resources/sample_5.csv'
        load_sample_file(sample_file_path, 'ce_uuid', 'ap_uuid', 'ci_uuid')

        patch_rabbit_context = patch_rabbit.return_value.__enter__.return_value
        publish_message_call_args = patch_rabbit_context.publish_message.call_args_list

        with open(sample_file_path) as sample_file:
            sample_file_rows = csv.DictReader(sample_file)
            for row_number, sample_row in enumerate(sample_file_rows):
                self.assertIn(sample_row['ARID'], publish_message_call_args[row_number][1]['message'])
                self.assertIn('ce_uuid', publish_message_call_args[row_number][1]['message'])
                self.assertIn('ap_uuid', publish_message_call_args[row_number][1]['message'])
                self.assertIn('ci_uuid', publish_message_call_args[row_number][1]['message'])

    def test_load_sample_file_writes_all_attributes_to_redis(self, patch_redis, _):
        sample_file_path = f'{self.current_file_path}/resources/sample_5.csv'
        load_sample_file(sample_file_path, 'ce_uuid', 'ap_uuid', 'ci_uuid')

        patch_redis_context = patch_redis.return_value.__enter__.return_value
        redis_set_call_args_list = patch_redis_context.set_names_to_values.call_args_list

        with open(sample_file_path) as sample_file:
            sample_file_rows = csv.DictReader(sample_file)
            for row_number, sample_row in enumerate(sample_file_rows):
                loaded_sample_unit = json.loads(tuple(redis_set_call_args_list[row_number][0][0].values())[0])
                for attribute, value in sample_row.items():
                    self.assertEqual(value, loaded_sample_unit['attributes'][attribute],
                                     f'Loaded sample attributes were missing attribute:'
                                     f' [{attribute}] with value [{value}]')

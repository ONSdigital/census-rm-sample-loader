import csv
import json
import os
from unittest import TestCase
from unittest.mock import patch
from xml.etree import ElementTree

from load_sample import load_sample_file, load_sample


@patch('load_sample.RabbitContext')
@patch('load_sample.RedisPipelineContext')
class TestLoadSample(TestCase):
    sample_5_file_path = f'{os.path.dirname(__file__)}/resources/sample_5.csv'

    def test_load_sample_file_publishes_cases_to_rabbit(self, _, patch_rabbit):
        load_sample_file(self.sample_5_file_path, 'test_ce_uuid', 'test_ap_uuid', 'test_ci_uuid')

        patch_rabbit_context = patch_rabbit.return_value.__enter__.return_value
        publish_message_call_args = patch_rabbit_context.publish_message.call_args_list

        with open(self.sample_5_file_path) as sample_file:
            self._check_published_cases_contain_required_data(publish_message_call_args, sample_file)

    def test_load_sample_file_writes_all_attributes_to_redis(self, patch_redis, _):
        load_sample_file(self.sample_5_file_path, 'test_ce_uuid', 'test_ap_uuid', 'test_ci_uuid')

        patch_redis_context = patch_redis.return_value.__enter__.return_value
        redis_set_call_args_list = patch_redis_context.set_names_to_values.call_args_list

        with open(self.sample_5_file_path) as sample_file:
            self._check_attributes_sent_to_redis_match_sample_file(redis_set_call_args_list, sample_file)

    def test_load_sample_publishes_case_to_rabbit(self, _, patch_rabbit):
        sample_file = ('ARID,UPRN,ADDRESS_TYPE,ADDRESS_LINE1,POSTCODE,TEST_ATTRIBUTE',
                       'DDR190314000000195675,,HH,123 Fake Street,AB1 2CD,abc',
                       'DDR190314000000239595,,HH,13 O\'Made-up Lane,AB123CD,123')
        load_sample(sample_file, 'test_ce_uuid', 'test_ap_uuid', 'test_ci_uuid')

        patch_rabbit_context = patch_rabbit.return_value.__enter__.return_value

        self.assertEqual(patch_rabbit_context.publish_message.call_count, 2)
        publish_message_call_args = patch_rabbit_context.publish_message.call_args_list

        self._check_published_cases_contain_required_data(publish_message_call_args, sample_file)

    def test_load_sample_writes_attributes_to_redis(self, patch_redis, _):
        sample_file = ('ARID,UPRN,ADDRESS_TYPE,ADDRESS_LINE1,POSTCODE,TEST_ATTRIBUTE',
                       'DDR190314000000195675,,HH,123 Fake Street,AB1 2CD,abc',
                       'DDR190314000000239595,,HH,13 O\'Made-up Lane,AB123CD,123')
        load_sample(sample_file, 'test_ce_uuid', 'test_ap_uuid', 'test_ci_uuid')

        patch_redis_context = patch_redis.return_value.__enter__.return_value
        self.assertEqual(patch_redis_context.set_names_to_values.call_count, 2)
        redis_set_call_args_list = patch_redis_context.set_names_to_values.call_args_list
        self._check_attributes_sent_to_redis_match_sample_file(redis_set_call_args_list, sample_file)

    def test_ARID_is_used_as_sample_unit_ref_in_case(self, _, patch_rabbit):
        sample_file = ('ARID',
                       'DDR190314000000195675')
        load_sample(sample_file, 'ce_uuid', 'ap_uuid', 'ci_uuid')

        patch_rabbit_context = patch_rabbit.return_value.__enter__.return_value
        case_xml = patch_rabbit_context.publish_message.call_args_list[0][1]['message']
        case_tree = ElementTree.fromstring(case_xml)
        sample_unit_ref = next(element.text for element in case_tree if element.tag == 'sampleUnitRef')
        self.assertEqual('DDR190314000000195675', sample_unit_ref)

    def _check_published_cases_contain_required_data(self, publish_message_call_args, sample_file,
                                                     ce_id='test_ce_uuid',
                                                     ap_id='test_ap_uuid',
                                                     ci_id='test_ci_uuid'):
        sample_file_rows = csv.DictReader(sample_file)
        for row_number, sample_row in enumerate(sample_file_rows):
            self.assertIn(sample_row['ARID'], publish_message_call_args[row_number][1]['message'])
            self.assertIn(ce_id, publish_message_call_args[row_number][1]['message'])
            self.assertIn(ap_id, publish_message_call_args[row_number][1]['message'])
            self.assertIn(ci_id, publish_message_call_args[row_number][1]['message'])

    def _check_attributes_sent_to_redis_match_sample_file(self, redis_set_call_args_list, sample_file):
        sample_file_rows = csv.DictReader(sample_file)
        for row_number, sample_row in enumerate(sample_file_rows):
            loaded_sample_unit = json.loads(tuple(redis_set_call_args_list[row_number][0][0].values())[0])
            for attribute, value in sample_row.items():
                self.assertEqual(value, loaded_sample_unit['attributes'][attribute])
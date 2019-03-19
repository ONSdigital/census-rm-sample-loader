import os
from unittest import TestCase
from unittest.mock import patch
from xml.etree import ElementTree

from sample_loader import SampleLoader


@patch('sample_loader.RabbitContext')
@patch('sample_loader.RedisPipelineContext')
class TestSampleLoader(TestCase):
    def setUp(self):
        self.current_file_path = os.path.dirname(__file__)

    def test_load_sample_publishes_case_to_rabbit(self, _, patch_rabbit):
        sample_file = ('ARID,UPRN,ADDRESS_TYPE,ADDRESS_LINE1,POSTCODE,TEST_ATTRIBUTE\n'
                       'DDR190314000000195675,,HH,123 Fake Street,XX1 1XX,abc\n'
                       'DDR190314000000239595,,HH,124 Fake Street,XX1 1XY,123\n').split('\n')
        sample_loader = SampleLoader()
        sample_loader.load_sample(sample_file, 'ce_uuid', 'ap_uuid', 'ci_uuid')

        patch_rabbit_context = patch_rabbit.return_value.__enter__.return_value

        self.assertEqual(patch_rabbit_context.publish_message.call_count, 2)
        publish_message_call_args = patch_rabbit_context.publish_message.call_args_list

        self.assertIn('DDR190314000000195675', publish_message_call_args[0][1]['message'])
        self.assertIn('ce_uuid', publish_message_call_args[0][1]['message'])
        self.assertIn('ap_uuid', publish_message_call_args[0][1]['message'])
        self.assertIn('ci_uuid', publish_message_call_args[0][1]['message'])

        self.assertIn('DDR190314000000239595', publish_message_call_args[1][1]['message'])
        self.assertIn('ce_uuid', publish_message_call_args[1][1]['message'])
        self.assertIn('ap_uuid', publish_message_call_args[1][1]['message'])
        self.assertIn('ci_uuid', publish_message_call_args[1][1]['message'])

    def test_load_sample_writes_attributes_to_redis(self, patch_redis, _):
        sample_file = ('ARID,UPRN,ADDRESS_TYPE,ADDRESS_LINE1,POSTCODE,TEST_ATTRIBUTE\n'
                       'DDR190314000000195675,,HH,123 Fake Street,AB1 2CD,abc\n'
                       'DDR190314000000239595,,HH,13 O\'Made-up Lane,AB123CD,123\n').split('\n')
        sample_loader = SampleLoader()
        sample_loader.load_sample(sample_file, 'ce_uuid', 'ap_uuid', 'ci_uuid')

        patch_redis_context = patch_redis.return_value.__enter__.return_value
        self.assertEqual(patch_redis_context.set_names_to_values.call_count, 2)

        first_call_attributes = tuple(patch_redis_context.set_names_to_values.call_args_list[0][0][0].values())[0]
        self.assertIn('"ARID": "DDR190314000000195675"', first_call_attributes)
        self.assertIn('"UPRN": ""', first_call_attributes)
        self.assertIn('"ADDRESS_TYPE": "HH"', first_call_attributes)
        self.assertIn('"ADDRESS_LINE1": "123 Fake Street"', first_call_attributes)
        self.assertIn('"POSTCODE": "AB1 2CD"', first_call_attributes)
        self.assertIn('"TEST_ATTRIBUTE": "abc"', first_call_attributes)

        second_call_attributes = tuple(patch_redis_context.set_names_to_values.call_args_list[1][0][0].values())[0]
        self.assertIn('"ARID": "DDR190314000000239595"', second_call_attributes)
        self.assertIn('"UPRN": ""', second_call_attributes)
        self.assertIn('"ADDRESS_TYPE": "HH"', second_call_attributes)
        self.assertIn('"ADDRESS_LINE1": "13 O\'Made-up Lane"', second_call_attributes)
        self.assertIn('"POSTCODE": "AB123CD"', second_call_attributes)
        self.assertIn('"TEST_ATTRIBUTE": "123"', second_call_attributes)

    def test_ARID_is_used_as_sample_unit_ref_in_case(self, _, patch_rabbit):
        sample_file = ('ARID\n'
                       'DDR190314000000195675\n').split('\n')
        sample_loader = SampleLoader()
        sample_loader.load_sample(sample_file, 'ce_uuid', 'ap_uuid', 'ci_uuid')

        patch_rabbit_context = patch_rabbit.return_value.__enter__.return_value
        case_xml = patch_rabbit_context.publish_message.call_args_list[0][1]['message']
        case_tree = ElementTree.fromstring(case_xml)
        sample_unit_ref = next(element.text for element in case_tree if element.tag == 'sampleUnitRef')
        self.assertEqual('DDR190314000000195675', sample_unit_ref)

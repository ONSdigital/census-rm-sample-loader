import os
from unittest import TestCase
from unittest.mock import patch

from sample_loader import SampleLoader


@patch('sample_loader.RabbitContext')
@patch('sample_loader.RedisPipelineContext')
class TestSampleLoader(TestCase):
    def setUp(self):
        self.current_file_path = os.path.dirname(__file__)

    def test_load_sample_publishes_to_rabbit(self, _, patch_rabbit):
        sample_file = ('TLA,REFERENCE,TEST_ATTRIBUTE\n'
                       'TL1,00001,abc\n'
                       'TL2,00002,123\n').split('\n')
        sample_loader = SampleLoader()
        sample_loader.load_sample(sample_file, 'ce_uuid', 'ap_uuid', 'ci_uuid')

        patch_rabbit_context_manager = patch_rabbit.return_value.__enter__.return_value

        self.assertEqual(patch_rabbit_context_manager.publish_message.call_count, 2)
        publish_message_call_args = patch_rabbit_context_manager.publish_message.call_args_list

        self.assertIn('TL100001', publish_message_call_args[0][1]['message'])
        self.assertIn('ce_uuid', publish_message_call_args[0][1]['message'])
        self.assertIn('ap_uuid', publish_message_call_args[0][1]['message'])
        self.assertIn('ci_uuid', publish_message_call_args[0][1]['message'])

        self.assertIn('TL200002', publish_message_call_args[1][1]['message'])
        self.assertIn('ce_uuid', publish_message_call_args[1][1]['message'])
        self.assertIn('ap_uuid', publish_message_call_args[1][1]['message'])
        self.assertIn('ci_uuid', publish_message_call_args[1][1]['message'])

    def test_load_sample_writes_to_redis(self, patch_redis, _):
        sample_file = ('TLA,REFERENCE,TEST,ARBITRARY_ATTRIBUTE\n'
                       'TL1,00001,abc,some_potentially \' unexpected ` characters\n'
                       'TL2,00002,123,this_text_can be anything\n').split('\n')
        sample_loader = SampleLoader()
        sample_loader.load_sample(sample_file, 'ce_uuid', 'ap_uuid', 'ci_uuid')

        patch_redis_context_manager = patch_redis.return_value.__enter__.return_value
        self.assertEqual(patch_redis_context_manager.set_names_to_values.call_count, 2)
        first_call_attributes = tuple(patch_redis_context_manager.set_names_to_values.call_args_list[0][0][0].values())[0]

        self.assertIn('"TLA": "TL1"', first_call_attributes)
        self.assertIn('"REFERENCE": "00001"', first_call_attributes)
        self.assertIn('"TEST": "abc"', first_call_attributes)
        self.assertIn('"ARBITRARY_ATTRIBUTE": "some_potentially \' unexpected ` characters"', first_call_attributes)

        second_call_attributes = tuple(patch_redis_context_manager.set_names_to_values.call_args_list[1][0][0].values())[0]
        self.assertIn('"TLA": "TL2"', second_call_attributes)
        self.assertIn('"REFERENCE": "00002"', second_call_attributes)
        self.assertIn('"TEST": "123"', second_call_attributes)
        self.assertIn('"ARBITRARY_ATTRIBUTE": "this_text_can be anything"', second_call_attributes)

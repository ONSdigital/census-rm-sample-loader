from unittest import TestCase
from unittest.mock import patch

from Exceptions import RedisPipelineClosedError
from redis_pipeline_context import RedisPipelineContext


@patch('redis_pipeline_context.redis')
class TestRedisPipelineContext(TestCase):

    def test_context_manager_opens_connection_and_pipeline(self, patch_redis):
        with RedisPipelineContext():
            patch_redis.StrictRedis.assert_called_once()
            patch_redis.StrictRedis.return_value.pipeline.assert_called_once()

    def test_context_manager_executes_on_exit(self, patch_redis):
        with RedisPipelineContext():
            patch_redis.StrictRedis.return_value.pipeline.return_value.execute.assert_not_called()
        patch_redis.StrictRedis.return_value.pipeline.return_value.execute.assert_called_once()

    def test_attempt_to_set_names_to_values_with_closed_connection_raises_correct_exception(self, _):
        with RedisPipelineContext() as redis_pipeline:
            pass

        with self.assertRaises(RedisPipelineClosedError):
            redis_pipeline.set_names_to_values({'test_name': 'test_value'})

    def test_set_names_to_values(self, patch_redis):
        with RedisPipelineContext() as redis_pipeline:
            redis_pipeline.set_names_to_values({'name_1': 'value_1',
                                                'name_2': 'value_2'})

        patch_pipeline = patch_redis.StrictRedis.return_value.pipeline.return_value
        self.assertEqual(patch_pipeline.set.call_count, 2)

        first_call_kwargs = patch_pipeline.set.call_args_list[0][1]
        self.assertEqual({'name': 'name_1', 'value': 'value_1'}, first_call_kwargs)

        second_call_kwargs = patch_pipeline.set.call_args_list[1][1]
        self.assertEqual({'name': 'name_2', 'value': 'value_2'}, second_call_kwargs)

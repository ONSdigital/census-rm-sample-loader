import csv
import json
import sys
import uuid

import jinja2

from rabbit_context import RabbitContext
from redis_pipeline_context import RedisPipelineContext


class SampleLoader:

    def __init__(self):
        self._env = jinja2.Environment(loader=jinja2.FileSystemLoader(["./"]))
        self._jinja_template = self._env.get_template("message_template.xml")

    def load_sample(self, sample_file, collection_exercise_id, action_plan_id, collection_instrument_id):
        sample_units = {}
        reader = csv.DictReader(sample_file, delimiter=',')

        with RabbitContext as rabbit:
            for count, sample_unit in enumerate(reader):
                sample_unit_id = uuid.uuid4()
                sample_units.update({"sample_unit:" + str(sample_unit_id): self.create_json(sample_unit_id, sample_unit)})
                rabbit.publish_message(
                    self._jinja_template.render(sample=sample_unit,
                                                sample_unit_id=sample_unit_id,
                                                collection_exercise_id=collection_exercise_id,
                                                action_plan_id=action_plan_id,
                                                collection_instrument_id=collection_instrument_id),
                    content_type='text/xml')

                if count % 5000 == 0:
                    sys.stdout.write(f"\r{count} samples loaded")
                    sys.stdout.flush()

        print('\nAll Sample Units have been added to the queue ' + rabbit.rabbitmq_queue)

        self.write_sample_units_to_redis(sample_units)

    @staticmethod
    def create_json(sample_unit_id, sample_unit):
        sample_unit = {"id": str(sample_unit_id), "attributes": sample_unit}
        return json.dumps(sample_unit)

    @staticmethod
    def write_sample_units_to_redis(sample_units):
        print("Writing sample_units to Redis")
        count = 0
        with RedisPipelineContext as redis_pipeline:
            for key, attributes in sample_units.items():
                redis_pipeline.set_name_value(key, attributes)
                count += 1
                if count % 5000 == 0:
                    sys.stdout.write(f"\r{count} samples loaded")
                    sys.stdout.flush()

        print("Sample Units written to Redis")

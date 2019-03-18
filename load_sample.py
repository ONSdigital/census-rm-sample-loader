import sys

from sample_loader import SampleLoader


def load_sample_file(sample_file_path, collection_exercise_id, action_plan_id, collection_instrument_id):
    sample_loader = SampleLoader()
    with open(sample_file_path) as sample_file:
        sample_loader.load_sample(sample_file, collection_exercise_id, action_plan_id, collection_instrument_id)


# ------------------------------------------------------------------------------------------------------------------
# Usage python loadSample.py <SAMPLE.csv> <COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID> <COLLECTION_INSTRUMENT_UUID>
# ------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print('Usage python loadSample.py sample.csv'
              '<COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID> <COLLECTION_INSTRUMENT_UUID>')
    else:
        load_sample_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

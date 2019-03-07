import sys

from sample_loader import SampleLoader

# ------------------------------------------------------------------------------------------------------------------
# Usage python loadSample.py <SAMPLE.csv> <COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID> <COLLECTION_INSTRUMENT_UUID>
# ------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            'Usage python loadSample.py sample.csv <COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID> <COLLECTION_INSTRUMENT_UUID>')
    else:
        sample_loader = SampleLoader()
        with open(sys.argv[1]) as f_obj:
            sample_loader.load_sample(f_obj, sys.argv[2], sys.argv[3], sys.argv[4])

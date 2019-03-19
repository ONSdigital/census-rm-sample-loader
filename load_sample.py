import argparse

from sample_loader import SampleLoader


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    parser.add_argument('collection_exercise_id', help='collection exercise ID', type=str)
    parser.add_argument('action_plan_id', help='action plan ID', type=str)
    parser.add_argument('collection_instrument_id', help='collection instrument ID', type=str)
    return parser.parse_args()


def load_sample_file(sample_file_path, collection_exercise_id, action_plan_id, collection_instrument_id):
    sample_loader = SampleLoader()
    with open(sample_file_path) as sample_file:
        sample_loader.load_sample(sample_file, collection_exercise_id, action_plan_id, collection_instrument_id)


if __name__ == "__main__":
    args = parse_arguments()
    load_sample_file(args.sample_file_path, args.collection_exercise_id, args.action_plan_id,
                     args.collection_instrument_id)

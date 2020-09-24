import argparse
import csv
import uuid


def parse_arguments():
    parser = argparse.ArgumentParser(description='Add case_id uuids to the sample file')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    return parser.parse_args()


def add_uuids_to_sample(sample_file_path):
    output_sample = sample_file_path[:-4] + "_with_ids.csv"
    with open(sample_file_path, 'r') as input_file, open(output_sample, 'w+') as output_sample:
        input_sample = csv.reader(input_file)
        headers = next(input_sample, None)
        headers.insert(0, 'CASE_ID')

        writer = csv.writer(output_sample)
        writer.writerow(headers)
        for row in input_sample:
            row.insert(0, str(uuid.uuid4()))
            writer.writerow(row)


def main():
    args = parse_arguments()
    add_uuids_to_sample(args.sample_file_path)


if __name__ == "__main__":
    main()

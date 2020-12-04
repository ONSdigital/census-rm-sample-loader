import argparse
import csv


def compare_files(old_file_path, new_file_path):
    old_file_by_uprn = {}

    problems_found = []

    with open(old_file_path) as old_file:

        old_file_reader = csv.DictReader(old_file, delimiter=',')

        for count, sample_row in enumerate(old_file_reader, 1):
            old_file_by_uprn[f'{sample_row["UPRN"]}'] = sample_row

    with open(new_file_path) as new_file:

        new_file_reader = csv.DictReader(new_file, delimiter=',')

        unique_uprns = set()

        for count, sample_row in enumerate(new_file_reader, 1):
            matching_sample_row = old_file_by_uprn.get(sample_row['UPRN'])
            if not matching_sample_row:
                print(f'Could not find UPRN in original sample {sample_row["UPRN"]} on row {count + 1}')
                problems_found.append(sample_row["UPRN"])
            else:
                if sample_row["UPRN"] in unique_uprns:
                    print(f'Duplicate UPRN {sample_row["UPRN"]} on row {count + 1}')
                    problems_found.append(sample_row["UPRN"])

                unique_uprns.add(sample_row['UPRN'])

                for row_key in list(sample_row.keys()):
                    if sample_row[row_key] != matching_sample_row[row_key] \
                            and row_key != 'FIELDCOORDINATOR_ID' and row_key != 'FIELDOFFICER_ID':
                        print(f'Found invalid data in column {row_key}, row {count + 1}: {sample_row[row_key]}'
                              f'\nExpected: {matching_sample_row[row_key]} ')
                        problems_found.append(sample_row[row_key])

    return problems_found


def parse_arguments():
    parser = argparse.ArgumentParser(description='Validate new file against old one')
    parser.add_argument('old_file', help='Old file to process', type=str)
    parser.add_argument('new_file', help='New file to process', type=str)
    return parser.parse_args()


def main():
    args = parse_arguments()

    if compare_files(old_file_path=args.old_file, new_file_path=args.new_file):
        print('This file has FAILED validation')
    else:
        print('This file has PASSED validation')


if __name__ == '__main__':
    main()

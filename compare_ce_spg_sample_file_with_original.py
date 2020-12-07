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
                problems_found.append(f'Could not find UPRN in original sample {sample_row["UPRN"]} on row {count + 1}')
            else:
                if sample_row["UPRN"] in unique_uprns:
                    problems_found.append(f'Duplicate UPRN {sample_row["UPRN"]} on row {count + 1}')

                unique_uprns.add(sample_row['UPRN'])

                for row_key in list(sample_row.keys()):
                    if sample_row[row_key] != matching_sample_row[row_key] \
                            and row_key != 'FIELDCOORDINATOR_ID' and row_key != 'FIELDOFFICER_ID':
                        problems_found.append(f'Found invalid data in column {row_key}, row {count + 1}:'
                                              f' {sample_row[row_key]}...Expected: {matching_sample_row[row_key]} ')

    return problems_found


def parse_arguments():
    parser = argparse.ArgumentParser(description='Validate new file against old one')
    parser.add_argument('old_file', help='Old file to process', type=str)
    parser.add_argument('new_file', help='New file to process', type=str)
    return parser.parse_args()


def main():
    args = parse_arguments()

    problems_found = compare_files(old_file_path=args.old_file, new_file_path=args.new_file)
    if problems_found:
        print('\n'.join(problems_found))
        print('This file has FAILED validation')
    else:
        print('This file has PASSED validation')


if __name__ == '__main__':
    main()

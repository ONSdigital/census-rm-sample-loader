import argparse
import csv
import random
from pathlib import Path

FIELDNAMES = ('ARID', 'ESTAB_ARID', 'UPRN', 'ADDRESS_TYPE', 'ESTAB_TYPE', 'ADDRESS_LEVEL', 'ABP_CODE',
              'ORGANISATION_NAME', 'ADDRESS_LINE1', 'ADDRESS_LINE2', 'ADDRESS_LINE3',
              'TOWN_NAME', 'POSTCODE', 'LATITUDE', 'LONGITUDE', 'OA', 'LSOA',
              'MSOA', 'LAD', 'REGION', 'HTC_WILLINGNESS', 'HTC_DIGITAL', 'TREATMENT_CODE',
              'FIELDCOORDINATOR_ID', 'FIELDOFFICER_ID', 'CE_EXPECTED_CAPACITY')
COUNTRIES = ['E', 'W', 'N']
ROADS = ['Road', 'Street', 'Lane', 'Passage', 'Alley', 'Way', 'Avenue']
CONURBATIONS = ['City', 'Town', 'Village', 'Hamlet']
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']
WORDS = []
arid_numbers = set()
arid_sequence = 0


def read_treatment_code_quantities(treatment_code_quantities_path: Path):
    treatment_code_quantities = []

    with open(treatment_code_quantities_path) as treatment_code_quantities_file:
        file_reader = csv.DictReader(treatment_code_quantities_file)
        for row in file_reader:
            treatment_code = row['Treatment Code']
            quantity = int(row['Quantity'])
            treatment_code_quantities.append({'treatment_code': treatment_code, 'quantity': quantity})

    return treatment_code_quantities


def read_words():
    with open('words.txt') as file:
        for line in file:
            if len(line) > 1:
                WORDS.append(line.rstrip())


def get_random_word():
    random_word = WORDS[random.randint(0, len(WORDS) - 1)]
    return random_word.title()


def get_random_letter():
    return LETTERS[random.randint(0, len(LETTERS) - 1)]


def get_random_arid():
    random_number = random.randint(100000000, 999999999)

    while random_number in arid_numbers:
        random_number = random.randint(100000000, 999999999)

    arid_numbers.add(random_number)

    return f'DDR190314{random_number:012}'


def get_sequential_arid():
    global arid_sequence
    arid_sequence += 1
    return f'DDR190314{arid_sequence:012}'


def get_random_abp_code():
    random_number = random.randint(2, 6)
    return f'RD{random_number:02}'


def get_random_uprn():
    random_number = random.randint(10000000000, 99999999999)
    return f'{random_number:011}'


def get_random_regiony_type_thing():
    random_country = COUNTRIES[random.randint(0, len(COUNTRIES) - 1)]
    random_number = random.randint(10000000, 99999999)
    return f'{random_country}{random_number}'


def get_random_htc():
    return str(random.randint(1, 5))


def get_random_address_line():
    random_number = random.randint(1, 999)
    random_road = ROADS[random.randint(0, len(ROADS) - 1)]

    return f'{random_number} {get_random_word()} {get_random_word()} {random_road}'


def get_random_post_town():
    random_conurbation = CONURBATIONS[random.randint(0, len(CONURBATIONS) - 1)]

    return f'{get_random_word()} {random_conurbation}'


def get_random_post_code():
    first_random_number = random.randint(1, 9)
    second_random_number = random.randint(1, 9)
    return f'{get_random_letter()}{get_random_letter()}{first_random_number} {second_random_number}' + \
           f'{get_random_letter()}{get_random_letter()}'


def get_random_lat_or_long():
    random_degrees = random.randint(-180, 180)
    random_minutes = random.randint(999, 9999)
    return f'{random_degrees}.{random_minutes}'


def main(output_file_path: Path, treatment_code_quantities_path: Path, sequential_arid=False):
    print('Generating sample...')
    read_words()
    treatment_code_quantities = read_treatment_code_quantities(treatment_code_quantities_path)

    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()

        for item in treatment_code_quantities:
            for _ in range(item["quantity"]):
                writer.writerow({
                    'ARID': f'{get_sequential_arid() if sequential_arid else get_random_arid()}',
                    'ESTAB_ARID': f'{get_random_arid()}',
                    'UPRN': f'{get_random_uprn()}',
                    'ADDRESS_TYPE': 'HH',
                    'ESTAB_TYPE': 'Household',
                    'ADDRESS_LEVEL': 'U',
                    'ABP_CODE': f'{get_random_abp_code()}',
                    'ORGANISATION_NAME': '',
                    'ADDRESS_LINE1': f'{get_random_address_line()}',
                    'ADDRESS_LINE2': '',
                    'ADDRESS_LINE3': '',
                    'TOWN_NAME': f'{get_random_post_town()}',
                    'POSTCODE': f'{get_random_post_code()}',
                    'LATITUDE': f'{get_random_lat_or_long()}',
                    'LONGITUDE': f'{get_random_lat_or_long()}',
                    'OA': f'{get_random_regiony_type_thing()}',
                    'LSOA': f'{get_random_regiony_type_thing()}',
                    'MSOA': f'{get_random_regiony_type_thing()}',
                    'LAD': f'{get_random_regiony_type_thing()}',
                    'REGION': f'{get_random_regiony_type_thing()}',
                    'HTC_WILLINGNESS': f'{get_random_htc()}',
                    'HTC_DIGITAL': f'{get_random_htc()}',
                    'TREATMENT_CODE': f'{item["treatment_code"]}',
                    'FIELDCOORDINATOR_ID': '',
                    'FIELDOFFICER_ID': '',
                    'CE_EXPECTED_CAPACITY': '',
                })


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('--sequential_arid',
                        help="Use sequential ARID's to speed up generation",
                        default=False,
                        action='store_true',
                        required=False)
    parser.add_argument('--treatment_code_quantities_path', '-t',
                        help='Path to treatment code quantities csv config file',
                        default='treatment_code_quantities.csv', required=False)
    parser.add_argument('--output_file_path', '-o',
                        help='Path write generated sample file to',
                        default='sample_file.csv', required=False)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    main(output_file_path=args.output_file_path,
         treatment_code_quantities_path=args.treatment_code_quantities_path,
         sequential_arid=args.sequential_arid)

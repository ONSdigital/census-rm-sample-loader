import argparse
import csv
import random
from pathlib import Path


class SampleGenerator:
    FIELDNAMES = ('ARID', 'ESTAB_ARID', 'UPRN', 'ADDRESS_TYPE', 'ESTAB_TYPE', 'ADDRESS_LEVEL', 'ABP_CODE',
                  'ORGANISATION_NAME', 'ADDRESS_LINE1', 'ADDRESS_LINE2', 'ADDRESS_LINE3',
                  'TOWN_NAME', 'POSTCODE', 'LATITUDE', 'LONGITUDE', 'OA', 'LSOA',
                  'MSOA', 'LAD', 'REGION', 'HTC_WILLINGNESS', 'HTC_DIGITAL', 'TREATMENT_CODE',
                  'FIELDCOORDINATOR_ID', 'FIELDOFFICER_ID', 'CE_EXPECTED_CAPACITY')
    COUNTRIES = ['E', 'W', 'N']
    ROADS = ['Road', 'Street', 'Lane', 'Passage', 'Alley', 'Way', 'Avenue']
    CONURBATIONS = ['City', 'Town', 'Village', 'Hamlet']
    LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V',
               'W', 'X', 'Y', 'Z']
    WORDS = []
    ARIDS = set()
    ARID_SEQUENCE = 0

    @staticmethod
    def read_treatment_code_quantities(treatment_code_quantities_path: Path):
        treatment_code_quantities = []

        with open(treatment_code_quantities_path) as treatment_code_quantities_file:
            file_reader = csv.DictReader(treatment_code_quantities_file)
            for row in file_reader:
                treatment_code = row['Treatment Code']
                quantity = int(row['Quantity'])
                treatment_code_quantities.append({'treatment_code': treatment_code, 'quantity': quantity})

        return treatment_code_quantities

    def read_words(self):
        with open(Path(__file__).parent.joinpath('words.txt')) as words_file:
            for line in words_file:
                if len(line) > 1:
                    self.WORDS.append(line.rstrip())

    def get_random_word(self):
        random_word = self.WORDS[random.randint(0, len(self.WORDS) - 1)]
        return random_word.title()

    def get_random_letter(self):
        return self.LETTERS[random.randint(0, len(self.LETTERS) - 1)]

    def get_random_arid(self):
        random_number = random.randint(100000000, 999999999)

        while random_number in self.ARIDS:
            random_number = random.randint(100000000, 999999999)

        self.ARIDS.add(random_number)

        return f'DDR190314{random_number:012}'

    def get_sequential_arid(self):
        self.ARID_SEQUENCE += 1
        return f'DDR190314{self.ARID_SEQUENCE:012}'

    @staticmethod
    def get_random_abp_code():
        random_number = random.randint(2, 6)
        return f'RD{random_number:02}'

    @staticmethod
    def get_random_uprn():
        random_number = random.randint(10000000000, 99999999999)
        return f'{random_number:011}'

    def get_random_regiony_type_thing(self):
        random_country = self.COUNTRIES[random.randint(0, len(self.COUNTRIES) - 1)]
        random_number = random.randint(10000000, 99999999)
        return f'{random_country}{random_number}'

    @staticmethod
    def get_random_htc():
        return str(random.randint(1, 5))

    def get_random_address_line(self):
        random_number = random.randint(1, 999)
        random_road = self.ROADS[random.randint(0, len(self.ROADS) - 1)]

        return f'{random_number} {self.get_random_word()} {self.get_random_word()} {random_road}'

    def get_random_post_town(self):
        random_conurbation = self.CONURBATIONS[random.randint(0, len(self.CONURBATIONS) - 1)]

        return f'{self.get_random_word()} {random_conurbation}'

    def get_random_post_code(self):
        first_random_number = random.randint(1, 9)
        second_random_number = random.randint(1, 9)
        return f'{self.get_random_letter()}{self.get_random_letter()}{first_random_number} {second_random_number}' + \
               f'{self.get_random_letter()}{self.get_random_letter()}'

    @staticmethod
    def get_random_lat_or_long():
        random_degrees = random.randint(-180, 180)
        random_minutes = random.randint(999, 9999)
        return f'{random_degrees}.{random_minutes}'

    def generate_sample_file(self, output_file_path: Path, treatment_code_quantities_path: Path, sequential_arid=False):
        print('Generating sample...')
        self.read_words()
        treatment_code_quantities = self.read_treatment_code_quantities(treatment_code_quantities_path)

        with open(output_file_path, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=self.FIELDNAMES)
            writer.writeheader()

            for item in treatment_code_quantities:
                for _ in range(item["quantity"]):
                    writer.writerow({
                        'ARID': self.get_sequential_arid() if sequential_arid else self.get_random_arid(),
                        'ESTAB_ARID': self.get_random_arid(),
                        'UPRN': self.get_random_uprn(),
                        'ADDRESS_TYPE': 'HH',
                        'ESTAB_TYPE': 'Household',
                        'ADDRESS_LEVEL': 'U',
                        'ABP_CODE': self.get_random_abp_code(),
                        'ORGANISATION_NAME': '',
                        'ADDRESS_LINE1': self.get_random_address_line(),
                        'ADDRESS_LINE2': '',
                        'ADDRESS_LINE3': '',
                        'TOWN_NAME': self.get_random_post_town(),
                        'POSTCODE': self.get_random_post_code(),
                        'LATITUDE': self.get_random_lat_or_long(),
                        'LONGITUDE': self.get_random_lat_or_long(),
                        'OA': self.get_random_regiony_type_thing(),
                        'LSOA': self.get_random_regiony_type_thing(),
                        'MSOA': self.get_random_regiony_type_thing(),
                        'LAD': self.get_random_regiony_type_thing(),
                        'REGION': self.get_random_regiony_type_thing(),
                        'HTC_WILLINGNESS': self.get_random_htc(),
                        'HTC_DIGITAL': self.get_random_htc(),
                        'TREATMENT_CODE': item["treatment_code"],
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
    SampleGenerator().generate_sample_file(output_file_path=args.output_file_path,
                                           treatment_code_quantities_path=args.treatment_code_quantities_path,
                                           sequential_arid=args.sequential_arid)

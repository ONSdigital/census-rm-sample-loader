import argparse
import csv
import random
from pathlib import Path


class SampleGenerator:
    FIELDNAMES = ('UPRN', 'ESTAB_UPRN', 'ADDRESS_TYPE', 'ESTAB_TYPE', 'ADDRESS_LEVEL', 'ABP_CODE',
                  'ORGANISATION_NAME', 'ADDRESS_LINE1', 'ADDRESS_LINE2', 'ADDRESS_LINE3',
                  'TOWN_NAME', 'POSTCODE', 'LATITUDE', 'LONGITUDE', 'OA', 'LSOA',
                  'MSOA', 'LAD', 'REGION', 'HTC_WILLINGNESS', 'HTC_DIGITAL', 'TREATMENT_CODE',
                  'FIELDCOORDINATOR_ID', 'FIELDOFFICER_ID', 'CE_EXPECTED_CAPACITY', 'CE_SECURE', 'PRINT_BATCH')
    COUNTRIES = ['E', 'W', 'N']
    ROADS = ['Road', 'Street', 'Lane', 'Passage', 'Alley', 'Way', 'Avenue']
    CONURBATIONS = ['City', 'Town', 'Village', 'Hamlet']
    LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
    WORDS = []

    CE_TYPES = ['Sheltered Accommodation',
                'Hall of Residence',
                'Care Home',
                'Boarding School',
                'Hotel',
                'Hostel',
                'Residential Caravanner',
                'Gypsy Roma Traveller',
                'Residential Boater']

    UPRNS = set()
    UPRN_SEQUENCE = 0

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

    def get_sequential_uprn(self):
        self.UPRN_SEQUENCE += 1
        return f'{self.UPRN_SEQUENCE:012}'

    @staticmethod
    def get_random_abp_code():
        random_number = random.randint(2, 6)
        return f'RD{random_number:02}'

    def get_random_uprn(self):
        random_number = random.randint(10000000000, 99999999999)

        while random_number in self.UPRNS:
            random_number = random.randint(10000000000, 99999999999)

        self.UPRNS.add(random_number)

        return f'{random_number:011}'

    @staticmethod
    def generate_region_from_treatment_code(treatment_code):
        region_code = treatment_code[-1]
        random_number = random.randint(10000000, 99999999)
        return f'{region_code}{random_number}'

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
    def get_random_ce_capacity():
        random_ce = random.randint(5, 1000)
        return f'{random_ce}'

    def get_random_print_batch(self):
        print_batch = random.randint(1, 99)
        return print_batch

    def get_random_ce_type(self):
        return self.CE_TYPES[random.randint(0, len(self.CE_TYPES) - 1)]

    @staticmethod
    def get_random_ce_secure():
        random_ce_secure = random.randint(0, 1)
        return f'{random_ce_secure}'

    @staticmethod
    def random_1_in_11():
        return random.randint(0, 10) > 9

    @staticmethod
    def get_random_lat_or_long():
        random_degrees = random.randint(-180, 180)
        random_minutes = random.randint(999, 9999)
        return f'{random_degrees}.{random_minutes}'

    def get_random_lsoa(self, treatment_code):
        region_code = treatment_code[-1]
        random_number = random.randint(1000001, 1033768)
        return f'{region_code}0{random_number}'

    def generate_sample_file(self, output_file_path: Path, treatment_code_quantities_path: Path, sequential_uprn=False):
        print('Generating sample...')
        self.read_words()
        treatment_code_quantities = self.read_treatment_code_quantities(treatment_code_quantities_path)

        with open(output_file_path, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=self.FIELDNAMES)
            writer.writeheader()

            for treatment_code in treatment_code_quantities:
                for _ in range(treatment_code["quantity"]):
                    if treatment_code["treatment_code"][:3] == "SPG":
                        self._write_estab_case(writer, sequential_uprn, treatment_code, address_type='SPG')
                        continue

                    # Randomly decide whether to create a CE case or not
                    if self.random_1_in_11():
                        self._write_estab_case(writer, sequential_uprn, treatment_code, address_type='CE')
                        continue

                    # otherwise write a standard HH case
                    self._write_row(writer, sequential_uprn, treatment_code, address_type='HH',
                                    address_level='U', expected_capacity=0)

    def _write_estab_case(self, writer, sequential_uprn, treatment_code, address_type):
        #  randomly decide if we want to create an E case with child U cases
        if self.random_1_in_11():
            self._write_parent_and_unit_cases(writer, sequential_uprn, treatment_code, address_type)
            return

        # otherwise write E case
        self._write_row(writer, sequential_uprn, treatment_code, address_type,
                        expected_capacity=self.get_random_ce_capacity(), address_level='E')

    def _write_parent_and_unit_cases(self, writer, sequential_uprn, treatment_code, address_type):
        # create parent case
        parent_uprn, estab_type = self._write_row(writer, sequential_uprn, treatment_code, address_type,
                                                  address_level='E', expected_capacity=0)

        # create child cases
        for _ in range(3):
            self._write_row(writer, sequential_uprn, treatment_code,
                            address_type, expected_capacity=self.get_random_ce_capacity(), estab_type=estab_type,
                            address_level='U', estab_uprn=parent_uprn)

    def _write_row(self, writer, sequential_uprn, treatment_code, address_type, expected_capacity,
                   address_level=None, estab_uprn=None, estab_type=None):
        uprn = self.get_sequential_uprn() if sequential_uprn else self.get_random_uprn()

        if estab_type is None:
            estab_type = self.get_random_ce_type() if address_type != 'HH' else 'Household'

        if estab_uprn is None:
            estab_uprn = self.get_random_uprn()

        writer.writerow({
            'UPRN': uprn,
            'ESTAB_UPRN': estab_uprn,
            'ADDRESS_TYPE': address_type,
            'ESTAB_TYPE': estab_type,
            'ADDRESS_LEVEL': address_level,
            'ABP_CODE': self.get_random_abp_code(),
            'ORGANISATION_NAME': '',
            'ADDRESS_LINE1': self.get_random_address_line(),
            'ADDRESS_LINE2': '',
            'ADDRESS_LINE3': '',
            'TOWN_NAME': self.get_random_post_town(),
            'POSTCODE': self.get_random_post_code(),
            'LATITUDE': self.get_random_lat_or_long(),
            'LONGITUDE': self.get_random_lat_or_long(),
            'OA': self.generate_region_from_treatment_code(treatment_code['treatment_code']),
            'LSOA': self.get_random_lsoa(treatment_code['treatment_code']),
            'MSOA': self.generate_region_from_treatment_code(treatment_code['treatment_code']),
            'LAD': self.generate_region_from_treatment_code(treatment_code['treatment_code']),
            'REGION': self.generate_region_from_treatment_code(treatment_code['treatment_code']),
            'HTC_WILLINGNESS': self.get_random_htc(),
            'HTC_DIGITAL': self.get_random_htc(),
            'TREATMENT_CODE': treatment_code["treatment_code"],
            'FIELDCOORDINATOR_ID': '',
            'FIELDOFFICER_ID': '',
            'CE_EXPECTED_CAPACITY': expected_capacity,
            'CE_SECURE': self.get_random_ce_secure() if address_type == 'CE' or address_type == 'SPG' else 0,
            'PRINT_BATCH': self.get_random_print_batch()
        })

        return uprn, estab_type


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('--sequential_uprn',
                        help="Use sequential UPRN's to speed up generation",
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
                                           sequential_uprn=args.sequential_uprn)

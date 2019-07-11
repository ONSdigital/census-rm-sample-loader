import csv
import random

COUNTRIES = ['E', 'W', 'N']
ROADS = ['Road', 'Street', 'Lane', 'Passage', 'Alley', 'Way', 'Avenue']
CONURBATIONS = ['City', 'Town', 'Village', 'Hamlet']
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
           'W', 'X', 'Y', 'Z']
WORDS = []
arid_numbers = set()


def read_treatment_code_quantities():
    treatment_code_quantities = []

    with open('treatment_code_quantities.csv') as file:
        file_reader = csv.DictReader(file)
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
    return f'{get_random_letter()}{get_random_letter()}{first_random_number} {second_random_number}' +\
           f'{get_random_letter()}{get_random_letter()}'


def get_random_lat_or_long():
    random_degrees = random.randint(-180, 180)
    random_minutes = random.randint(999, 999999)
    return f'{random_degrees}.{random_minutes}'


def main():
    print('Generating sample...')
    read_words()
    treatment_code_quantities = read_treatment_code_quantities()

    with open('sample_file.csv', 'w') as file:
        for item in treatment_code_quantities:
            for _ in range(item["quantity"]):
                file.write(
                    f'{get_random_arid()},{get_random_arid()},{get_random_uprn()},HH,Household,U,' +
                    f'{get_random_abp_code()},,{get_random_address_line()},,,{get_random_post_town()},' +
                    f'{get_random_post_code()},{get_random_lat_or_long()},{get_random_lat_or_long()},' +
                    f'{get_random_regiony_type_thing()},{get_random_regiony_type_thing()},' +
                    f'{get_random_regiony_type_thing()},{get_random_regiony_type_thing()},' +
                    f'{get_random_regiony_type_thing()},{get_random_htc()},{get_random_htc()},' +
                    f'{item["treatment_code"]},,,\n')


if __name__ == '__main__':
    main()

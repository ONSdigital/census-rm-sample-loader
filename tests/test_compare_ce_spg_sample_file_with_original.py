from pathlib import Path

from compare_ce_spg_sample_file_with_original import compare_files

RESOURCE_FILE_PATH = Path(__file__).parent.joinpath('resources/compare_ce_spg_files')


def test_pass_validation_if_rows_removed_in_new_file():
    old_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_old.csv')

    new_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_new_removed_rows.csv')

    problems_found = compare_files(old_sample_file, new_sample_file)

    assert len(problems_found) == 0


def test_fail_validation_if_duplicated_lines_in_new_file():
    old_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_old.csv')

    new_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_new_duplicated_lines.csv')

    problems_found = compare_files(old_sample_file, new_sample_file)

    expected_problems = ['Duplicate UPRN 12348874419 on row 6', 'Duplicate UPRN 12348874419 on row 7',
                         'Duplicate UPRN 12348874419 on row 8']

    assert problems_found == expected_problems


def test_fail_validation_if_new_rows_in_new_file():
    old_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_old.csv')

    new_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_new_brand_new_uprns.csv')

    problems_found = compare_files(old_sample_file, new_sample_file)

    expected_problems = ['Could not find UPRN in original sample 12345 on row 5']

    assert problems_found == expected_problems


def test_fail_validation_if_columns_other_than_field_officer_and_field_coordinator_are_changed():
    old_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_old.csv')

    new_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_new_postcode_changed.csv')

    problems_found = compare_files(old_sample_file, new_sample_file)

    expected_problems = ['Found invalid data in column POSTCODE, row 3: XXXXXX \nExpected: OO9 5DX ']

    assert problems_found == expected_problems


def test_pass_validation_if_field_officer_and_field_coordinator_are_changed():
    old_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_old.csv')

    new_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_new_field_columns_changed.csv')

    problems_found = compare_files(old_sample_file, new_sample_file)

    assert len(problems_found) == 0

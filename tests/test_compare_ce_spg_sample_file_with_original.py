from pathlib import Path

from compare_ce_spg_sample_file_with_original import compare_files

RESOURCE_FILE_PATH = Path(__file__).parent.joinpath('resources/compare_ce_spg_files')


def test_pass_validation_if_rows_removed_in_new_file():
    old_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_old.csv')

    new_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_new_removed_rows.csv')

    problems = compare_files(old_sample_file, new_sample_file)

    assert problems is False


def test_fail_validation_if_duplicated_lines_in_new_file():
    old_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_old.csv')

    new_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_new_duplicated_lines.csv')

    problems = compare_files(old_sample_file, new_sample_file)

    assert problems is True


def test_fail_validation_if_new_rows_in_new_file():
    old_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_old.csv')

    new_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_new_brand_new_uprns.csv')

    problems = compare_files(old_sample_file, new_sample_file)

    assert problems is True


def test_fail_validation_if_columns_other_than_field_officer_and_field_coordinator_are_changed():
    old_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_old.csv')

    new_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_new_postcode_changed.csv')

    problems = compare_files(old_sample_file, new_sample_file)

    assert problems is True


def test_pass_validation_if_field_officer_and_field_coordinator_are_changed():
    old_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_old.csv')

    new_sample_file = RESOURCE_FILE_PATH.joinpath('ce_spg_new_field_columns_changed.csv')

    problems = compare_files(old_sample_file, new_sample_file)

    assert problems is False

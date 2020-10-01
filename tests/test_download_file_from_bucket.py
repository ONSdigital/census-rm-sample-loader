import shutil
from functools import partial
from pathlib import Path
from unittest.mock import patch

import pytest

from download_file_from_bucket import load_bucket_sample_file


@pytest.fixture
def create_dir():
    Path("sample_files").mkdir(exist_ok=True)
    yield
    shutil.rmtree("sample_files")


@patch('download_file_from_bucket.storage')
def test_download_file_from_bucket_happy_path(patched_storage, create_dir):
    # Given
    sample_file = "sample_file.csv"

    patched_storage.Client.return_value.download_blob_to_file.side_effect = partial(mock_download_blob,
                                                                                    mock_data=(
                                                                                        b'header_1,header_2\n'
                                                                                        b'value1,value2\n'))
    # When
    load_bucket_sample_file(sample_file)

    # Then
    created_file = Path("sample_files").joinpath(sample_file).read_text()

    assert patched_storage.Client.return_value.download_blob_to_file.call_count == 1

    assert created_file == ('header_1,header_2\n'
                            'value1,value2\n')


def mock_download_blob(_source_blob, destination_file, mock_data):
    destination_file.write(mock_data)

from functools import partial
from pathlib import Path
from unittest.mock import patch

from download_file_from_bucket import load_bucket_sample_file

@patch('download_file_from_bucket.storage')
def test_download_file_from_bucket_happy_path(patched_storage):
    # Given
    Path("sample_files").mkdir()

    sample_file = "sample_file.csv"

    patched_storage.Client.return_value.download_blob_to_file.side_effect = partial(mock_download_blob,
                                                                                    mock_data=(
                                                                                        b'header_1,header_2\n'
                                                                                        b'value1,value2\n'))
    # When
    load_bucket_sample_file(sample_file)

    # Then


def mock_download_blob(_source_blob, destination_file, mock_data):
    destination_file.write(mock_data)

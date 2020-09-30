from pathlib import Path
from unittest.mock import patch

from download_file_from_bucket import load_bucket_sample_file


def test_download_file_from_bucket_happy_path():
    # Given
    Path("sample_files").mkdir()

    sample_file = "sample_file.csv"

    with patch('download_file_from_bucket.storage') as patched_storage:
        patched_storage.Client.return_value.download_blob_to_file.side_effect = \
            "resources/sample_file_invalid_treatment_code.csv"

        load_bucket_sample_file(sample_file)

    # mock.blob = Mock()

    # When

    # Then


def mock_download_blob(_source_blob, destination_file, mock_data):
    destination_file.write(mock_data)

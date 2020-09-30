import argparse
import os

from google.cloud import storage


def load_bucket_sample_file(sample_file):
    client = storage.Client(project="census-rm-leo-howard-mark4")

    bucket = client.get_bucket(os.getenv('SAMPLE_BUCKET', 'census-rm-leo-howard-mark4-sample'))
    blob = storage.Blob(sample_file, bucket)

    with open(sample_file, 'wb+') as file_obj:
        client.download_blob_to_file(blob, file_obj)

    print(f'downloaded file {sample_file} from gcp bucket {os.getenv("SAMPLE_BUCKET")}, now loading')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Download sample file from bucket')
    parser.add_argument('--sample_file',
                        required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    load_bucket_sample_file(args.sample_file)

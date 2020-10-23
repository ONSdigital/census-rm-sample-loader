# Census sample loader
This project contains a simplified sample loading script for Response Management case setup. (Currently in use for performance test setup on Kubernetes) It will take as arguments a sample CSV file, a Collection Exercise UUID and an Action Plan UUID.

The Sample Loader will generate UUIDs for Sample Units and place messages (See example.xml for format) directly onto the Case.CaseDelivery queue. Case service will then create corresponding Cases.
All of the attributes will be added to the queue as part of the message
  

## Setting up the python environment
This project uses pyenv and pipenv for python version and dependency management, install with
```shell script
brew install pyenv pipenv
```

Install dependencies with
```shell script
make build
```

Enter the environment shell with
```shell script
pipenv shell
```

## Building and pushing the docker container
```shell script
docker build -t eu.gcr.io/census-rm-ci/census-rm-sample-loader:<TAG> .
docker push eu.gcr.io/census-rm-ci/census-rm-sample-loader:<TAG>
```

## Testing Locally with Docker
To test the script locally you must run a RabbitMQ container. A docker-compose.yml file exists for this purpose.

```shell script
docker-compose up -d
```

Once RabbitMQ is running you can run the sample loader.


## Sample Loader
### Usage
```shell script
pipenv run python load_sample.py sample.csv <COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID>
```
e.g.
```shell script
pipenv run python load_sample.py sample_100000.csv 2fc107ee-96f5-465b-923e-38914ce63e3e 2c64c460-2543-4abe-8728-01bbb0449807
```

### Logging
You can set the global log level with the `LOG_LEVEL` environment variable, when the sample loader runs as a script it defaults to `INFO` logging from script itself and `ERROR` for other log sources (e.g. pika).


### Viewing messages in the Rabbit queue
The Rabbit docker image included in docker-compose.yml has the management plugin enabled. This can be accessed when runnning on http://localhost:15672 use guest:guest as the credentials.


### Running in Kubernetes
To run the load_sample app in Kubernetes 

```shell script
./run_in_kubernetes.sh
```

You can also run it with a specific image rather than the default with
```shell script
IMAGE=fullimagelocation ./run_in_kubernetes.sh
```

This will deploy a sample loader pod in the context your kubectl is currently set to and attach to the shell, allowing you to run the sample loader within the cluster. The pod is deleted when the shell is exited.

### Copying across a sample file
To get a sample file into a pod in kubernetes you can use the `kubectl cp` command

While the sample loader pod is running, from another shell run
```shell script
kubectl cp <path_to_sample_file> <namespace>/<sample_load_pod_name>:<destination_path_on_pod>
```

### Downloading a sample file from bucket
Given a file is in the sample bucket, shell into the sample pod, then run command
```shell script
SAMPLE_BUCKET=<env_name>-sample python download_file_from_bucket.py --sample_file <name_of_file_in_bucket.csv>
```

This will download the file from the bucket onto the persistent volume which is mounted to the directory: /home/sampleloader/sample_files 

## Sample File Validator
The is a validation script provided which performs a basic sanity check of the sample file. 

To run the sample validation locally run
```shell script
pipenv run python validate_sample.py <sample_file>
```

See the `SAMPLE_ROW_SCHEMA` in [`validate_sample.py`](/validate_sample.py) for the schema spec.

## Dummy Sample File Generator
The [`generate_sample_file.py`](/generate_sample_file.py) script generates a dummy sample file of random data designed to have a realistic shape.

Run it with the provided treatment code quantities config:
```shell script
pipenv run python generate_sample_file.py
```

And it will write out the generated file to `sample_file.csv`

To run it with customised config and output path:
```shell script
pipenv run python generate_sample_file.py -o /custom/path.csv -t /path/to/treatment_code_quantities.csv
```
Where the treatment code quantities file is a csv with headers `"Treatment Code"` and `"Quantity"` specifying the quantities of each treatment code to include in the generated sample

An optional flag `-s` or `--sequential_uprn` can be used to generate unique UPRN's sequentially instead of randomly, making it faster to generate a massive file.

## Sample file redactor
The [`redact_sample.py`](/redact_sample.py) script takes in a sample file and outputs the same sample with random data for redacted fields

To redact **all** sensitive fields, run it with the script :
```shell script
pipenv run python redact_sample.py sample_files/my_sample.csv
```
And it will write out the redacted file to `my_sample_redacted.csv`

To redact just the HTC fields, run the script with the flag `--redact-htc-only`:
```shell script
pipenv run python redact_sample.py sample_files/my_sample.csv --redact-htc-only
```

And it will write out the redacted file to `my_sample_htc_redacted_only.csv`

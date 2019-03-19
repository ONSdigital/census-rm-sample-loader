# Census sample loader
This project contains a simplified sample loading script for Response Management case setup. (Currently in use for performance test setup on Kubernetes) It will take as arguments a sample CSV file, a Collection Exercise UUID, Action Plan UUID and Collection Instrument UUID.

The Sample Loader will generate UUIDs for Sample Units and place messages (See example.xml for format) directly onto the Case.CaseDelivery queue. Case service will then create corresponding Cases.

After adding messages to the queue it then loads all sample attributes into Redis keyed by sampleunit:<UUID>. The JSON stored for each sample matches the JSON returned by the current Sample service.
  
Collection Exercises, Collection Instruments and Action Plans must currently be setup either using the social-test-setup scripts https://github.com/ONSdigital/rm-tools/tree/master/social-test-setup or the rasrm-ops UI https://github.com/ONSdigital/rasrm-ops



## Setting up the python environment
This project uses pyenv and pipenv for python version and dependency management, install with
```bash
brew install pyenv pipenv
```

Install dependencies with
```bash
make build
```

Enter the environment shell with
```bash
pipenv shell
```

## building and pushing the docker container
```bash
docker build -t eu.gcr.io/census-rm-ci/census-rm-sample-loader:<TAG> .
docker push eu.gcr.io/census-rm-ci/census-rm-sample-loader:<TAG>
```

## Testing Locally with Docker
To test the script locally you must run RabbitMQ and Redis containers. A docker-compose.yml file exists for this purpose.

```
docker-compose up -d
```

Once running Redis and RabbitMQ are running you can now run the sample loader.
This also runs the stub sample service to retrieve the sample units via an API.

## Usage
```
python load_sample.py sample.csv <COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID> <COLLECTION_INSTRUMENT_UUID>
```
e.g.
```
python load_sample.py sample_100000.csv 2fc107ee-96f5-465b-923e-38914ce63e3e 2c64c460-2543-4abe-8728-01bbb0449807 ec6da84c-2b3b-4445-88c7-17c2171d9063
```

## Vewing messages in the Rabbit queue
The Rabbit docker image included in docker-compose.yml has the management plugin enabled. This can be accessed when runnning on http://localhost:15672 use guest:guest as the credentials.

## Viewing Redis contents
Install the redis cli 
```
brew install redis
```
Then you can list all keys
```
redis-cli
127.0.0.1:6379> keys *
```
To get the contents of a key e.g.
```
127.0.0.1:6379> get sampleunit:44c844ba-3289-48f3-9d11-8a0fc00dc415
```
To clear the contents of redis
```
127.0.0.1:6379> flushall
```

## Running in Kubernetes
To run the load_sample app in Kubernetes 

```bash
./run_in_kubernetes.sh
```

This will deploy a sample loader pod in the context your kubectl is currently set to and attach to the shell, allowing you to run the sample loader within the cluster. The pod is deleted when the shell is exited.

### Copying across a sample file
To get a sample file into a pod in kubernetes you can use the `kubectl cp` command

While the sample loader pod is running, from another shell run
```bash
kubectl cp <path_to_sample_file> <namespace>/<sample_load_pod_name>:<destination_path_on_pod>
```

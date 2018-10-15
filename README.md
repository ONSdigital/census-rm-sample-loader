# Census sample loader
This project contains a simplified sample loading script for Response Management case setup. (Currently in use for performance test setup on Kubernetes) It will take as arguments a sample CSV file, a Collection Exercise UUID, Action Plan UUI and Collection Instrument UUID.

The Loader will generate UUIDs for Sample Units and place messages (See example.xml for format) directly onto the Case.CaseDelivery queue. Case service will then create corresponding Cases.

After adding messages to the queue it then loads all sample attributes into Redis keyed by sampleunit:<UUID>. The JSON stored for each sample matches the JSON returned by the current Sample service.



## Setting up the python environment
```
brew install pyenv
pyenv install
pip install --upgrade pip setuptools pipenv
pipenv install --dev
pipenv shell
```

## building and pushing the docker container
docker build -t sdcplatform/census-sample-loader:latest .
docker push sdcplatform/census-sample-loader:latest

## Testing Locally with Docker
To test the script locally you must run RabbitMQ and Redis containers. A docker-compose.yml file exists for this purpose.

```
docker-compose up -d
```

Once running Redis and RabbitMQ are running you can now run the sample loader

## Usage
```
python loadSample.py sample.csv <COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID> <COLLECTION_INSTRUMENT_UUID>
```
e.g.
```
python loadSample.py Social_Pilot_Sample_100000.csv ed3b1381-efb5-4162-9af6-3d95ca0c543c 4f5e6db7-6f55-4998-b4e5-db234c8740ac 7eadd7b2-ccf1-46c3-acb8-9db450df5521
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
To run the loadSample app in Kubernetes 

```
kubectl run sampleloader --image sdcplatform/census-sample-loader -it --rm /bin/bash
```
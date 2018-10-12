`brew install pyenv`
`pyenv install`
`pip install --upgrade pip setuptools pipenv`
`pipenv install --dev`
`python loadSample.py Social_Pilot_Sample_100000.csv <COLLECTION_EXERCISE_UUID> <ACTIONPLAN_UUID> <COLLECTION_INSTRUMENT_UUID>`

Running the docker image
(locally)
`docker run -it sampleloader:latest --name sampleloader /bin/sh`

once in the image shell run
`python loadSample.py Social_Pilot_Sample_100000.csv 1 2 3`
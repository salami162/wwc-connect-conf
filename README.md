# Women Who Code - CONNECT Conference Workshop

## Setup
The following steps will help you setup a development environment.

1. ### Install pip
```
$ sudo easy_install pip
```

2. ### Install virtualenv
```
$ sudo pip install virtualenv
```

3. ### Clone this repository
```
$ git clone git@github.com:sbalireddi/wwc-connect-conf.git
$ cd wwc-connect-conf
```

4. ### Activate virtual environment
```
$ virtualenv venv
$ source venv/bin/activate
```

5. ### Install the required python packages
```
$ pip install -r requirements.txt
```

6. ### Running the server
```
python manage.py runserver
```
This will launch a server on localhost at port 5000. Hit up the index page at ```http://localhost:5000/```

7. ### Running KMeans
```
python manage.py kmeans -c 4 -src './data/wwc_conf_dataset_tiny.csv' -dest './data/trained_output.csv'
```
Given a csv file of locations, generates clusters and outputs them into another csv file. The following command will output 4 clusters, with the lat/lng of the centers in `./data/trained_output.csv`

## Testing
### Run unit tests
```
$ pytest -v -s tests/unit/utils/test_utils.py
```

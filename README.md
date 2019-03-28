# GAQL

GAQL - The Google Ads Query Language Query Executor

## Setup

It is recommended to use Python virtual evironment.
Python version greater or equal **3.6** is required.

You should have installed **git**, **python**, **pip** and **virtualenv** to proceed with the next steps.

### Dependencies

```bash
git clone https://github.com/dsteb/gaql
cd gaql
python3 -m venv venv
. venv/bin/activate
venv/bin/pip install -r requirements.txt
```

### Credentials

To authenticate your API calls, you must specify your **client ID**, **client secret**, **refresh token**, **developer token**, and, if you are authenticating with a manager account, a **login customer id**.

The default behavior is to load a configuration file named **google-ads.yaml** located in your home directory.
Here you can find a [template](https://github.com/googleads/google-ads-python/blob/master/google-ads.yaml) you can use.

## Run

```bash
FLASK_APP=gaql FLASK_ENV=development venv/bin/flask run
```

Open http://localhost:5000/query

## Tests

### Install dependencies

```bash
venv/bin/pip install -r dev-requirements.txt
```

### Test

```bash
venv/bin/pytest
```

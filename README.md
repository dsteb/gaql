# GAQL

GAQL - The Google Ads Query Language Command Line Tool

## Setup

It is recommended to use Python virtual evironment.
Python version greater or equal **3.6** is required.

You should have installed **git**, **python**, **pip** and **virtualenv** to proceed with the next steps.

### Dependencies

```bash
git clone https://github.com/dsteb/gaql
cd gaql
virtualenv venv --python=python3.6
source venv/bin/activate
pip install -r requirements.txt
```

### Credentials

To authenticate your API calls, you must specify your **client ID**, **client secret**, **refresh token**, **developer token**, and, if you are authenticating with a manager account, a **login customer id**.

The default behavior is to load a configuration file named **google-ads.yaml** located in your home directory.
Here you can find a [template](https://github.com/googleads/google-ads-python/blob/master/google-ads.yaml) you can use.

### Run

```bash
python src/main.py --customer_id 123-456-7890
```

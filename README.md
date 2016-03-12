# Fill minstone status

fill PyCon JP milestone(Google Spreadsheet) status from JIRA.

## Preparation for Mac

```
$ xcode-select --install
```

## install

```
$ git clone git@github.com:pyconjp/fill-milestone-status.git
$ cd fill-milestone-status
$ virtualenv -p python3 env
$ . env/bin/activate
(env)$ pip install -r requirements.txt
```

## Enable Google Drive API

1. Open [Google Developer Console](https://console.developers.google.com/home/dashboard "Google Developer Console")
2. Start a project -> Create a project...
3. Project name: `fill-milestone-status` -> Click `Create` button
4. Select `API Manager` menu
5. Select `Drive API`
6. Click `Enable` button

## Create Client ID for OAuth2

1. Select `Permissions` menu on Google Developer Console
2. Select `Service accounts` -> Click `Create service account` button
3. Enter name of service account -> check `urnish a new private key` -> `JSON` -> Click `Create` button
4. Save `*.json` file

## Share setting on Google spreadsheet

1. Open spreadsheet
2. Click `Share` button
3. Enter email address of Client ID


```
(env)$ cp config.ini.sample config.ini
(env)$ vi config.ini
(env)$ ./fill-milestone-status.py
```

## Confirm access to spreadsheet

```
import json

import gspread
from oauth2client.client import SignedJwtAssertionCredentials

json_key = json.load(open('myproject.json'))
email = json_key['client_email']
key = json_key['private_key'].encode('utf-8')
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(email, key, scope)

gc = gspread.authorize(credentials)

spreadsheet_key = '1jqFebgLJpZT0MpTI9op0wuOJMkZmcZWcPFhiBzHllZM'
spreadsheet = gc.open_by_key(spreadsheet_key)
worksheet =  spreadsheet.sheet1
print(worksheet.title)
```

## Enter JIRA username/password

```
(env)$ cp config.ini.sample config.ini
(env)$ vi config.ini
```

config.ini.sample

```
[JIRA]
username = JIRA username
password = JIRA password
```

## Run script

```
(env)$ ./fill-milestone-status.py
```

# Reference

- [Using OAuth2 for Authorization — gspread 0.3.0 documentation](http://gspread.readthedocs.org/en/latest/oauth2.html "Using OAuth2 for Authorization — gspread 0.3.0 documentation")


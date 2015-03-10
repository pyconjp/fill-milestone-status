======================
 Fill minstone status
======================
fill-milestone-status.py fill PyCon JP milestone(Google Spreadsheet) status from JIRA.

::

  $ virtualenv -p python2 .venv
  $ . .venv/bin/activate
  (.venv)$ pip install -r requirements.txt
  (.venv)$ cp config.ini.sample config.ini
  (.venv)$ vi config.ini.sample
  (.venv)$ ./fill-milestone-status.py

config.ini.sample::
   
   [JIRA]
   username = JIRA username
   password = JIRA password
   
   [Google]
   username = Google Account username
   password = Google Account password

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyCon JP 2015 マイルストーンのスプレッドシートで、各JIRAタスクのステータスを
取得し、スプレードッシート上に書き込むスクリプト
https://docs.google.com/spreadsheet/ccc?key=0Avbw8GEmTD5OdDJkVHRaVjBFWWZ0VTdtdEMyY0NaS0E#gid=16
"""

import ConfigParser

from jira import JIRA

from google_spreadsheet.api import SpreadsheetAPI

# JIRA サーバー
SERVER='https://pyconjp.atlassian.net'

def fill_milestone_status(worksheet, jira):
    """
    指定されたシートのマイルストーンの情報を更新する
    """

    for row in worksheet.get_rows():
        issue_id = row['jira']
        if issue_id != None:
            # issue_id(HTC-XXX)からissueを取得
            issue = jira.issue(issue_id)
            # 状態、期限の列を更新
            row[u'状態'] = issue.fields.status.name
            row[u'期限'] = issue.fields.duedate
            try:
                row[u'担当'] = issue.fields.assignee.name
            except:
                row[u'担当'] = u'未割り当て'
            row = worksheet.update_row(row)

if __name__ == '__main__':
    # config.ini からパラメーターを取得
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    jira_auth = config.get('JIRA', 'username'), config.get('JIRA', 'password')
    google_auth = config.get('Google', 'username'), config.get('Google', 'password')

    # JIRA に接続
    options = {'server': SERVER}
    jira = JIRA(options=options, basic_auth=jira_auth)

    # Google Spreadsheetに接続
    api = SpreadsheetAPI(config.get('Google', 'username'),
                         config.get('Google', 'password'),
                         "hogehoge")
    spreadsheet_key = '0Avbw8GEmTD5OdDJkVHRaVjBFWWZ0VTdtdEMyY0NaS0E'
    for title, key in api.list_worksheets(spreadsheet_key):
        if title == '2015マイルストーン':
            worksheet = api.get_worksheet(spreadsheet_key, key)
            # ワークシートのマイルストーンの状態を入れる
            fill_milestone_status(worksheet, jira)

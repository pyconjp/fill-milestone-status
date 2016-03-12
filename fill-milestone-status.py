#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyCon JP 2015 マイルストーンのスプレッドシートで、各JIRAタスクのステータスを
取得し、スプレードッシート上に書き込むスクリプト
https://docs.google.com/spreadsheet/ccc?key=0Avbw8GEmTD5OdDJkVHRaVjBFWWZ0VTdtdEMyY0NaS0E#gid=16
"""

import configparser
import json

import gspread
from jira import JIRA
from oauth2client.client import SignedJwtAssertionCredentials

# JIRA サーバー
SERVER='https://pyconjp.atlassian.net'

def fill_milestone_status(worksheet, jira):
    """
    指定されたシートのマイルストーンの情報を更新する
    """

    for row in range(2, worksheet.row_count + 1):
        # J列(JIRAのissue id)のデータを取得
        issue_id = worksheet.cell(row, 10).value
        if issue_id.startswith('HTJ'):
            # issue_id(HTC-XXX)からissueを取得
            issue = jira.issue(issue_id)
            # 状態、期限の列を更新
            worksheet.update_cell(row, 7, issue.fields.status.name)
            worksheet.update_cell(row, 8, issue.fields.duedate)
            # 担当者の列を更新
            try:
                worksheet.update_cell(row, 9, issue.fields.assignee.name)
            except:
                worksheet.update_cell(row, 9, '未割り当て')

if __name__ == '__main__':
    # config.ini からパラメーターを取得
    config = configparser.ConfigParser()
    config.read('config.ini')
    jira_auth = config.get('JIRA', 'username'), config.get('JIRA', 'password')

    # JIRA に接続
    options = {'server': SERVER}
    jira = JIRA(options=options, basic_auth=jira_auth)

    # Google Spreadsheetに接続
    json_key = json.load(open('myproject.json'))
    email = json_key['client_email']
    key = json_key['private_key'].encode('utf-8')
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(email, key, scope)

    gc = gspread.authorize(credentials)

    spreadsheet_key = '1jqFebgLJpZT0MpTI9op0wuOJMkZmcZWcPFhiBzHllZM'
    spreadsheet = gc.open_by_key(spreadsheet_key)
    worksheet =  spreadsheet.worksheet('2016マイルストーン')

    # ワークシートのマイルストーンの状態を入れる
    fill_milestone_status(worksheet, jira)

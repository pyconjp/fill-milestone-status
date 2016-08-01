#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PyCon JP 2016 マイルストーンのスプレッドシートで、各JIRAタスクのステータスなどを
取得し、スプレードッシート上に書き込むスクリプト
https://docs.google.com/spreadsheets/d/1jqFebgLJpZT0MpTI9op0wuOJMkZmcZWcPFhiBzHllZM/edit#gid=1989509719
"""

import configparser
import json
import logging

import gspread
from jira import JIRA, JIRAError
from oauth2client.service_account import ServiceAccountCredentials

# JIRA server URL
SERVER='https://pyconjp.atlassian.net'

# jira id/slack id dict
JIRA_SLACK = {
    "angela": "sayaka_angela",
    "massa142": "arai",
    "satisfaction": "manzoku",
    "kitahara": "surgo",
    "Ds110": "ds110",
    "checkpoint": "sekine",
    "hidemasuoka112": "hidetomasuoka",
    "koedoyoshida": "yoshida",
    "yasushihashimoto": "yhashimoto",
    "yutaro.muta": "yutaro",
}

def get_slack_id(jira_id):
    """
    convert JIRA id to slack id
    """

    return JIRA_SLACK.get(jira_id, jira_id)

def create_hyperlink(url, target):
    '''
    create hyperlink text for Google Spreadsheet
    '''
    hyperlink = '=HYPERLINK("{}","{}")'.format(url, target)
    return hyperlink

def update_row(worksheet, row, issue):
    """
    update row of spreadsheet by parameter of issue

    :param worksheet: Google Spreadsheet
    :param row: row number
    :param issue: JIRA issue object
    """

    # issue への link を追加
    issue_url = '{}/browse/{}'.format(SERVER, issue)
    worksheet.update_cell(row, 12, create_hyperlink(issue_url, issue))

    # 優先度、更新日、ステータス、期限の列を更新
    worksheet.update_cell(row, 7, issue.fields.priority.name)
    updated, _ = issue.fields.updated.split('T')
    worksheet.update_cell(row, 8, updated)
    worksheet.update_cell(row, 9, issue.fields.status.name)
    worksheet.update_cell(row, 10, issue.fields.duedate)

    # 担当者の列を更新
    try:
        jira_id = issue.fields.assignee.name
        slack = get_slack_id(jira_id)
        prof_url = 'https://pyconjp.slack.com/team/' + slack
        slack_link = create_hyperlink(prof_url, '@' + slack)
        worksheet.update_cell(row, 11, slack_link)
    except:
        worksheet.update_cell(row, 11, '未割り当て')

    
def fill_milestone_status(worksheet, jira):
    """
    指定されたシートのマイルストーンの情報を更新する
    """

    for row in range(2, worksheet.row_count + 1):
        # J列(JIRAのissue id)のデータを取得
        issue_id = worksheet.cell(row, 12).value.strip()
        status = worksheet.cell(row, 9).value
        if issue_id.startswith('SAR'):
            try:
                # issue_id(SAR-XXX)からissueを取得
                issue = jira.issue(issue_id)
                # スプレッドシート上の情報を更新する
                update_row(worksheet, row, issue)
            except JIRAError:
                pass


def get_google_connection():
    '''
    get google connection for gspread
    '''

    # Google Spreadsheetに接続

    scope = ['https://spreadsheets.google.com/feeds']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'myproject.json', scope)
    
    gc = gspread.authorize(credentials)

    return gc
    
if __name__ == '__main__':
    # config.ini からパラメーターを取得
    config = configparser.ConfigParser()
    config.read('config.ini')
    jira_auth = config.get('JIRA', 'username'), config.get('JIRA', 'password')

    # JIRA に接続
    options = {'server': SERVER}
    jira = JIRA(options=options, basic_auth=jira_auth)

    gc = get_google_connection()

    spreadsheet_key = '1jqFebgLJpZT0MpTI9op0wuOJMkZmcZWcPFhiBzHllZM'
    spreadsheet = gc.open_by_key(spreadsheet_key)
    worksheet =  spreadsheet.worksheet('2016マイルストーン')

    # ワークシートのマイルストーンの状態を入れる
    fill_milestone_status(worksheet, jira)

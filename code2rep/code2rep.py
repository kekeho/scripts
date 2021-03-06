#!/usr/bin/env python3

import sys
import pdfkit
import json
from markdown import markdown
import subprocess

SOURCE_CODE_TITLE = 'ソースコード'
RESULT_TITLE = '実行結果'


def importCode(file_name):
    extension = file_name.split('.')[-1]
    try:
        with open(file_name, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print('No such file: {}'.format(file_name))
        exit()

    return {'file_name': file_name, 'extension': extension, 'code': code}


def makeMD(codes):
    md_str = '# ' + SOURCE_CODE_TITLE + '\n\n'  # title

    # create markdown strings
    for code in codes:
        if code['extension'] is None:
            code['extension'] = ''

        md_str += '\n\n### {}\n'.format(code['file_name'])  # add filename
        md_str += '```{type}\n{code}\n```\n'.format(
            type=code['extension'], code=code['code'])  # add code
    return md_str


def mdToHTML(md_str):
    with open('style.css', 'r') as css_file:
        css = css_file.read()
    html = css + markdown(md_str, extensions=['extra', 'codehilite'])
    return html


def htmlToPDF(html_str):
    options = {
        'page-size': 'A4',
        'margin-top': '0.4in',
        'margin-right': '0.3in',
        'margin-bottom': '0.1in',
        'margin-left': '0.3in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    pdfkit.from_string(html_str, 'report.pdf', options=options)


def makeResult(results, env_file):
    env = json.load(env_file)
    ret = []
    for filename in results:  # 拡張子だけ抽出
        try:
            environment = env[filename.split('.')[1]]  # 拡張子を取得し環境を特定
        except KeyError as e:
            print(
                'Error!\nA file with an extension not in the "environments.json" was entered.')
            exit()

        command = (environment, filename)
        try:
            ret.append({'file_name': 'result ' + filename, 'code': subprocess.check_output(
                command).decode('utf-8'), 'extension': None})
        except subprocess.CalledProcessError as e:
            print('Execute Error!\n', e, ret)  # 実行エラー
            exit()

    return(ret)


def main(files):
    with open('environments.json', 'r') as env_file:
        results = makeResult(files['results'], env_file)
    codes = []
    for source in files['sources']:
        codes.append(importCode(source))

    for result in results:
        codes.append(result)

    md = makeMD(codes)
    html = mdToHTML(md)
    htmlToPDF(html)


def printUsage():
    print("""Usage:
    code2rep.py [OPTION] [SOURCE_FILES] : [RESULT_FILES]
    EXAMPLE: code2rep utils.js main.js : main.js
    
    OPTIONS:
        -m : output markdown only
        -h : output html only
    """)


if __name__ == '__main__':
    sources = []
    results = []

    # argc check
    if len(sys.argv) < 4:
        print('ERROR!')
        printUsage()
        exit()

    # option mode
    if sys.argv[1] in '-':
        if sys.argv[1] is '-m':  # output markdown only
            pass
        elif sys.argv[1] is '-h':
            pass
        else:
            print('ERROR! Unknown Option: {}'.format(sys.argv[1]))
            printUsage()
            exit()

    # normal mode
    cnt = 0
    for i in sys.argv:
        if i is ':':
            break
        sources.append(i)
        cnt += 1
    sources.remove(sys.argv[0])
    [results.append(sys.argv[i]) for i in range(cnt + 1, len(sys.argv))]

    main({'sources': sources, 'results': results})

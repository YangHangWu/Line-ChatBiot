# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
import datetime
import os
import sys
import time
import random
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,LocationSendMessage
)
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
sched = BlockingScheduler()
app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = '454ffd8925294fccf34647a4ee6a8fc0'
channel_access_token = 'Orb15wL5mdZUF6aHTOsPnyx/YOHXKULyZMLZ87CCPzFQNCp3g5/ptBj4derWQ2wVAFpOGzzw+1UFCULdfWBjWaPTNLPX6vF8MpFmtWAGg6xjnIBbr+Oy5FnE7hOt2ZeOj5ik7b89Yd+885CDtpoTTQdB04t89/1O/w1cDnyilFU='

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)



msg_dict={
    '級職':'二兵',
    '姓名':'吳仰航',
    '體溫':'35.5',
    '1.時間':'19:00',
    '2.交通方式':'機車',
    '3.地點':'家',
    '4.密切接觸者':'無（近14日均未出)'
}


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body, "Signature: " + signature)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
       abort(400)

    return 'OK'

reply_date=[]
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    print(event)
    t = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    date = str(t.month)+'/'+str(t.day)+' '+str(t.hour)+':'+str(t.minute)
    body_temperature=35.0+random.randint(0,16)/10
    report_msg='\
    級職：二兵\n\
    姓名：吳仰航\n\
    體溫：'+str(body_temperature)+'\n\
    1.時間：'+date+'\n\
    2.交通方式: 機車\n\
    3.地點：家\n\
    4.密切接觸者：無（近14日均未出)'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=report_msg)
    )
    
@sched.scheduled_job('interval', seconds=3)
def timed_job():
    now = datetime.now()
    current_time = now.strftime("%H")
    current_date=now.strftime("%m")+'/'+now.strftime("%d")

    print("Current Time =", current_time)
    reply_msg=''
    for key in msg_dict.keys():
        reply_msg+=key
        reply_msg+=msg_dict[key]
        reply_msg+='\n'
    try:
        print(reply_msg)
        line_bot_api.push_message('C5ad09ef9a4d6889fa886e60d6ccfa269', [TextSendMessage(text=reply_msg),LocationSendMessage(
    title='我的位置',
    address='806高雄市前鎮區瑞政街56號',
    latitude=22.598579999999998,
    longitude=120.324364
    )])
    except:
        print('error to send msg')

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=5000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    #sched.start()
    app.run()

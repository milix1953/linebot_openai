from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import time
#======python的函數庫==========

#======這裡是呼叫的檔案內容=====
from mongodb_function import *
#======這裡是呼叫的檔案內容=====

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('wNeecpSbD4LVSh7qG+7lP5dKy4ws9S/BxvNU5bgDn4ufCtkK6ipJzH6xE8XwTJkXLsKKGmI7cz+TtbCctuxMiUUTvCCD0w1s1rpWA3OV0h0Q0SoKKUNkHapkPH2xWho2WaAEuWLVfhUhT6I8g6IpvwdB04t89/1O/w1cDnyilFU='))
# Channel Secret
handler = WebhookHandler(os.getenv('e9ec4cc1141ece77dd6173d82037195c'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# # 處理訊息
# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     msg = event.message.text
#     reply_message = TextSendMessage(text="You said: " + msg)
#     line_bot_api.reply_message(event.reply_token, reply_message)

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '最新合作廠商' in msg:
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)

    #======MongoDB操作範例======

    elif '@讀取' in msg:
        datas = read_many_datas()
        datas_len = len(datas)
        message = TextSendMessage(text=f'資料數量，一共{datas_len}條')
        line_bot_api.reply_message(event.reply_token, message)

    elif '@查詢' in msg:
        datas = col_find('events')
        message = TextSendMessage(text=str(datas))
        line_bot_api.reply_message(event.reply_token, message)

    elif '@對話紀錄' in msg:
        datas = read_chat_records()
        print(type(datas))
        n = 0
        text_list = []
        for data in datas:
            if '@' in data:
                continue
            else:
                text_list.append(data)
            n+=1
        data_text = '\n'.join(text_list)
        message = TextSendMessage(text=data_text[:5000])
        line_bot_api.reply_message(event.reply_token, message)

    elif '@刪除' in msg:
        text = delete_all_data()
        message = TextSendMessage(text=text)
        line_bot_api.reply_message(event.reply_token, message)

    #======MongoDB操作範例======

    else:
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token, message)

# 處理 Postback 事件
@handler.add(PostbackEvent)
def handle_postback(event):
    postback_data = event.postback.data
    reply_message = TextSendMessage("You selected: " + postback_data)
    line_bot_api.reply_message(event.reply_token, reply_message)
    print("您按了:" + postback_data)


@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name}歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
        
        
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

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
import openai
import time
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('wNeecpSbD4LVSh7qG+7lP5dKy4ws9S/BxvNU5bgDn4ufCtkK6ipJzH6xE8XwTJkXLsKKGmI7cz+TtbCctuxMiUUTvCCD0w1s1rpWA3OV0h0Q0SoKKUNkHapkPH2xWho2WaAEuWLVfhUhT6I8g6IpvwdB04t89/1O/w1cDnyilFU='))
# Channel Secret
handler = WebhookHandler(os.getenv('e9ec4cc1141ece77dd6173d82037195c'))
# OPENAI API Key初始化設定
openai.api_key = os.getenv('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')


# def GPT_response(text):
#     # 接收回應
#     response = openai.Completion.create(model="text-davinci-003", prompt=text, temperature=0.5, max_tokens=500)
#     print(response)
#     # 重組回應
#     answer = response['choices'][0]['text'].replace('。','')
#     return answer


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    # GPT_answer = GPT_response(msg)
    # print(GPT_answer)
    # line_bot_api.reply_message(event.reply_token, TextSendMessage(GPT_answer))

@handler.add(PostbackEvent)
def handle_message(event):
    print(event.postback.data)


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

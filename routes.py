from flask import Flask, render_template, request
from forms import SignupForm
import subprocess
from subprocess import Popen
import time
import re
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (PeerChannel)
from tradingview_ta import TA_Handler, Interval, Exchange
import trade
import asyncio


app = Flask(__name__)


def get_or_create_eventloop():
  try:
      return asyncio.get_event_loop()
  except RuntimeError as ex:
      if "There is no current event loop in thread" in str(ex):
          loop = asyncio.new_event_loop()
          asyncio.set_event_loop(loop)
          return asyncio.get_event_loop()

app.secret_key = "development-key"

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      print(form.tele_id.data, form.tele_hash.data, form.tele_channel.data, form.accountid.data)
      #asyncio.set_event_loop(asyncio.SelectorEventLoop())
      get_or_create_eventloop().run_until_complete(trade.main(form.tele_id.data, form.tele_hash.data, form.tele_channel.data, form.accountid.data, form.accountkey.data, form.accountsecret.data))
      #client = TelegramClient('session', form.tele_id.data, form.tele_hash.data)
  
      return 'Auto trading start!'


  elif request.method == "GET":
    return render_template('signup.html', form=form)

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)

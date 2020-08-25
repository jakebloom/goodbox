import sys
import ujson
import time
import network
from machine import Pin
from urequests import get

WIFI_LED = Pin(2, Pin.OUT)
MONEY_LED = Pin(13, Pin.OUT)
SURF_LED = Pin(14, Pin.OUT)
MAX_SURF_HEIGHT = 1.3 # in metres for some reason
ENVIRONMENT = {}

def do_connect():
  global ENVIRONMENT
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
      print('connecting to network...')
      wlan.connect(ENVIRONMENT['WIFI_NAME'], ENVIRONMENT['WIFI_PASS'])
      while not wlan.isconnected():
          pass
  print('network config:', wlan.ifconfig())

def load_env():
  envFile = open('./env.json', 'r')
  envJson = ujson.loads(envFile.read())
  global ENVIRONMENT
  ENVIRONMENT = envJson
  print('environment:', ENVIRONMENT)

def fetch_stock():
  global ENVIRONMENT
  res = get('https://finnhub.io/api/v1/quote?symbol={}&token={}'
    .format(ENVIRONMENT['STOCK_TICKER'], ENVIRONMENT['STOCK_TOKEN'])).json()

  if res['c'] > res['o']: # we have made money
    return True
  return False

def fetch_surf():
  res = get('https://us-central1-goodbox-287320.cloudfunctions.net/waves').json()
  height = res["values"][0]["value"]
  return height < MAX_SURF_HEIGHT

def main():
  load_env()

  WIFI_LED.off()
  do_connect()
  WIFI_LED.on()

  while True:
    moneyIsGood = fetch_stock()
    surfIsGood = fetch_surf()

    if moneyIsGood:
      print("money good")
      MONEY_LED.on()
    else:
      print("money bad")
      MONEY_LED.off()

    if surfIsGood:
      print("surf good")
      SURF_LED.on()
    else:
      print("surf bad")
      SURF_LED.off()

    time.sleep(10 * 60)


if __name__ == '__main__':
  main()
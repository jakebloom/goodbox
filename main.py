import ujson
import time
import network
from machine import Pin
from urequests import get

WIFI_LED = Pin(2, Pin.OUT)
MONEY_LED = None
SURF_LED = None
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
  return False

def main():
  load_env()

  WIFI_LED.off()
  do_connect()
  WIFI_LED.on()

  while True:
    moneyIsGood = fetch_stock()
    surfIsGood = fetch_surf()

    if moneyIsGood:
      pass # set money led
    else:
      pass # turn off money led

    if surfIsGood:
      pass # set surf led
    else:
      pass # turn off surf led

    time.sleep(60 * 10) # update again in 10 mins


if __name__ == '__main__':
  main()
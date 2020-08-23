import time
import network
from machine import Pin
from urequests import get

WIFI_LED = Pin(2, Pin.OUT)
MONEY_LED = None
SURF_LED = None

def do_connect():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
      print('connecting to network...')
      wlan.connect('ssid', 'password')
      while not wlan.isconnected():
          pass
  print('network config:', wlan.ifconfig())

def fetch_stock():
  res = get("https://finnhub.io/api/v1/quote?symbol=FB&token=token").json()
  print(res)
  if res["c"] > res["o"]: # If we have made money
    return True
  return False

def fetch_surf():
  pass

WIFI_LED.off()
do_connect()
WIFI_LED.on()

while True:
  moneyIsGood = fetch_stock()
  surfIsGood = fetch_surf()

  if moneyIsGood:
    pass # set money led
  if surfIsGood:
    pass # set surf led

  time.sleep(60 * 10) # update again in 10 mins
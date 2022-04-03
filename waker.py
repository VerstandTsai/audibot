import requests
from time import sleep

while True:
    sleep(10*60)
    requests.get('https://audibot-discord.herokuapp.com/')

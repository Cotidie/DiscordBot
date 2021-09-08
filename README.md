# Discord Bot for 아늑
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Heroku](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)

## Intro
A discord bot to make ease of various nuisances in Mabinogi, a korean classic game. Features include providing guides, schedule notification and event management.

## Installation

### Modules
> discord.py  
> discord-py-slash-command  
> apscheduler     
> requests  
> bs4  
> cssselect   
> selenium  
> pymongo, pymongo[srv]  
> pytz
> 
### Environment Setting
* 'db_host.0' file must be present in the root directory. Ask admin of this file.
* For Windows, make sure you added chromedriver.exe's path to $PATH
* You should provide the bot your Naver ID & PW via Env variables NAVER_ID, NAVER_PW. Also the account should be a member of '마시카' Naver cafe.

## Features(Commands)
: These commands are also visible from the slash(/) prompt on Discord.
* **'/오늘의미션'**
  * Feature: Scrape daily missions from sigkill.kr
* **'/레이드'**
  * Options: '현재' and raid boss names.
  * Feature: Show raid info of each boss. If the option is '현재', a list of raids currently in progress will be displayed.

## Deployment on Heroku
1. Login to heroku CLI and clone heroku git
```shell
> cd ./data/heroku
> heroku login
> heroku git:remote -a <heroku app>
```
2. Register following Env variables
```text
'DB_TOKEN': a token string for MongoDB
'GOOGLE_CHROME_BIN': /app/.apt/usr/bin/google-chrome
'CHROMEDRIVER_PATH': /app/.chromedriver/bin/chromedriver
```
3. Add those buildpacks for chromedriver
```text
https://github.com/heroku/heroku-buildpack-google-chrome
https://github.com/heroku/heroku-buildpack-chromedriver
```
4. Add following snippet for selenium's chromedriver
```python
from selenium import webdriver
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
```
5. Deploy this branch to Heroku app on Heroku website
6. If something fails, run this command to view logs
```shell
> heroku logs -a <heroku app>
```
7. In Resources tab, turn on the main.py

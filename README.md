# Discord Bot for 아늑
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Repl.it](https://img.shields.io/badge/Repl.it-%230D101E.svg?style=for-the-badge&logo=replit&logoColor=white)
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
> 
### Environment Setting
* Must add PhantomJS executable's path to $PATH
* 'db_host.0' file must be present in the root directory. Ask admin of this file.
* For Windows, make sure you added chromedriver.exe's path to $PATH
* You should provide the bot your Naver ID & PW via Env variables NAVER_ID, NAVER_PW. Also the account should be a member of '마시카' Naver cafe.

## Features(Commands)
: These commands are also visible from the slash(/) prompt on Discord.
* **'/오늘의미션'**
  * Aliases: '오미'
  * Feature: Scrape daily missions from sigkill.kr
* **'/레이드정보'**
  * Aliases: '레이드'
  * Feature: 
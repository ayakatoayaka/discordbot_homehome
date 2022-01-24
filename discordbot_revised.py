# インストールした discord.py を読み込む
import discord
import datetime
import schedule
import time
import requests
from bs4 import BeautifulSoup
import re
import config

def job():
    # 自分のBotのアクセストークンに置き換えてください
    TOKEN = config.TOKEN

    intents = discord.Intents.default()
    intents.members = True
    intents.typing = False
    # 接続に必要なオブジェクトを生成
    client = discord.Client(intents=intents)

    print(datetime.datetime.now())

    # 起動時に動作する処理
    @client.event
    async def on_ready():
        # 起動したらターミナルにログイン通知が表示される
        print('ログインしました')
        contestPage = "https://atcoder.jp/contests/"
        
        res = requests.get(contestPage)
        soup = BeautifulSoup(res.text,'html.parser')
        contestLatest = soup.find(id='contest-table-recent').find('tbody').find_all('tr')[0]
        latestContestDate = contestLatest.find('time').text.split(" ")[0]
        # print(latestContestDate)
        
        # if str(datetime.datetime.now()).split(" ")[0] != str(latestContestDate):
        if "2021-12-10" != str(datetime.datetime.now()).split(" ")[0]:
            print("We dosn't have a contest today...")
        else:
            for guild in client.guilds:
                for member in guild.members:
                    if member.nick is not None:                  
                        # CHANNEL_ID = 855833226164305934
            
                        # channel = guild.get_channel(CHANNEL_ID)
                        channel = discord.utils.get(guild.text_channels, name="ほめます")
                        if channel is None:
                            print("This server doesn't have ほめます channel.")
                            break

                        memberPage = 'https://atcoder.jp/users/'+member.nick+'/history'
                        try:
                            res = requests.get(memberPage)
                            soup = BeautifulSoup(res.text,'html.parser')
                            table = soup.find('table')
                            tr = table.find('tbody').find_all('tr')  
                        except:
                            continue

                        print(member.nick)
                        if len(tr) >= 2:
                            pattern = '<span class="user-(.+)">(.+)</span>'
                            currentTr = tr[len(tr)-1]
                            previousTr = tr[len(tr)-2]
                            latestJoinedDate = currentTr.find('time').text.split(" ")[0]
                            if latestContestDate == latestJoinedDate:                               
                                currentColor = currentTr.find('span', class_=re.compile("user"))
                                previousColor = previousTr.find('span', class_=re.compile("user"))
                                currentResults = re.findall(pattern, str(currentColor), re.S)
                                previousResults = re.findall(pattern, str(previousColor), re.S) 
                                if currentColor != previousColor and int(previousResults[0][1]) <= int(currentResults[0][1]):
                                    await channel.send(currentColor+"おめでとう!！！！")
                                elif int(previousResults[0][1]) > int(currentResults[0][1]):
                                    await channel.send(str(int(currentResults[0][1])-int(previousResults[0][1]))+"も下がってる！！！草！")
                                elif int(previousResults[0][1]) <= int(currentResults[0][1]):
                                    await channel.send(str(int(currentResults[0][1])-int(previousResults[0][1]))+"も上がっている！！！神！")                    
                            else:
                                print(member.nick+" didn't join today's contest.")

    # Botの起動とDiscordサーバーへの接続
    client.run(TOKEN)

schedule.every().day.at("18:54").do(job)

  
while True:
  schedule.run_pending()
  time.sleep(60)

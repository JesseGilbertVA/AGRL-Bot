from lib2to3.pgen2 import driver
import discord
import config
import championships
import requests
from bs4 import BeautifulSoup

client = discord.Client()

def getDriverStandings():
    URL = championships.testSeason
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.findAll('table')
    drivers = table[0]
    returnable = []
    drivers_rows = drivers.findAll('tr')
    for dr in drivers_rows:
        dd = dr.findAll('td')
        drow = [id.text.strip() for id in dd]
        if any(drow):
            returnable = returnable + drow
    addX = 4
    while addX < len(returnable):
        returnable.insert(addX, '\n')
        addX += 5
    returnable[0] = '  |  1'
    return(returnable)

def getTeamStandings():
    URL = championships.testSeason
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.findAll('table')
    teams = table[1]
    returnable = []
    teams_rows = teams.findAll('tr')
    for tr in teams_rows:
        td = tr.findAll('td')
        trow = [it.text.strip() for it in td]
        if any(trow):
            returnable = returnable + trow
    addX = 3
    while addX < len(returnable):
        returnable.insert(addX, '\n')
        addX += 4
    returnable[0] = '  |  1'
    return(returnable)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!standings'):
        driverStandings = getDriverStandings()
        driverJoin = '  |  '.join(driverStandings)
        driverString = '**Test Season Driver Standings:**\n' + driverJoin
        await message.channel.send(driverString)
    
    if message.content.lower().startswith('!teamstandings'):
        teamStandings = getTeamStandings()
        teamJoin = '  |  '.join(teamStandings)
        teamString = '**Test Season Team Standings:**\n' + teamJoin
        await message.channel.send(teamString)
    
    if message.content.lower().startswith('!register'):
        await message.channel.send('Register for Season 7 here: ' + championships.season7, reference=message)

#    if message.content.startswith('$kill'):
#            await message.channel.send('goodbye')
#            await client.close()

#    if 'word' in message.content:
#        await message.channel.send('found word')

client.run(config.discordToken)
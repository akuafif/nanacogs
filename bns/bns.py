from __main__ import send_cmd_help
import re
import asyncio
import discord
from discord.ext import commands 
from lxml import etree
import urllib, json
from urllib.parse import quote 
from lxml.html import fromstring, HTMLParser
import requests
from aiohttp import get

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

class BNS:
	def __init__(self, bot):
		self.bot = bot
		
	def eb(text,b,e):
		begin=text.find(b)
		end=text.find(e,begin)
		return text[begin+len(b):end].strip()
		
	@commands.command(pass_context=True)
	async def bns(self, ctx, *text):
		""" Search a character from Blade And Soul Taiwan
		Usage :	rin bns charactername
		"""

		# Class Vars in ascii. Why? Cause im noob, doesnot know how to deal with utf-8 unicode
		blademaster = '\\xe5\\x8a\\x8d\\xe5\\xa3\\xab'
		assassin = '\\xe5\\x88\\xba\\xe5\\xae\\xa2'
		kungfumaster = '\\xe6\\x8b\\xb3\\xe5\\xa3\\xab'
		bladedancer = '\\xe7\\x87\\x90\\xe5\\x8a\\x8d\\xe5\\xa3\\xab'
		forcemaster = '\\xe6\\xb0\\xa3\\xe5\\x8a\\x9f\\xe5\\xa3\\xab'
		summoner = '\\xe5\\x8f\\xac\\xe5\\x96\\x9a\\xe5\\xb8\\xab'
		warlock = '\\xe5\\x92\\x92\\xe8\\xa1\\x93\\xe5\\xb8\\xab'
		gunner = '\\xe6\\xa7\\x8d\\xe6\\x93\\x8a\\xe5\\xa3\\xab'
		soulfighter = '\\xe4\\xb9\\xbe\\xe5\\x9d\\xa4\\xe5\\xa3\\xab'
		destroyer = '\\xe5\\x8a\\x9b\\xe5\\xa3\\xab'

		# Icons
		gunner_icon = 'https://cdn.discordapp.com/attachments/334877847124443136/381108060325675020/shooter.png'
		soulfighter_icon = 'https://cdn.discordapp.com/attachments/334877847124443136/381108077140770816/soulfighter.png'
		warlock_icon = 'https://cdn.discordapp.com/attachments/334877847124443136/381108079116156940/warlock.png'
		summoner_icon = 'https://cdn.discordapp.com/attachments/334877847124443136/381108082131992596/summoner.png'
		forcemaster_icon = 'https://cdn.discordapp.com/attachments/334877847124443136/381108969067773953/forcemaster.png'
		bladedancer_icon = 'https://cdn.discordapp.com/attachments/334877847124443136/381108084732592138/bladedancer.png'
		kungfumaster_icon = 'https://cdn.discordapp.com/attachments/334877847124443136/381108087735582720/kungfufighter.png'
		assassin_icon = 'https://cdn.discordapp.com/attachments/334877847124443136/381108090424262656/assassin.png'
		blademaster_icon = 'https://cdn.discordapp.com/attachments/334877847124443136/381108080710123520/blademaster.png'
		destroyer_icon = 'https://cdn.discordapp.com/attachments/334877847124443136/381134533233344514/destroyer.png'

		# vars
		classname = None
		classicon = None
		level = None
		hmlevel = None
		stats = None

		# Preparing the Name
		name = ''
		stack = ctx.message.content.lower().split()			
		if len(stack) == 3:
			name = stack[2]
		else:
                        await send_cmd_help(ctx)
                        return

		# Need to convert space to URL encoding character
		msgOut = await self.bot.say('*Fetching...*')

		page = await get('http://g.bns.tw.ncsoft.com/ingame/bs/character/profile?c=' + name)
		content = await page.read()
		content = fromstring(str(content).encode('UTF-8'))
		
		# Player ID - Required to make sure the character exist or server timeout
		playerID = content.xpath('//dl[@class="signature"]/dt/a/text()')
		if len(playerID) != 0:
			id = playerID[0]
		else:
			failmsg='1. Character does not exist \n2. Server timed out, try again'
			failEmbed = discord.Embed(colour=0xff0000,title='Failed',description=failmsg)	
			await self.bot.edit_message(msgOut,new_content=' ', embed=failEmbed)
			return

		# Get Player Class, Level
		playerInfo = content.xpath('//dd[@class="desc"]/ul/li/text()')
		classname = playerInfo[0]
		level = playerInfo[1]	

		# Translate to readable english Classname
		if classname == bladedancer: 
			classname = 'Lyn Blade Dancer'
			classicon = bladedancer_icon
		elif classname == blademaster: 
			classname = 'Blade Master'
			classicon = blademaster_icon
		elif classname == assassin: 
			classname = 'Assassin'
			classicon = assassin_icon
		elif classname == kungfumaster: 
			classname = 'Kung Fu Master'
			classicon = kungfumaster_icon
		elif classname == forcemaster: 
			classname = 'Force Master'
			classicon = forcemaster_icon
		elif classname == summoner: 
			classname = 'Summoner'
			classicon = summoner_icon
		elif classname == warlock: 
			classname = 'Warlock'
			classicon = warlock_icon
		elif classname == gunner: 
			classname = 'Gunner'
			classicon = gunner_icon
		elif classname == soulfighter: 
			classname = 'Soul Fighter'
			classicon = soulfighter_icon
		elif classname == destroyer:
			classname = 'Destroyer'
			classicon = destroyer_icon
	
		# Player HM Level
		playerHMLv = content.xpath('//span[@class="masteryLv"]/text()')
		if len(playerHMLv) != 0:
			hmlevel = playerHMLv[0]
			hmlevel=re.sub('[^0-9]', '', hmlevel[24:26])
		else:
			hmlevel = '0'


		# Output Embed for stage 1
		# Stage 1 will be just the Level, name, hmlevel
		footer_text = "Coded poorly by rarakat"
		descURL = 'http://g.bns.tw.ncsoft.com/ingame/bs/character/profile?c=' + name

		embed = discord.Embed(colour=0xe241f4,
			description='[{name}]({url})'.format(name=name,url=descURL) )
		embed.title = '{classname}'.format(classname=classname)
		embed.set_thumbnail(url=classicon)
		embed.set_footer(text=footer_text)

		infotext =  'Level: {level}\n' \
			'HM: {hmlevel}' 
		
		level=re.sub('[^0-9]', '', level[-3:])
		embed.add_field(name='__Info__', value=infotext.format(level=level,
			hmlevel=hmlevel))
		
		msgOut = await self.bot.edit_message(msgOut, new_content=' ', embed=embed)


		# Output Embed for stage 2
		# Getting the stats. Server might be too potato. So have to Retry if fail
		# URL : http://g.bns.tw.ncsoft.com/ingame/bs/character/data/abilities.json?c= + name.encode('utf-8')
		while(1):
			url = 'http://g.bns.tw.ncsoft.com/ingame/bs/character/data/abilities.json?c=' + quote(name)
			r = urllib.request.urlopen(url)
			data = json.loads(r.read().decode(r.info().get_param('charset') or 'utf-8'))

			#break if its not fail
			if len(data.keys()) != 1:
				break

		# JSON data for stats and Points distribution
		stats = data['records']['total_ability']
		pointsability = data['records']['point_ability']

		# Getting the elemental stats
		firstelement = None
		firstelementrate = None
		firstelementicon = None
		sencondelement = None
		secondelementrate = None
		secondelementicon = None
		if classicon == assassin_icon:
			firstelement = stats['attack_attribute_lightning_value']
			firstelementrate = stats['attack_attribute_lightning_rate']
			firstelementicon = ':zap:'
			sencondelement = stats['attack_attribute_void_value']
			secondelementrate = stats['attack_attribute_void_value']
			secondelementicon = ':new_moon_with_face:'
		elif classicon == bladedancer_icon:
			firstelement = stats['attack_attribute_lightning_value']
			firstelementrate = stats['attack_attribute_lightning_rate']
			firstelementicon = ':zap:'
			sencondelement = stats['attack_attribute_wind_value']
			secondelementrate = stats['attack_attribute_wind_rate']
			secondelementicon = ':cloud_tornado:'
		elif classicon == blademaster_icon:
			firstelement = stats['attack_attribute_fire_value']
			firstelementrate = stats['attack_attribute_fire_rate']
			firstelementicon = ':fire:'
			sencondelement = stats['attack_attribute_lightning_value']
			secondelementrate = stats['attack_attribute_lightning_rate']
			secondelementicon = ':zap:'
		elif classicon == soulfighter_icon:
			firstelement = stats['attack_attribute_ice_value']
			firstelementrate = stats['attack_attribute_ice_rate']
			firstelementicon = ':snowflake:'
			sencondelement = stats['attack_attribute_earth_value']
			secondelementrate = stats['attack_attribute_earth_rate']
			secondelementicon = ':mountain:'
		elif classicon == forcemaster_icon:
			firstelement = stats['attack_attribute_fire_value']
			firstelementrate = stats['attack_attribute_fire_rate']
			firstelementicon = ':fire:'
			sencondelement = stats['attack_attribute_ice_value']
			secondelementrate = stats['attack_attribute_ice_rate']
			secondelementicon = ':snowflake:'
		elif classicon == summoner_icon:
			firstelement = stats['attack_attribute_wind_value']
			firstelementrate = stats['attack_attribute_wind_rate']
			firstelementicon = ':cloud_tornado:'
			sencondelement = stats['attack_attribute_earth_value']
			secondelementrate = stats['attack_attribute_earth_rate']
			secondelementicon = ':mountain:'
		elif classicon == kungfumaster_icon:
			firstelement = stats['attack_attribute_fire_value']
			firstelementrate = stats['attack_attribute_fire_rate']
			firstelementicon = ':fire:'
			sencondelement = stats['attack_attribute_wind_value']
			secondelementrate = stats['attack_attribute_wind_rate']
			secondelementicon = ':cloud_tornado:'
		elif classicon == warlock_icon:
			firstelement = stats['attack_attribute_ice_value']
			firstelementrate = stats['attack_attribute_ice_rate']
			firstelementicon = ':snowflake:'
			sencondelement = stats['attack_attribute_void_value']
			secondelementrate = stats['attack_attribute_void_rate']
			secondelementicon = ':new_moon_with_face:'
		elif classicon == gunner_icon:
			firstelement = stats['attack_attribute_fire_value']
			firstelementrate = stats['attack_attribute_fire_rate']
			firstelementicon = ':fire:'
			sencondelement = stats['attack_attribute_void_value']
			secondelementrate = stats['attack_attribute_void_rate']
			secondelementicon = ':new_moon_with_face:'		
		elif classicon == destroyer_icon:
			firstelement = stats['attack_attribute_earth_value']
			firstelementrate = stats['attack_attribute_earth_rate']
			firstelementicon = ':mountain:'
			sencondelement = stats['attack_attribute_void_value']
			secondelementrate = stats['attack_attribute_void_rate']
			secondelementicon = ':new_moon_with_face:'

		elementalValue = '{firsticon}: {firstvalue} ({firstrate}%) \n' \
			'{secondicon}: {secondvalue} ({secondrate}%)' \
			.format(firsticon=firstelementicon,
			firstvalue=firstelement,
			firstrate=firstelementrate,
			secondicon=secondelementicon,
			secondvalue=sencondelement,
			secondrate=secondelementrate)
		embed.add_field(name='__Elemental__', value=elementalValue)

                # Getting the offensive stats
		attackpower = stats['attack_power_value']
		attackpoints = pointsability['offense_point']

		pierce = stats['attack_pierce_value']
		accuracy = stats['attack_hit_value']
		accuracyrate = stats['attack_hit_rate']
		crit = stats['attack_critical_value']
		critrate = stats['attack_critical_rate']
		critdmg = stats['attack_critical_damage_value']
		critdmgrate = stats['attack_critical_damage_rate']
		
		offensiveValue = 'AP: {attackpower} :crossed_swords: {attackpoints}\n' \
			'Pierce: {pierce}\n' \
			'Acc: {accuracy} ({accuracyrate}%)\n' \
			'Crit Hit: {crit} ({critrate}%)\n' \
			'Crit Dmg: {critdmg} ({critdmgrate}%)' \
			.format(attackpower=attackpower,
			attackpoints=attackpoints,
			pierce=pierce,
			accuracy=accuracy,
			accuracyrate=accuracyrate,
			crit=crit,
			critrate=critrate,
			critdmg=critdmg,
			critdmgrate=critdmgrate)
		embed.add_field(name='__Attack__', value=offensiveValue)		

		# Gettin the Defensive stats
		defensepoints = pointsability['defense_point']
		health = stats['max_hp']

		defense = stats['defend_power_value']
		defenserate = stats['defend_physical_damage_reduce_rate']
		evasion = stats['defend_dodge_value']
		evasionrate = stats['defend_dodge_rate']
		block = stats['defend_parry_value']
		blockrate = stats['defend_parry_rate']
		critdefense = stats['defend_critical_value']
		critdefenserate = stats['defend_critical_damage_rate']

		defensiveValue = 'HP: {maxhp} :shield: {defensepoints}\n' \
			'Defense: {defense} ({defenserate}%)\n' \
			'Evasion: {evasion} ({evasionrate}%)\n' \
			'Block: {block} ({blockrate}%)\n' \
			'Crit Def: {critdefense} ({critdefenserate}%)' \
			.format(maxhp=health,
			defensepoints=defensepoints,
			defense=defense,
			defenserate=defenserate,
			evasion=evasion,
			evasionrate=evasionrate,
			block=block,
			blockrate=blockrate,
			critdefense=critdefense,
			critdefenserate=critdefenserate)
		embed.add_field(name='__Defense__', value=defensiveValue)

		# Output the final result
		msgOut = await self.bot.edit_message(msgOut, embed=embed)

def setup(bot):
	n = BNS(bot)
	bot.add_cog(n)

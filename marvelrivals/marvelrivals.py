from redbot.core import commands
import json, discord
from datetime import datetime
from urllib.request import Request, urlopen

class MarvelRivals(commands.Cog):
    """Command: <prefix> mrplayer PlayerName"""
    
    def __init__(self, bot):
        self.bot = bot

    def convert_to_preferred_format(self, sec):
        sec = sec % (24 * 3600)
        hour = sec // 3600
        sec %= 3600
        min = sec // 60
        sec %= 60
        print("seconds value in hours:",hour)
        print("seconds value in minutes:",min)
        return "%02d Hr %02d Min %02d Sec" % (hour, min, sec) 
    
    def get_rank(self, id):
        rank_dict = ["Bronze III","Bronze II","Bronze I","Silver III","Silver II","Silver I","Gold III","Gold II","Gold I","Platinum III","Platinum II","Platinum I","Diamond III","Diamond II","Diamond I","Grandmaster III","Grandmaster II","Grandmaster I","Celestial III","Celestial II","Celestial I","Eternity III","Eternity II","Eternity I","One Above All"]
        return rank_dict[id-1]

    @commands.command()
    async def mrplayer(self, ctx, *text):
        """
        Search a player from Marvel Rival.
        Last Update time depends on Public API.
		Usage :	[p]mrplayer playername
        """
        
        name = ''
        stack = ctx.message.content.lower().split()			
        if len(stack) < 3:
            await ctx.send('Search a player from Marvel Rival.\nLast Updated may depends on the API.\nUsage : `[p]mrplayer charactplayernameername`')
            return

        name = ' '.join(stack[2::])
        try:
            # Get player id
            req = Request('https://rivalsmeta.com/api/find-player', method="POST")
            req.add_header('Content-Type', 'application/json')
            req.add_header('User-Agent', 'Mozilla/5.0')
            data = {"name": name}
            data = json.dumps(data)
            data = data.encode()
            html = urlopen(req, data=data).read()
            id_json = json.loads(html)
            id = id_json[0]["aid"]
            
            # Get player stats
            req = Request(url=f'https://rivalsmeta.com/api/player/{id}', 
                          headers={'User-Agent': 'Mozilla/5.0'}
                         )
            html = urlopen(req).read()
            json_data = json.loads(html)
            
            last_updated = datetime.utcfromtimestamp(json_data["player"]["info_update_time"]).strftime('%Y-%m-%d %H:%M:%S')
            
            rank_details = ''
            i = 0
            for key in json_data["player"]["info"]["rank_game_season"]:
                value = json_data["player"]["info"]["rank_game_season"][key]
                tempjson = json.loads(value)
                rank_details += f'Season {i} Rank : {self.get_rank(tempjson["level"])}\n'
                i += 1
                        
            # Creating Header Embed
            embed = discord.Embed(colour=0xe241f4)
            embed.set_author(name=f"Marvel Rival Player Info (Profile Last Updated: {last_updated})", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            embed.set_footer(text=f"Coded by rarakat")
            
            # Adding Embed
            embed.add_field(name="Profile",
                                value=f'Name (id): {json_data["player"]["info"]["name"]} ({json_data["player"]["info"]["aid"]}) \nLevel: {json_data["player"]["info"]["level"]}',
                                inline=False)
            embed.add_field(name='Rank', value=f'**{rank_details}**')
            embed.add_field(name='Matches Overall', value=f'Total win matches: {json_data["stats"]["total_wins"]} / {json_data["stats"]["total_matches"]}')
            embed.add_field(name='Unranked Matches Overall', 
                            value=f'Win / Total: {json_data["stats"]["total_wins"]} / {json_data["stats"]["total_matches"]}\nK/D/A: {json_data["stats"]["unranked"]["total_kills"]} / {json_data["stats"]["unranked"]["total_deaths"]} / {json_data["stats"]["unranked"]["total_assists"]}\nTime Played: {self.convert_to_preferred_format(json_data["stats"]["unranked"]["total_time_played"])}')
            embed.add_field(name='Ranked Matches Overall', 
                            value=f'Win / Total: {json_data["stats"]["ranked_matches_wins"]} / {json_data["stats"]["ranked_matches"]}\nK/D/A: {json_data["stats"]["ranked"]["total_kills"]} / {json_data["stats"]["ranked"]["total_deaths"]} / {json_data["stats"]["ranked"]["total_assists"]}\nTime Played: {self.convert_to_preferred_format(json_data["stats"]["ranked"]["total_time_played"])}')

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {repr(e)}\nOr profile is PRIVATE.")

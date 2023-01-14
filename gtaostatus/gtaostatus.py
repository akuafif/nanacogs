from redbot.core import commands
import urllib.request, json, datetime, discord

class GTAOStatus(commands.Cog):
    """Command: <prefix> [gtaostatus/gtaonews] """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gtaostatus(self, ctx):
        """Pulls the GTA Online PC Service Status"""

        # API url
        url = 'https://support.rockstargames.com/services/status.json'
        # Open and load to json format
        req = urllib.request.Request(url, headers={ 'User-Agent':'Mozilla/5.0' })
        html = urllib.request.urlopen(req).read()
        parsed_json = json.loads(html)
        
        rg_status = {}
        for data in parsed_json["statuses"]:
            if data['name'] == "Grand Theft Auto Online":
                for platform in data['services_platforms']:
                    if platform['name'] == "PC":
                        gtao_pc_header = f"{data['name']} - {platform['name']}"
                        gtao_pc_status = platform['service_status']['status']
                        gtao_pc_stat_last_update = datetime.datetime.strptime(platform['updated'], "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(hours = 8)
                        
                        gtapc_msg = data['message']
                        gtapc_last_update = data['recent_update']
            if data['name'] == "Social Club":
                for platform in data['services_platforms']:
                    sc_header = f"{data['name']} - {platform['name']}"
                    sc_status = platform['service_status']['status']
                    sc_stat_last_update = datetime.datetime.strptime(platform['updated'], "%Y-%m-%dT%H:%M:%S") + datetime.timedelta(hours = 8)
                sc_msg = data['message']
                sc_last_update = data['recent_update']
            if data['name'] == "Rockstar Games Launcher":
                for platform in data['services_platforms']:
                    rg_status[f"{data['name']} - {platform['name']}"] = f"{platform['service_status']['status']} \nAt: {datetime.datetime.strptime(platform['updated'], '%Y-%m-%dT%H:%M:%S')} (GMT+8)"
        
        # Creating the Embed
        embed = discord.Embed(colour=0xe241f4)
        embed.set_author(name=f"Requested by: {ctx.author.display_name}", url=url, icon_url=ctx.author.avatar_url)
        embed.title = f"Rockstar Services Status - {parsed_json['updated']}"
        embed.set_footer(text=f"coded by rarakat")
        #embed.set_thumbnail(url="https://i.imgur.com/axLm3p6.jpeg")
        
        # Adding GTAO PC Service Status
        embed.add_field(name=f"{gtao_pc_header}", 
                        value=f"Status: {gtao_pc_status}\nAt: {gtao_pc_stat_last_update} (GMT+8)")
        
        # Adding Rockstar Social Club Status
        embed.add_field(name=f"{sc_header}", 
                        value=f"Status: {sc_status}\nAt: {sc_stat_last_update} (GMT+8)")
        
        # Adding Rockstar Game Luancher Status
        for k,v in rg_status.items():
            embed.add_field(name=f"{k}", 
                    value=f"Status: {v}")
        
        # Adding GTAO PC Recent Message
        embed.add_field(name=f"{gtao_pc_header} Recent Message", 
                        value=f"{gtapc_msg}\nPosted on: {gtapc_last_update} (GMT+8)", 
                        inline=False)
        
        # Adding Rockstar Social Club Recent Message
        embed.add_field(name=f"{sc_header} Recent Message", 
                        value=f"{sc_msg}\nPosted on: {sc_last_update} (GMT+8)", 
                        inline=False)
        
        await ctx.send(embed=embed)
        
    @commands.command()
    async def gtaonews(self, ctx):
        """Pulls the GTA Online News"""
        # Get List of Events
        url = 'http://prod.cloud.rockstargames.com/titles/gta5/pcros/news/news.json'
        req = urllib.request.Request(url, headers={ 'User-Agent':'Mozilla/5.0' })
        html = urllib.request.urlopen(req).read()
        all_events = json.loads(html)

        # Creating the Embed
        embed = discord.Embed(colour=0xe241f4)
        embed.set_author(name=f"GTA Online Events", url=url)
        embed.set_footer(text=f"Coded by rarakat")
        
        # Load Last 6 Events
        for i in range (0,5):
            # Get latest news
            url = f"https://prod.cloud.rockstargames.com/global/sc/news/{all_events[i]['gm.evt']['d']['k']}/en.json"
            # Open and load to json format
            req = urllib.request.Request(url, headers={ 'User-Agent':'Mozilla/5.0' })
            html = urllib.request.urlopen(req).read()
            parsed_json = json.loads(html)
            event_date = datetime.datetime.fromtimestamp(parsed_json['date']).strftime("%A, %B %d, %Y %I:%M:%S")
        
            # Adding News Embed
            embed.add_field(name=f"{parsed_json['subtitle']} - {event_date} (GMT)", 
                            value=f"{parsed_json['content']}", 
                            inline=False)
            
        await ctx.send(embed=embed)
    
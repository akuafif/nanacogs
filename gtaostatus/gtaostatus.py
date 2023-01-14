from redbot.core import commands
import urllib.request, json, datetime, discord

class GTAOStatus(commands.Cog):
    """Pulls the GTA PC Service Status"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gtaostatus(self, ctx):
        """Command: <prefix> gtaostatus"""

        url = 'https://support.rockstargames.com/services/status.json'
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
        embed = discord.Embed(colour=0xe241f4)#,description=f"")
        embed.set_author(name=f"Requested by: {ctx.author.display_name}", url=url, icon_url=ctx.author.avatar_url)
        embed.title = f"Rockstar Services Status - {parsed_json['updated']}"
        embed.set_footer(text=f"---coded by rarakat")
        
        # Adding GTAO PC Service Status
        embed.add_field(name=f"{gtao_pc_header}", 
                        value=f"Status: {gtao_pc_status}\nAt: {gtao_pc_stat_last_update} (GMT+8)")
        
        # Adding Rockstar Social Club Status
        embed.add_field(name=f"{sc_header}", 
                        value=f"Status: {sc_status}\nAt: {sc_stat_last_update} (GMT+8)")
        
        # Adding Rockstar Game Launcher Status
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
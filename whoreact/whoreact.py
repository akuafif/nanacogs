from redbot.core import commands
import discord

class WhoReact(commands.Cog):
    """Get the unique names of users reacted to a message """

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def whoreact(self, ctx: commands.Context, message: discord.Message):
        """Get the unique names of users reacted to a message 
        Command: <prefix> whoreact [message_id]"""
        
        users = set()
        for reaction in message.reactions:
            async for user in reaction.users():
                users.add(user)
                
        # Creating the Embed
        embed = discord.Embed(colour=0xe241f4)
        embed.set_author(name=f"Who reacted to {message.author.display_name}")
        embed.set_footer(text=f"Coded by rarakat")
        
        # Message content
        embed.add_field(name=f"{message.author.display_name} says:", 
                        value=f"{message.content}", 
                        inline=False)
        
        # User list
        nameslist = '- ' + ('\n- '.join(user.display_name for user in users))
        embed.add_field(name="Users", 
                        value=f"{nameslist}", 
                        inline=False)
        
        # User count
        embed.add_field(name="Total Users:", 
                        value=f"{len(users)}", 
                        inline=False)
        
        await ctx.send(embed=embed)
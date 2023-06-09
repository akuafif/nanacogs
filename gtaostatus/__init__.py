from .gtaostatus import GTAOStatus

async def setup(bot):
    cog = GTAOStatus(bot)
    await bot.add_cog(cog)

from .marvelrivals import MarvelRivals

async def setup(bot):
    cog = MarvelRivals(bot)
    await bot.add_cog(cog)

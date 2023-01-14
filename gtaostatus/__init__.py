from .gtaostatus import GTAOStatus

def setup(bot):
    bot.add_cog(GTAOStatus(bot))


import discord

from discord.ext import commands
from discord.ext.commands import Context



class Help(commands.Cog, name="help"):
    def __init__(self, bot) -> None:
        print("registered!")
        self.bot = bot
    
        
        
    @commands.hybrid_command(name="helpcmd", description="Get help")
    async def helpcmd(self, ctx: Context) -> None:
        print("I'm here")
        embed = discord.Embed(
            title="Help",
            description="Test command!",
            color=0xE02B2B,
        )
        await ctx.send(embed=embed)
        
        
    
async def setup(bot):
    await bot.add_cog(Help(bot))
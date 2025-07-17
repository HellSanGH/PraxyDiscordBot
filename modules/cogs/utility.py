import discord
import json
import base64
import requests
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands
from ..embed_builder import embed_builder
from ..button_view import ButtonView 
import re
import time


def retrieve_mc(username):
    api_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(api_url)
    if response.status_code == 200:
        profile = response.json()
        uuid = profile['id']
        api_url2 = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        response = requests.get(api_url2)
        profile_data = response.json()
        uuid = profile_data['id']
        name = profile_data['name']
        skin_url = f"https://mc-heads.net/body/{uuid}/right"
        decoded_bytes = base64.b64decode(profile_data['properties'][0]['value'])
        decoded = json.loads(decoded_bytes.decode('utf-8'))
        download_url = decoded['textures']['SKIN']['url']
        try:
            model = decoded['textures']['SKIN']['metadata']['model']
        except:
            model = ""
        try:
            cape = decoded['textures']['CAPE']['url']
            
            cape_map = {
                "http://textures.minecraft.net/texture/2340c0e03dd24a11b15a8b33c2a7e9e32abb2051b2481d0ba7defd635ca7a933": "Migrator Cape <:capeMigrator:1204004538567233536>",
                "http://textures.minecraft.net/texture/9e507afc56359978a3eb3e32367042b853cddd0995662913fb00f7": "Mojang Studios Cape <:capeMojangStudios:1204004559115259934>",
                "http://textures.minecraft.net/texture/f9a76537647989f9a0b6d001e320dac591c359e9e61a31f4ce11c88f207f0ad4": "Vanilla Cape <:capeVanilla:1204004578316521483>",
                "http://textures.minecraft.net/texture/17912790ff164b93196f08ba71d0e62129304776d0f347334f8a6eae509f8a56": "Realm Mapmaker Cape <:capeRealmsmapmaker:1204004564240572476>",
                "http://textures.minecraft.net/texture/953cac8b779fe41383e675ee2b86071a71658f2180f56fbce8aa315ea70e2ed6": "Minecon 2011 Cape <:capeMinecon2011:1204004542916599818>",
                "http://textures.minecraft.net/texture/a2e8d97ec79100e90a75d369d1b3ba81273c4f82bc1b737e934eed4a854be1b6": "Minecon 2012 Cape <:capeMinecon2012:1204004545987092501>",
                "http://textures.minecraft.net/texture/153b1a0dfcbae953cdeb6f2c2bf6bf79943239b1372780da44bcbb29273131da": "Minecon 2013 Cape <:capeMinecon2013:1204004547870068756>",
                "http://textures.minecraft.net/texture/b0cc08840700447322d953a02b965f1d65a13a603bf64b17c803c21446fe1635": "Minecon 2015 Cape <:capeMinecon2015:1204004550386655242>",
                "http://textures.minecraft.net/texture/e7dfea16dc83c97df01a12fabbd1216359c0cd0ea42f9999b6e97c584963e980": "Minecon 2016 Cape <:capeMinecon2016:1204004552370814976>",
                "http://textures.minecraft.net/texture/8f120319222a9f4a104e2f5cb97b2cda93199a2ee9e1585cb8d09d6f687cb761": "Mojang Classic Cape <:capeMojangclassic:1204004556959387668>",
                "http://textures.minecraft.net/texture/5786fe99be377dfb6858859f926c4dbc995751e91cee373468c5fbf4865e7151": "Mojang Cape <:capeMojang:1204004555361222676>",
                "http://textures.minecraft.net/texture/ae677f7d98ac70a533713518416df4452fe5700365c09cf45d0d156ea9396551": "Mojira Moderator Cape <:capeMojiramoderator:1204004747120738364>",
                "http://textures.minecraft.net/texture/1bf91499701404e21bd46b0191d63239a4ef76ebde88d27e4d430ac211df681e": "Translator Cape <:capeTranslator:1204004573551796235>",
                "http://textures.minecraft.net/texture/ca35c56efe71ed290385f4ab5346a1826b546a54d519e6a3ff01efa01acce81": "Cobalt Cape <:capeCobalt:1204004534121406515>",
                "http://textures.minecraft.net/texture/3efadf6510961830f9fcc077f19b4daf286d502b5f5aafbd807c7bbffcaca245": "Scrolls Champion Cape <:capeScrolls:1204007001445634048>",
                "http://textures.minecraft.net/texture/2262fb1d24912209490586ecae98aca8500df3eff91f2a07da37ee524e7e3cb6": "Chinese Translator Cape <:capeTranslator:1204004573551796235>",
                "http://textures.minecraft.net/texture/ca29f5dd9e94fb1748203b92e36b66fda80750c87ebc18d6eafdb0e28cc1d05f": "Cheapsh0t's Cape <:capeTranslator:1204004573551796235>",
                "http://textures.minecraft.net/texture/5048ea61566353397247d2b7d946034de926b997d5e66c86483dfb1e031aee95": "Turtle Cape <:capeTurtle:1204004575552479242>",
                "http://textures.minecraft.net/texture/2056f2eebd759cce93460907186ef44e9192954ae12b227d817eb4b55627a7fc": "Birthday Cape <:capeBirthday:1204004529364795412>",
                "http://textures.minecraft.net/texture/d8f8d13a1adf9636a16c31d47f3ecc9bb8d8533108aa5ad2a01b13b1a0c55eac": "Prismarine Cape <:capePrismarine:1204004561828843570>",
                "http://textures.minecraft.net/texture/70efffaf86fe5bc089608d3cb297d3e276b9eb7a8f9f2fe6659c23a2d8b18edf": "Millionth Customer Cape <:capeMillionth:1204004540890746921>",
                "http://textures.minecraft.net/texture/bcfbe84c6542a4a5c213c1cacf8979b5e913dcb4ad783a8b80e3c4a7d5c8bdac": "dannyBstyle's Cape <:capeDB:1204004536717545492>",
                "http://textures.minecraft.net/texture/23ec737f18bfe4b547c95935fc297dd767bb84ee55bfd855144d279ac9bfd9fe": "JulianClark's Cape <:capeSnowman:1204004715596226601>",
                "http://textures.minecraft.net/texture/2e002d5e1758e79ba51d08d92a0f3a95119f2f435ae7704916507b6c565a7da8": "MrMessiah's Cape <:capeSpade:1204004570896928869>",
                "http://textures.minecraft.net/texture/afd553b39358a24edfe3b8a9a939fa5fa4faa4d9a9c3d6af8eafb377fa05c2bb": "Cherry Blossom Cape <:capeCherryBlossom:1204004532271714354>",
                "http://textures.minecraft.net/texture/cb40a92e32b57fd732a00fc325e7afb00a7ca74936ad50d8e860152e482cfbde": "Twitch Cape"
            }
            cape = cape_map.get(cape, cape)

            
        except:
            cape = ""

        return [skin_url, uuid, name, download_url, cape, model]
    elif response.status_code == 404:
        return None
    else:
        return None
    

class Utility(commands.Cog, name="utility"):
    def __init__(self, bot) -> None:
        print(f"[COG] Registered {self.__class__.__name__} Cog")
        self.bot = bot
    
    @commands.hybrid_command(
        name="minecraftuser",
        description="Receive information on a minecraft user")
    
    @app_commands.describe(username="The Minecraft username to look up.")
    async def minecraftuser(self, ctx: Context, username: str):
        await ctx.defer()
        retrieve = retrieve_mc(username)

        if retrieve:
            skin_url = retrieve[0]
            uuid = retrieve[1]
            name = retrieve[2]
            download_url = retrieve[3]
            cape = retrieve[4]
            model = retrieve[5]
            
            cape_of = ""
            cape_url = f"http://s.optifine.net/capes/{name}.png"
            try:
                response_of = requests.head(cape_url, timeout=5)
                if response_of.status_code == 200:
                    cape_of = cape_url
            except requests.exceptions.RequestException:
                pass

            skin_format = "Slim" if model else "Wide"
            
            embed = discord.Embed(
                title=f"{name}'s Minecraft Profile",
                description=""
            )
            embed = embed_builder(ctx, embed, use_default_thumbnail=False)
            
            embed.add_field(name="UUID", value=f"`{uuid}`", inline=False)
            embed.add_field(name="Skin Format", value=skin_format, inline=False)
            
            if cape:
                embed.add_field(name="Currently Worn Cape", value=cape, inline=False)

            is_capeof = bool(cape_of)
            if is_capeof:
                embed.set_image(url=cape_of)
            
            embed.set_thumbnail(url=skin_url)
            
            view = ButtonView()
            view.add_button(download_url, "Download Skin")
            namemc_link = f"https://namemc.com/profile/{name}"
            view.add_button(namemc_link, "NameMC Page")
            if is_capeof:
                view.add_button(cape_of, "Optifine Cape")
            
            await ctx.send(embed=embed, view=view)
        else:
            error_embed = discord.Embed(description=f"Username '{username}' was not found. This may be due to the rate limit of the Mojang API.")
            error_embed = embed_builder(ctx, error_embed, use_color=2)
            await ctx.send(embed=error_embed, ephemeral=True)
            
            
    @app_commands.command(
        name="lovecalc",
        description="Calculate the love between two users (with accuracy fr fr)"
    )
    async def love_calc(self, interaction: discord.Interaction, user1: str, user2: str): # Add self and type hint for interaction
        try:
            # Extract user IDs from mentions (e.g., "<@123456789>")
            user1n = int(user1.strip('<@!>')) # Use .strip() for robustness
            user2n = int(user2.strip('<@!>'))
        except ValueError: # Be specific with exception
            await interaction.response.send_message("Please provide 2 valid user mentions (e.g., `@User1 @User2`).", ephemeral=True)
            return
        except IndexError: # Catches if string is too short/malformed
            await interaction.response.send_message("Please provide 2 valid user mentions (e.g., `@User1 @User2`).", ephemeral=True)
            return

        # Basic validation for mention format (optional, as strip() and int() handle some cases)
        if not re.match(r'<@!?\d+>', user1) or not re.match(r'<@!?\d+>', user2):
            await interaction.response.send_message("Please provide 2 valid user mentions (e.g., `@User1 @User2`).", ephemeral=True)
            return

        # Explicitly convert to set for easier comparison with pre-defined sets
        users_set = {user1n, user2n}

        # Define special cases (these should be at the class level or outside if truly global constants)
        # For simplicity, defined inside the command for now, but consider scope.
        hellbonnie = {481998330549764106, 1185973996055965799}
        hellgab = {415974992308862977, 481998330549764106}
        gabbonnie = {415974992308862977, 1185973996055965799}
        crystalpraxy = {1170434322453504093, 1186799421636231208}
        crystal = {1170434322453504093}

        love: int # Declare type hint for 'love'
        if users_set == hellbonnie:
            love = 100
        elif users_set == hellgab:
            love = 100
        elif users_set == gabbonnie:
            love = 0
        elif users_set == crystalpraxy:
            love = 100
        elif (user1n in crystal) or (user2n in crystal): # Check if *either* user is Crystal
            love = 0
        else:
            # Original calculation: (user1n / user2n * 31415) % 100
            # Handle potential ZeroDivisionError if user2n is 0 (though Discord IDs are positive)
            if user2n == 0: # Extremely unlikely with Discord IDs, but good practice
                love = 0 # Or some other default
            else:
                love = int(user1n / user2n * 31415 % 100)

        print(f"[PNH Logs] (lovecalc) love is estimated to {love}")

        comment = "" # Initialize comment
        if love < 10 and (user1n not in crystal) and (user2n not in crystal):
            comment = r"I may be wrong but uhh love may not be compatible with these two-"
        elif users_set == crystalpraxy:
            comment = r"AAAAAAAAAAAAAAA AAAAAARGJOJRTOHTJO I love Crystal so much 💀💀 it's so true \<3 ..."
        elif (user1n in crystal) or (user2n in crystal):
            comment = r"Nobody loves Crystal SMHH (Besides me ,-, >.<)"
        elif 10 <= love < 30:
            comment = r"Not that high but doesn't mean it's impossible. Wait and see lol"
        elif 30 <= love < 40:
            comment = r"Can feel something between em, still very decent"
        elif 40 <= love < 60:
            comment = r"Pretty average, y'all got all your chances"
        elif 60 <= love < 70:
            comment = r"Eyyy this is starting to be some good score ngl"
        elif 70 <= love < 80:
            comment = r"Awww, you both have to make up fr"
        elif 80 <= love < 100:
            comment = r"\<3 DAMN if you want intimacy, just let us know and we'll let you be"
        elif love == 100:
            comment = r"You are made for each other... \<33"

        embed = discord.Embed(
            title=r"Lovecalc <3", # Changed raw string r"Lovecalc \<3" to normal "Lovecalc <3"
            description=f"I'd estimate the love between {user1} and {user2} to be {love}%...\n{comment}",
            color=0x30b521
        )
        embed.set_footer(text=f"Command requested by {interaction.user.display_name} at {time.ctime()}", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
import discord
import os
from collections import deque
from discord.ext import commands
from discord.ext.commands import Context
from ..embed_builder import embed_builder

music_queue = deque()
last_play_channel_id = None

class Music(commands.Cog, name="music"):
    def __init__(self, bot) -> None:
        self.bot = bot
        print("Music cog loaded!")

    def get_music_list(self):
        music_directory = "musics"
        music_list = []
        if not os.path.exists(music_directory):
            os.makedirs(music_directory)
        for filename in os.listdir(music_directory):
            if filename.endswith(".mp3"):
                music_list.append(filename[:-4].lower())
        print(f"[PNH Logs] Music list: {music_list}")
        return music_list

    async def on_music_end(self, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return

        voice_client = guild.voice_client

        if music_queue:
            print(f"There's a queue and next music is {music_queue[0]}")
            if voice_client and voice_client.is_playing():
                voice_client.stop()
            
            next_music_name = music_queue.popleft()
            file_path = f"musics/{next_music_name.capitalize()}.mp3"
            audio_source = discord.FFmpegPCMAudio(file_path)

            if voice_client and not voice_client.is_playing():
                voice_client.play(audio_source, after=lambda e: self.bot.loop.create_task(self.on_music_end(guild.id)))
                
                queue_message = self.format_queue()
                now_playing = f"🎵 **Now Playing** 🎵 | {next_music_name.capitalize()}\n{queue_message}"
                embed = discord.Embed(
                    description=now_playing,
                )
                
                if last_play_channel_id:
                    target_channel = guild.get_channel(last_play_channel_id)
                    if target_channel:
                        embed = embed_builder(None, embed, target_channel.guild.me) 
                        await target_channel.send(embed=embed)
            else:
                print(f"Voice client is not ready or is already playing in on_music_end: {voice_client}")
        else:
            if last_play_channel_id:
                last_channel = guild.get_channel(last_play_channel_id)
                if last_channel:
                    embed = discord.Embed(
                        title="Queue Empty",
                        description="There are no more songs in the queue.",
                    )
                    embed = embed_builder(None, embed, last_channel.guild.me)
                    await last_channel.send(embed=embed)

    def format_queue(self):
        if not music_queue:
            return "The queue is empty."
        queue_message = "\n".join([f"> {music.capitalize()}" for music in music_queue])
        return f"**Queue:**\n{queue_message}"
    '''
    @commands.hybrid_command(name="play", description="Plays a music that is in the list of available musics.")
    async def play(self, ctx: Context, music_name: str):
        global last_play_channel_id
        voice_client = ctx.guild.voice_client

        if not ctx.author.voice or not ctx.author.voice.channel:
            embed = discord.Embed(description="You are not connected to a voice channel.")
            embed = embed_builder(ctx, embed)
            await ctx.send(embed=embed, ephemeral=True)
            return

        user_voice_channel = ctx.author.voice.channel
        if voice_client and voice_client.is_connected():
            bot_voice_channel = voice_client.channel
            if user_voice_channel != bot_voice_channel:
                embed = discord.Embed(description="You are not in the same voice channel as the bot.")
                embed = embed_builder(ctx, embed)
                await ctx.send(embed=embed, ephemeral=True)
                return
        else:
            await user_voice_channel.connect()
            voice_client = ctx.guild.voice_client

        if music_name.lower() not in self.get_music_list():
            embed = discord.Embed(
                description=f"**Could not find \"{music_name.capitalize()}\"**. You may choose musics through {self.get_music_list()}.",
            )
            embed = embed_builder(ctx, embed)
            await ctx.send(embed=embed, ephemeral=True)
            return

        if voice_client and voice_client.is_playing():
            music_queue.append(music_name.lower())
            queue_message = self.format_queue()
            embed = discord.Embed(
                description=f"**{music_name.capitalize()}** has been added to the queue.\n\n{queue_message}",
            )
            embed = embed_builder(ctx, embed)
            await ctx.send(embed=embed)
        else:
            await ctx.defer()
            last_play_channel_id = ctx.channel.id 

            file_path = f"musics/{music_name.capitalize()}.mp3"
            audio_source = discord.FFmpegPCMAudio(file_path)

            if voice_client and not voice_client.is_playing():
                voice_client.play(audio_source, after=lambda e: self.bot.loop.create_task(self.on_music_end(ctx.guild.id)))
                
                queue_message = self.format_queue()
                now_playing = f"🎵 **Now Playing** 🎵 | {music_name.capitalize()}\n{queue_message}"
                embed = discord.Embed(
                    description=now_playing,
                )
                embed = embed_builder(ctx, embed)
                await ctx.send(embed=embed)
            else:
                print(f"Voice client is not ready or is already playing: {voice_client}")
    '''
    '''
    @commands.hybrid_command(name="skip", description="Skips the current music and plays the next one in the queue.")
    async def skip(self, ctx: Context):
        voice_client = ctx.guild.voice_client

        if not ctx.author.voice or not ctx.author.voice.channel:
            embed = discord.Embed(
                description="You are not connected to a voice channel.",
            )
            embed = embed_builder(ctx, embed)
            await ctx.send(embed=embed, ephemeral=True)
            return
        
        user_voice_channel = ctx.author.voice.channel
        if not voice_client or not voice_client.is_connected():
            embed = discord.Embed(
                description="The bot is not connected to a voice channel.",
            )
            embed = embed_builder(ctx, embed)
            await ctx.send(embed=embed, ephemeral=True)
            return
        
        bot_voice_channel = voice_client.channel
        if user_voice_channel != bot_voice_channel:
            embed = discord.Embed(
                description="You are not in the same voice channel as the bot.",
            )
            embed = embed_builder(ctx, embed)
            await ctx.send(embed=embed, ephemeral=True)
            return
        
        if voice_client.is_playing():
            voice_client.stop()
            if music_queue:
                await ctx.defer()
                await self.on_music_end(ctx.guild.id)
            else:
                embed = discord.Embed(
                    description="⏭️ **Skipped** the current music. There are no more songs in the queue.",
                )
                embed = embed_builder(ctx, embed)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                description="There are no songs to skip.",
            )
            embed = embed_builder(ctx, embed)
            await ctx.send(embed=embed, ephemeral=True)
    '''
    '''
    @commands.hybrid_command(name="disconnect", description="Disconnects the bot from the voice channel if it's connected.")
    async def disconnect(self, ctx: Context):
        voice_client = ctx.guild.voice_client

        if not voice_client or not voice_client.is_connected():
            embed = discord.Embed(
                description="The bot is not connected to a voice channel.",
            )
            embed = embed_builder(ctx, embed)
            await ctx.send(embed=embed, ephemeral=True)
            return

        await voice_client.disconnect()

        embed = discord.Embed(
            description="The bot has been disconnected from the voice channel.",
        )
        embed = embed_builder(ctx, embed)
        await ctx.send(embed=embed)
    '''

async def setup(bot):
    await bot.add_cog(Music(bot))
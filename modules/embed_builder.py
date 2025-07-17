import time
from .config_parser import config
import discord
from discord.ext import commands

DEFAULT_COLOR = config.get("default_color", 0x30B521)
SYSTEM_COLOR = config.get("system_color", 0x8C8B8B)
RED_COLOR = config.get("red_color", 0xFF0000)
YELLOW_COLOR = config.get("yellow_color", 0xEAFF00)
BLUE_COLOR = config.get("blue_color", 0x0066FF)
config_default_thumbnail_url = config.get("default_embed_thumbnail", "")
config_default_displaytime = config.get("default_embed_displaytime", False)

def embed_builder(
    source_obj: object,
    embed: discord.Embed,
    use_color: int = 0,
    use_default_thumbnail: bool = None,
    use_default_displaytime: bool = None
) -> discord.Embed:
    
    color_map = {
        0: DEFAULT_COLOR,
        1: SYSTEM_COLOR,
        2: RED_COLOR,
        3: YELLOW_COLOR,
        4: BLUE_COLOR,
    }

    apply_thumbnail = use_default_thumbnail if use_default_thumbnail is not None else (config_default_thumbnail_url and config_default_thumbnail_url.lower() != "none")
    apply_displaytime = use_default_displaytime if use_default_displaytime is not None else config_default_displaytime

    if embed.color is None:
        selected_color = color_map.get(use_color, DEFAULT_COLOR)
        embed.color = selected_color

    if apply_thumbnail and config_default_thumbnail_url:
        if not embed.thumbnail or not embed.thumbnail.url:
            embed.set_thumbnail(url=config_default_thumbnail_url)
    
    if apply_displaytime:
        user_name = "Unknown User" # Default value
        
        # Determine the user from either Context or Interaction
        if isinstance(source_obj, commands.Context):
            user_name = str(source_obj.author)
        elif isinstance(source_obj, discord.Interaction):
            user_name = str(source_obj.user) # Use .user for Interaction
        
        embed.set_footer(text=f"Command requested by {user_name} at {time.ctime()}")
    
    return embed
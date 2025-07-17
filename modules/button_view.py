import discord

class ButtonView(discord.ui.View):
    def __init__(self):
        super().__init__()
        
    def add_button(self, url, label):
        button = discord.ui.Button(label=label, url=url)
        self.add_item(button)
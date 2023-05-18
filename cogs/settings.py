"""Contains general, but useful commands for the bot"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.db import DB


class Settings(commands.GroupCog, name='settings'):
    """Cog for Utility commands"""

    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        super().__init__()

    @app_commands.command(name='muterole', description='Configure the bot')
    @app_commands.describe(role='The mute role')
    async def muterole(self, interaction: discord.Interaction, role: discord.Role):
        """sets the muterole for the server

        Args:
            interaction (discord.Interaction): The discord interaction
        """
        settings_collection = DB.get_collection('settings')
        settings_collection.update_one(
            { 'server_id': interaction.guild_id },
            { '$set': {'mute_role': role.id} },
            upsert=True
        )
        await interaction.response.send_message(f'Mute role set to {role.name} ({role.id})')

async def setup(bot: commands.Bot):
    """Sets up the cog

    Args:
        bot (commands.Bot): The bot logged in
    """
    await bot.add_cog(Settings(bot))

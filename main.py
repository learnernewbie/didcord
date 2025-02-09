import discord
from discord.ext import commands
import asyncio
import logging
import json
import os
from utils.config import DEFAULT_SERVER_ID, COMMAND_PREFIX, get_token

# Bot setup with proper intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=COMMAND_PREFIX,
            intents=intents,
            help_command=None,
            description="A Discord bot for managing server events and calculations"
        )
        self.initial_extensions = ['cogs.events', 'cogs.calculator']

    async def setup_hook(self):
        """Initial setup after bot is ready"""
        print("Loading extensions...")
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
                print(f"Loaded extension {extension}")
            except Exception as e:
                print(f"Failed to load extension {extension}: {e}")

        # Sync commands with Discord
        print("Syncing commands...")
        try:
            print("Syncing guild commands...")
            guild = discord.Object(id=DEFAULT_SERVER_ID)
            # Clear existing commands first
            self.tree.clear_commands(guild=guild)
            await self.tree.sync(guild=guild)
            print("✅ Commands synced successfully!")
        except discord.HTTPException as e:
            print(f"❌ Failed to sync commands: {e}")
        except Exception as e:
            print(f"❌ An unexpected error occurred while syncing commands: {e}")

bot = Bot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    target_guild = bot.get_guild(DEFAULT_SERVER_ID)
    if target_guild:
        print(f"Successfully connected to server: {target_guild.name}")
    else:
        print(f"Warning: Could not find server with ID {DEFAULT_SERVER_ID}")

    await bot.change_presence(activity=discord.Game(name=f"{COMMAND_PREFIX}help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Please wait {error.retry_after:.2f}s before using this command again.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command!")
    elif isinstance(error, commands.CommandInvokeError):
        if isinstance(ctx, discord.Interaction):
            if not ctx.response.is_done():
                await ctx.response.send_message(f"An error occurred: {str(error.original)}", ephemeral=True)
            else:
                await ctx.followup.send(f"An error occurred: {str(error.original)}", ephemeral=True)
        else:
            await ctx.send(f"An error occurred: {str(error.original)}")
    else:
        if isinstance(ctx, discord.Interaction):
            if not ctx.response.is_done():
                await ctx.response.send_message(f"An error occurred: {str(error)}", ephemeral=True)
            else:
                await ctx.followup.send(f"An error occurred: {str(error)}", ephemeral=True)
        else:
            await ctx.send(f"An error occurred: {str(error)}")

async def main():
    token = get_token()
    try:
        await bot.start(token)
    except discord.errors.LoginFailure:
        print("Failed to login: Invalid Discord bot token")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
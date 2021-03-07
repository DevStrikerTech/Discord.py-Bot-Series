import json
import discord
import datetime
from random import randint
from discord.ext import commands


class GlobalChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def globalchatstart(self, ctx, channel):
        guild_id = ctx.message.guild.id
        channel_id = int(channel.strip('<>#'))

        with open('.\\databases\\global_chat.json', 'r') as file:
            global_chat_data = json.load(file)
            new_global_chat = str(guild_id)

            # Existing global chat
            if new_global_chat in global_chat_data:
                await ctx.send(':no_entry: **Channel has already added to global chat!**')

            # Add new global chat
            else:
                global_chat_data[new_global_chat] = channel_id
                with open('.\\databases\\global_chat.json', 'w') as new_global_chat:
                    json.dump(global_chat_data, new_global_chat, indent=4)

                await ctx.send(':white_check_mark: **Channel has been added to global chat!**')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def globalchatstop(self, ctx):
        guild_id = ctx.message.guild.id

        with open('.\\databases\\global_chat.json', 'r') as file:
            global_chat_data = json.load(file)

        global_chat_data.pop(str(guild_id))

        # Update global chat
        with open('.\\databases\\global_chat.json', 'w') as update_global_chat_file:
            json.dump(global_chat_data, update_global_chat_file, indent=4)

        await ctx.send(':white_check_mark: **Channel has been removed from global chat!**')

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if not message.content.startswith('!'):
                with open('.\\databases\\global_chat.json', 'r') as file:
                    global_chat_data = json.load(file)

                channel_id = list(global_chat_data.values())

                # Message sender
                if message.channel.id in channel_id:

                    # Unsupported message content
                    if not message.content:
                        return

                    # Message receiver
                    for ids in channel_id:
                        if message.channel.id != ids:
                            message_embed = discord.Embed(colour=randint(0, 0xffffff))

                            message_embed.timestamp = datetime.datetime.utcnow()
                            message_embed.set_author(icon_url=message.author.avatar_url, name=f'{message.author}')
                            message_embed.description = f'**`Said: {message.content}`**'
                            message_embed.set_footer(icon_url=message.guild.icon_url, text=message.guild.name)

                            await self.bot.get_channel(ids).send(embed=message_embed)


def setup(bot):
    bot.add_cog(GlobalChat(bot))

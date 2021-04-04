import json
from discord.ext import commands
from apis.perspective_api import perspective_api


class AiModeration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def startmoderation(self, ctx, mod_channel):
        guild_id = ctx.message.guild.id
        mod_channel_id = int(mod_channel.strip('<>#'))

        with open('./databases/moderation.json', 'r') as file:
            moderation_data = json.load(file)
            moderation_guild = str(guild_id)

            # Update existing moderation data
            if moderation_guild in moderation_data:
                for item in list(moderation_data.values()):
                    if str(mod_channel_id) not in item:
                        moderation_data[moderation_guild] += [str(mod_channel_id)]
                        with open('./databases/moderation.json', 'w') as update_moderation_data:
                            json.dump(moderation_data, update_moderation_data, indent=4)

                        await ctx.send(f':white_check_mark: '
                                       f'**`{ctx.channel}` channel has been registered for moderation!**')

                    else:
                        await ctx.send(f':no_entry: '
                                       f'**`{ctx.channel}` channel already registered for moderation!**')

            # Add new moderation data
            else:
                moderation_data[moderation_guild] = [str(mod_channel_id)]
                with open('./databases/moderation.json', 'w') as new_moderation_data:
                    json.dump(moderation_data, new_moderation_data, indent=4)

                await ctx.send(f':white_check_mark: '
                               f'**`{ctx.channel}` channel has been registered for moderation!**')

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stopmoderation(self, ctx, mod_channel):
        mod_channel_id = int(mod_channel.strip('<>#'))

        with open('./databases/moderation.json', 'r') as file:
            moderation_data = json.load(file)

            for remove_keys, remove_values in moderation_data.items():
                if str(mod_channel_id) in remove_values:
                    remove_values.remove(str(mod_channel_id))

                    with open('./databases/moderation.json', 'w') as update_moderation_file:
                        json.dump(moderation_data, update_moderation_file, indent=4)

                    await ctx.send(f':white_check_mark: **`{ctx.channel}` channel has been removed from moderation!**')

                else:
                    await ctx.send(f':no_entry: **`{ctx.channel}` channel is not registered for moderation!**')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('./databases/moderation.json', 'r') as file:
            moderation_data = json.load(file)

        moderation_data.pop(str(guild.id))

        with open('./databases/moderation.json', 'w') as update_file:
            json.dump(moderation_data, update_file, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.content.startswith('!'):
            if not message.author.bot:
                with open('./databases/moderation.json', 'r') as file:
                    moderation_data = json.load(file)

                    for guild_ids, channel_ids in moderation_data.items():
                        if str(message.channel.id) in channel_ids:

                            # Unsupported message content
                            if not message.content:
                                return

                            moderation_result = perspective_api(message.content)
                            moderation_category = [key for (key, value) in moderation_result.items() if value is True]

                            if any((category in moderation_category for category in ['INSULT', 'TOXICITY', 'SPAM'])):
                                with open('./databases/karma.json', 'r') as karma_file:
                                    karma_data = json.load(karma_file)
                                    user_karma = str(message.author.id)

                                    if user_karma in karma_data:
                                        # Ban user
                                        if 4 in list(karma_data.values()):
                                            with open('./databases/karma.json', 'r') as karma_ban:
                                                karma_ban_user = json.load(karma_ban)

                                            karma_ban_user.pop(str(message.author.id))

                                            with open('./databases/karma.json', 'w') as update_karma_ban:
                                                json.dump(karma_data, update_karma_ban, indent=4)

                                            await message.delete(delay=None)
                                            await message.author.ban()

                                        # Kick user
                                        elif 3 in list(karma_data.values()):
                                            karma_data[user_karma] += 1
                                            with open('./databases/karma.json', 'w') as update_karma_kick:
                                                json.dump(karma_data, update_karma_kick, indent=4)

                                            await message.delete(delay=None)
                                            await message.author.kick()

                                        # Warn user
                                        else:
                                            karma_data[user_karma] += 1
                                            with open('./databases/karma.json', 'w') as update_karma_warn:
                                                json.dump(karma_data, update_karma_warn, indent=4)

                                            await message.delete(delay=None)
                                            await message.channel.send(f'<@{message.author.id}> '
                                                                       f':warning: **for insult/toxic/spam in chat!**')
                                    else:
                                        karma_data[user_karma] = 1
                                        with open('./databases/karma.json', 'w') as new_karma_data:
                                            json.dump(karma_data, new_karma_data, indent=4)

                                        await message.delete(delay=None)
                                        await message.channel.send(f'<@{message.author.id}> '
                                                                   f':warning: **for insult/toxic/spam in chat!**')


def setup(bot):
    bot.add_cog(AiModeration(bot))

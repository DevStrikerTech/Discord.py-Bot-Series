import json
import discord
from datetime import datetime
from discord.ext import commands, tasks


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3',
                      '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3', '\U0001F51F']

    @commands.Cog.listener()
    async def on_ready(self):
        self.poll_result.start()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # Remove poll
        with open('.\\databases\\poll.json', 'r') as file:
            poll_data = json.load(file)

        # Remove schedule
        with open('.\\databases\\scheduler.json', 'r') as file:
            scheduler_data = json.load(file)

        if str(message.id) in poll_data:
            poll_data.pop(str(message.id))

            with open('.\\databases\\poll.json', 'w') as update_poll_data:
                json.dump(poll_data, update_poll_data, indent=4)

            scheduler_data.pop(str(message.channel.id))

            with open('.\\databases\\scheduler.json', 'w') as update_scheduler_data:
                json.dump(scheduler_data, update_scheduler_data, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def poll(self, ctx, time: int, vote: int, title, *options):
        if len(options) > 10:
            await ctx.send(':no_entry: You can only have **10 options** at maximum!')

        elif time <= 15:
            await ctx.send(':no_entry: Please provide poll end time grater then **15 minute**!')

        elif 1000000 < vote:
            await ctx.send(':no_entry: Please provide poll maximum number of vote less then **million**!')

        else:
            with open('.\\databases\\scheduler.json', 'r') as scheduler_file:
                scheduler_data = json.load(scheduler_file)

                if str(ctx.message.channel.id) not in scheduler_data:
                    polls = [('\u200b',
                              '\n'.join([f'{self.emoji[index]} {option} \n' for index, option in enumerate(options)]),
                              False)]

                    embed = discord.Embed(title=title,
                                          description=f':stopwatch: Poll will end in **{time} minute**!',
                                          colour=0xFF0000)

                    embed.set_thumbnail(
                        url=f'https://cdn.discordapp.com/icons/{ctx.message.guild.id}/{ctx.message.guild.icon}.png')

                    for name, value, inline in polls:
                        embed.add_field(name=name, value=value, inline=inline)

                    message = await ctx.send(embed=embed)

                    for item in self.emoji[:len(options)]:
                        await message.add_reaction(item)

                    # Poll data
                    with open('.\\databases\\poll.json', 'r') as poll_file:
                        poll_data = json.load(poll_file)
                        new_message = str(message.id)

                        poll_dictionary = dict.fromkeys(list(options), 0)
                        poll_data[new_message] = [poll_dictionary]

                        with open('.\\databases\\poll.json', 'w') as new_poll_data:
                            json.dump(poll_data, new_poll_data, indent=4)

                    # Poll schedule
                    scheduler_data[message.channel.id] = {'message_id': message.id, 'scheduler_time': time,
                                                          'poll_start_time': datetime.now().isoformat(),
                                                          'max_vote': vote}

                    with open('.\\databases\\scheduler.json', 'w') as new_scheduler_data:
                        json.dump(scheduler_data, new_scheduler_data, indent=4)

                else:
                    await ctx.send(f':no_entry: **Channel is currently occupied with poll!**')

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id != self.bot.user.id:
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

            with open('.\\databases\\poll.json', 'r') as poll_file:
                poll_data = json.load(poll_file)

                if str(payload.message_id) in poll_data:
                    # Time and max vote calculation
                    with open('.\\databases\\scheduler.json', 'r') as schedule:
                        scheduler_data = json.load(schedule)

                    max_vote_count = 0
                    time_counter = 0

                    for item in scheduler_data.items():
                        if str(payload.channel_id) in item[0]:
                            max_vote_count += item[1]['max_vote']

                            cur_time = datetime.now()
                            prev_time = datetime.strptime(item[1]['poll_start_time'].replace('T', ' '),
                                                          '%Y-%m-%d %H:%M:%S.%f')
                            time_delta = (cur_time - prev_time)
                            total_seconds = time_delta.total_seconds()
                            calc_minutes = total_seconds / 60

                            if int(calc_minutes) <= 0:
                                time_counter += item[1]['scheduler_time']
                            else:
                                time_counter += item[1]['scheduler_time'] - int(calc_minutes)

                    # Add poll count
                    if payload.emoji.name == '1⃣' and list(poll_data[str(payload.message_id)][0].values())[
                        0] < max_vote_count:
                        first_poll = list(poll_data[str(payload.message_id)][0].keys())[0]
                        poll_data[str(payload.message_id)][0][first_poll] += 1

                        with open('.\\databases\\poll.json', 'w') as update_poll_data:
                            json.dump(poll_data, update_poll_data, indent=4)

                        await reaction.remove(payload.member)

                    elif payload.emoji.name == '2⃣' and list(poll_data[str(payload.message_id)][0].values())[
                        1] < max_vote_count:
                        second_poll = list(poll_data[str(payload.message_id)][0].keys())[1]
                        poll_data[str(payload.message_id)][0][second_poll] += 1

                        with open('.\\databases\\poll.json', 'w') as update_poll_data:
                            json.dump(poll_data, update_poll_data, indent=4)

                        await reaction.remove(payload.member)

                    elif payload.emoji.name == '3⃣' and list(poll_data[str(payload.message_id)][0].values())[
                        2] < max_vote_count:
                        third_poll = list(poll_data[str(payload.message_id)][0].keys())[2]
                        poll_data[str(payload.message_id)][0][third_poll] += 1

                        with open('.\\databases\\poll.json', 'w') as update_poll_data:
                            json.dump(poll_data, update_poll_data, indent=4)

                        await reaction.remove(payload.member)

                    elif payload.emoji.name == '4⃣' and list(poll_data[str(payload.message_id)][0].values())[
                        3] < max_vote_count:
                        fourth_poll = list(poll_data[str(payload.message_id)][0].keys())[3]
                        poll_data[str(payload.message_id)][0][fourth_poll] += 1

                        with open('.\\databases\\poll.json', 'w') as update_poll_data:
                            json.dump(poll_data, update_poll_data, indent=4)

                        await reaction.remove(payload.member)

                    elif payload.emoji.name == '5⃣' and list(poll_data[str(payload.message_id)][0].values())[
                        4] < max_vote_count:
                        fifth_poll = list(poll_data[str(payload.message_id)][0].keys())[4]
                        poll_data[str(payload.message_id)][0][fifth_poll] += 1

                        with open('.\\databases\\poll.json', 'w') as update_poll_data:
                            json.dump(poll_data, update_poll_data, indent=4)

                        await reaction.remove(payload.member)

                    elif payload.emoji.name == '6⃣' and list(poll_data[str(payload.message_id)][0].values())[
                        5] < max_vote_count:
                        sixth_poll = list(poll_data[str(payload.message_id)][0].keys())[5]
                        poll_data[str(payload.message_id)][0][sixth_poll] += 1

                        with open('.\\databases\\poll.json', 'w') as update_poll_data:
                            json.dump(poll_data, update_poll_data, indent=4)

                        await reaction.remove(payload.member)

                    elif payload.emoji.name == '7⃣' and list(poll_data[str(payload.message_id)][0].values())[
                        6] < max_vote_count:
                        seventh_poll = list(poll_data[str(payload.message_id)][0].keys())[6]
                        poll_data[str(payload.message_id)][0][seventh_poll] += 1

                        with open('.\\databases\\poll.json', 'w') as update_poll_data:
                            json.dump(poll_data, update_poll_data, indent=4)

                        await reaction.remove(payload.member)

                    elif payload.emoji.name == '8⃣' and list(poll_data[str(payload.message_id)][0].values())[
                        7] < max_vote_count:
                        eighth_poll = list(poll_data[str(payload.message_id)][0].keys())[7]
                        poll_data[str(payload.message_id)][0][eighth_poll] += 1

                        with open('.\\databases\\poll.json', 'w') as update_poll_data:
                            json.dump(poll_data, update_poll_data, indent=4)

                        await reaction.remove(payload.member)

                    elif payload.emoji.name == '9⃣' and list(poll_data[str(payload.message_id)][0].values())[
                        8] < max_vote_count:
                        ninth_poll = list(poll_data[str(payload.message_id)][0].keys())[8]
                        poll_data[str(payload.message_id)][0][ninth_poll] += 1

                        with open('.\\databases\\poll.json', 'w') as update_poll_data:
                            json.dump(poll_data, update_poll_data, indent=4)

                        await reaction.remove(payload.member)

                    elif payload.emoji.name == '🔟' and list(poll_data[str(payload.message_id)][0].values())[
                        9] < max_vote_count:
                        tenth_poll = list(poll_data[str(payload.message_id)][0].keys())[9]
                        poll_data[str(payload.message_id)][0][tenth_poll] += 1

                        with open('.\\databases\\poll.json', 'w') as update_poll_data:
                            json.dump(poll_data, update_poll_data, indent=4)

                        await reaction.remove(payload.member)

                    else:
                        await reaction.remove(payload.member)

                    # Update embed
                    options = list(poll_data[str(payload.message_id)][0].keys())

                    updated_polls = [('\u200b',
                                      '\n'.join(
                                          [f'{self.emoji[index]} {option} \n' for index, option in enumerate(options)]),
                                      False)]

                    poll_graphs = [('\u200b',
                                    ''.join([f'{int(values / (max_vote_count / 7))} **{values}** '
                                             for key, values in
                                             enumerate(list(poll_data[str(payload.message_id)][0].values()))]),
                                    False)]

                    update_embed = discord.Embed(title=message.embeds[0].title,
                                                 description=f':stopwatch: '
                                                             f'Poll will end in **{time_counter} minute**!',
                                                 colour=0xFF0000)

                    update_embed.set_thumbnail(url=message.embeds[0].thumbnail.url)

                    for name, value, inline in updated_polls:
                        update_embed.add_field(name=name, value=value, inline=inline)

                    for graph_name, graph_value, graph_inline in poll_graphs:
                        if reaction.emoji in self.emoji and len(message.reactions) == 1:
                            graph_calculation_1 = int(graph_value.split(' ')[0]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[0])) * ':white_large_square:'

                            graph_poll_count_1 = graph_value.split(' ')[1]

                            update_embed.add_field(name=graph_name,
                                                   value=f'1\u20e3 {graph_calculation_1} {graph_poll_count_1}',
                                                   inline=graph_inline)

                            await message.edit(embed=update_embed)

                        elif reaction.emoji in self.emoji and len(message.reactions) == 2:
                            graph_calculation_1 = int(graph_value.split(' ')[0]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[0])) * ':white_large_square:'
                            graph_calculation_2 = int(graph_value.split(' ')[2]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[2])) * ':white_large_square:'

                            graph_poll_count_1 = graph_value.split(' ')[1]
                            graph_poll_count_2 = graph_value.split(' ')[3]

                            update_embed.add_field(name=graph_name,
                                                   value=f'1\u20e3 {graph_calculation_1} {graph_poll_count_1}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'2\u20e3 {graph_calculation_2} {graph_poll_count_2}',
                                                   inline=graph_inline)

                            await message.edit(embed=update_embed)

                        elif reaction.emoji in self.emoji and len(message.reactions) == 3:
                            graph_calculation_1 = int(graph_value.split(' ')[0]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[0])) * ':white_large_square:'
                            graph_calculation_2 = int(graph_value.split(' ')[2]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[2])) * ':white_large_square:'
                            graph_calculation_3 = int(graph_value.split(' ')[4]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[4])) * ':white_large_square:'

                            graph_poll_count_1 = graph_value.split(' ')[1]
                            graph_poll_count_2 = graph_value.split(' ')[3]
                            graph_poll_count_3 = graph_value.split(' ')[5]

                            update_embed.add_field(name=graph_name,
                                                   value=f'1\u20e3 {graph_calculation_1} {graph_poll_count_1}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'2\u20e3 {graph_calculation_2} {graph_poll_count_2}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'3\u20e3 {graph_calculation_3} {graph_poll_count_3}',
                                                   inline=graph_inline)

                            await message.edit(embed=update_embed)

                        elif reaction.emoji in self.emoji and len(message.reactions) == 4:
                            graph_calculation_1 = int(graph_value.split(' ')[0]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[0])) * ':white_large_square:'
                            graph_calculation_2 = int(graph_value.split(' ')[2]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[2])) * ':white_large_square:'
                            graph_calculation_3 = int(graph_value.split(' ')[4]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[4])) * ':white_large_square:'
                            graph_calculation_4 = int(graph_value.split(' ')[6]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[6])) * ':white_large_square:'

                            graph_poll_count_1 = graph_value.split(' ')[1]
                            graph_poll_count_2 = graph_value.split(' ')[3]
                            graph_poll_count_3 = graph_value.split(' ')[5]
                            graph_poll_count_4 = graph_value.split(' ')[7]

                            update_embed.add_field(name=graph_name,
                                                   value=f'1\u20e3 {graph_calculation_1} {graph_poll_count_1}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'2\u20e3 {graph_calculation_2} {graph_poll_count_2}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'3\u20e3 {graph_calculation_3} {graph_poll_count_3}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'4\u20e3 {graph_calculation_4} {graph_poll_count_4}',
                                                   inline=graph_inline)

                            await message.edit(embed=update_embed)

                        elif reaction.emoji in self.emoji and len(message.reactions) == 5:
                            graph_calculation_1 = int(graph_value.split(' ')[0]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[0])) * ':white_large_square:'
                            graph_calculation_2 = int(graph_value.split(' ')[2]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[2])) * ':white_large_square:'
                            graph_calculation_3 = int(graph_value.split(' ')[4]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[4])) * ':white_large_square:'
                            graph_calculation_4 = int(graph_value.split(' ')[6]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[6])) * ':white_large_square:'
                            graph_calculation_5 = int(graph_value.split(' ')[8]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[8])) * ':white_large_square:'

                            graph_poll_count_1 = graph_value.split(' ')[1]
                            graph_poll_count_2 = graph_value.split(' ')[3]
                            graph_poll_count_3 = graph_value.split(' ')[5]
                            graph_poll_count_4 = graph_value.split(' ')[7]
                            graph_poll_count_5 = graph_value.split(' ')[9]

                            update_embed.add_field(name=graph_name,
                                                   value=f'1\u20e3 {graph_calculation_1} {graph_poll_count_1}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'2\u20e3 {graph_calculation_2} {graph_poll_count_2}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'3\u20e3 {graph_calculation_3} {graph_poll_count_3}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'4\u20e3 {graph_calculation_4} {graph_poll_count_4}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'5\u20e3 {graph_calculation_5} {graph_poll_count_5}',
                                                   inline=graph_inline)

                            await message.edit(embed=update_embed)

                        elif reaction.emoji in self.emoji and len(message.reactions) == 6:
                            graph_calculation_1 = int(graph_value.split(' ')[0]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[0])) * ':white_large_square:'
                            graph_calculation_2 = int(graph_value.split(' ')[2]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[2])) * ':white_large_square:'
                            graph_calculation_3 = int(graph_value.split(' ')[4]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[4])) * ':white_large_square:'
                            graph_calculation_4 = int(graph_value.split(' ')[6]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[6])) * ':white_large_square:'
                            graph_calculation_5 = int(graph_value.split(' ')[8]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[8])) * ':white_large_square:'
                            graph_calculation_6 = int(graph_value.split(' ')[10]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[10])) * ':white_large_square:'

                            graph_poll_count_1 = graph_value.split(' ')[1]
                            graph_poll_count_2 = graph_value.split(' ')[3]
                            graph_poll_count_3 = graph_value.split(' ')[5]
                            graph_poll_count_4 = graph_value.split(' ')[7]
                            graph_poll_count_5 = graph_value.split(' ')[9]
                            graph_poll_count_6 = graph_value.split(' ')[11]

                            update_embed.add_field(name=graph_name,
                                                   value=f'1\u20e3 {graph_calculation_1} {graph_poll_count_1}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'2\u20e3 {graph_calculation_2} {graph_poll_count_2}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'3\u20e3 {graph_calculation_3} {graph_poll_count_3}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'4\u20e3 {graph_calculation_4} {graph_poll_count_4}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'5\u20e3 {graph_calculation_5} {graph_poll_count_5}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'6\u20e3 {graph_calculation_6} {graph_poll_count_6}',
                                                   inline=graph_inline)

                            await message.edit(embed=update_embed)

                        elif reaction.emoji in self.emoji and len(message.reactions) == 7:
                            graph_calculation_1 = int(graph_value.split(' ')[0]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[0])) * ':white_large_square:'
                            graph_calculation_2 = int(graph_value.split(' ')[2]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[2])) * ':white_large_square:'
                            graph_calculation_3 = int(graph_value.split(' ')[4]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[4])) * ':white_large_square:'
                            graph_calculation_4 = int(graph_value.split(' ')[6]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[6])) * ':white_large_square:'
                            graph_calculation_5 = int(graph_value.split(' ')[8]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[8])) * ':white_large_square:'
                            graph_calculation_6 = int(graph_value.split(' ')[10]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[10])) * ':white_large_square:'
                            graph_calculation_7 = int(graph_value.split(' ')[12]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[12])) * ':white_large_square:'

                            graph_poll_count_1 = graph_value.split(' ')[1]
                            graph_poll_count_2 = graph_value.split(' ')[3]
                            graph_poll_count_3 = graph_value.split(' ')[5]
                            graph_poll_count_4 = graph_value.split(' ')[7]
                            graph_poll_count_5 = graph_value.split(' ')[9]
                            graph_poll_count_6 = graph_value.split(' ')[11]
                            graph_poll_count_7 = graph_value.split(' ')[13]

                            update_embed.add_field(name=graph_name,
                                                   value=f'1\u20e3 {graph_calculation_1} {graph_poll_count_1}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'2\u20e3 {graph_calculation_2} {graph_poll_count_2}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'3\u20e3 {graph_calculation_3} {graph_poll_count_3}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'4\u20e3 {graph_calculation_4} {graph_poll_count_4}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'5\u20e3 {graph_calculation_5} {graph_poll_count_5}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'6\u20e3 {graph_calculation_6} {graph_poll_count_6}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'7\u20e3 {graph_calculation_7} {graph_poll_count_7}',
                                                   inline=graph_inline)

                            await message.edit(embed=update_embed)

                        elif reaction.emoji in self.emoji and len(message.reactions) == 8:
                            graph_calculation_1 = int(graph_value.split(' ')[0]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[0])) * ':white_large_square:'
                            graph_calculation_2 = int(graph_value.split(' ')[2]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[2])) * ':white_large_square:'
                            graph_calculation_3 = int(graph_value.split(' ')[4]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[4])) * ':white_large_square:'
                            graph_calculation_4 = int(graph_value.split(' ')[6]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[6])) * ':white_large_square:'
                            graph_calculation_5 = int(graph_value.split(' ')[8]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[8])) * ':white_large_square:'
                            graph_calculation_6 = int(graph_value.split(' ')[10]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[10])) * ':white_large_square:'
                            graph_calculation_7 = int(graph_value.split(' ')[12]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[12])) * ':white_large_square:'
                            graph_calculation_8 = int(graph_value.split(' ')[14]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[14])) * ':white_large_square:'

                            graph_poll_count_1 = graph_value.split(' ')[1]
                            graph_poll_count_2 = graph_value.split(' ')[3]
                            graph_poll_count_3 = graph_value.split(' ')[5]
                            graph_poll_count_4 = graph_value.split(' ')[7]
                            graph_poll_count_5 = graph_value.split(' ')[9]
                            graph_poll_count_6 = graph_value.split(' ')[11]
                            graph_poll_count_7 = graph_value.split(' ')[13]
                            graph_poll_count_8 = graph_value.split(' ')[15]

                            update_embed.add_field(name=graph_name,
                                                   value=f'1\u20e3 {graph_calculation_1} {graph_poll_count_1}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'2\u20e3 {graph_calculation_2} {graph_poll_count_2}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'3\u20e3 {graph_calculation_3} {graph_poll_count_3}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'4\u20e3 {graph_calculation_4} {graph_poll_count_4}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'5\u20e3 {graph_calculation_5} {graph_poll_count_5}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'6\u20e3 {graph_calculation_6} {graph_poll_count_6}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'7\u20e3 {graph_calculation_7} {graph_poll_count_7}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'8\u20e3 {graph_calculation_8} {graph_poll_count_8}',
                                                   inline=graph_inline)

                            await message.edit(embed=update_embed)

                        elif reaction.emoji in self.emoji and len(message.reactions) == 9:
                            graph_calculation_1 = int(graph_value.split(' ')[0]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[0])) * ':white_large_square:'
                            graph_calculation_2 = int(graph_value.split(' ')[2]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[2])) * ':white_large_square:'
                            graph_calculation_3 = int(graph_value.split(' ')[4]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[4])) * ':white_large_square:'
                            graph_calculation_4 = int(graph_value.split(' ')[6]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[6])) * ':white_large_square:'
                            graph_calculation_5 = int(graph_value.split(' ')[8]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[8])) * ':white_large_square:'
                            graph_calculation_6 = int(graph_value.split(' ')[10]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[10])) * ':white_large_square:'
                            graph_calculation_7 = int(graph_value.split(' ')[12]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[12])) * ':white_large_square:'
                            graph_calculation_8 = int(graph_value.split(' ')[14]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[14])) * ':white_large_square:'
                            graph_calculation_9 = int(graph_value.split(' ')[16]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[16])) * ':white_large_square:'

                            graph_poll_count_1 = graph_value.split(' ')[1]
                            graph_poll_count_2 = graph_value.split(' ')[3]
                            graph_poll_count_3 = graph_value.split(' ')[5]
                            graph_poll_count_4 = graph_value.split(' ')[7]
                            graph_poll_count_5 = graph_value.split(' ')[9]
                            graph_poll_count_6 = graph_value.split(' ')[11]
                            graph_poll_count_7 = graph_value.split(' ')[13]
                            graph_poll_count_8 = graph_value.split(' ')[15]
                            graph_poll_count_9 = graph_value.split(' ')[17]

                            update_embed.add_field(name=graph_name,
                                                   value=f'1\u20e3 {graph_calculation_1} {graph_poll_count_1}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'2\u20e3 {graph_calculation_2} {graph_poll_count_2}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'3\u20e3 {graph_calculation_3} {graph_poll_count_3}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'4\u20e3 {graph_calculation_4} {graph_poll_count_4}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'5\u20e3 {graph_calculation_5} {graph_poll_count_5}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'6\u20e3 {graph_calculation_6} {graph_poll_count_6}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'7\u20e3 {graph_calculation_7} {graph_poll_count_7}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'8\u20e3 {graph_calculation_8} {graph_poll_count_8}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'9\u20e3 {graph_calculation_9} {graph_poll_count_9}',
                                                   inline=graph_inline)

                            await message.edit(embed=update_embed)

                        elif reaction.emoji in self.emoji and len(message.reactions) == 10:
                            graph_calculation_1 = int(graph_value.split(' ')[0]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[0])) * ':white_large_square:'
                            graph_calculation_2 = int(graph_value.split(' ')[2]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[2])) * ':white_large_square:'
                            graph_calculation_3 = int(graph_value.split(' ')[4]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[4])) * ':white_large_square:'
                            graph_calculation_4 = int(graph_value.split(' ')[6]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[6])) * ':white_large_square:'
                            graph_calculation_5 = int(graph_value.split(' ')[8]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[8])) * ':white_large_square:'
                            graph_calculation_6 = int(graph_value.split(' ')[10]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[10])) * ':white_large_square:'
                            graph_calculation_7 = int(graph_value.split(' ')[12]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[12])) * ':white_large_square:'
                            graph_calculation_8 = int(graph_value.split(' ')[14]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[14])) * ':white_large_square:'
                            graph_calculation_9 = int(graph_value.split(' ')[16]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[16])) * ':white_large_square:'
                            graph_calculation_10 = int(graph_value.split(' ')[18]) * ':red_square:' + (
                                    7 - int(graph_value.split(' ')[18])) * ':white_large_square:'

                            graph_poll_count_1 = graph_value.split(' ')[1]
                            graph_poll_count_2 = graph_value.split(' ')[3]
                            graph_poll_count_3 = graph_value.split(' ')[5]
                            graph_poll_count_4 = graph_value.split(' ')[7]
                            graph_poll_count_5 = graph_value.split(' ')[9]
                            graph_poll_count_6 = graph_value.split(' ')[11]
                            graph_poll_count_7 = graph_value.split(' ')[13]
                            graph_poll_count_8 = graph_value.split(' ')[15]
                            graph_poll_count_9 = graph_value.split(' ')[17]
                            graph_poll_count_10 = graph_value.split(' ')[19]

                            update_embed.add_field(name=graph_name,
                                                   value=f'1\u20e3 {graph_calculation_1} {graph_poll_count_1}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'2\u20e3 {graph_calculation_2} {graph_poll_count_2}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'3\u20e3 {graph_calculation_3} {graph_poll_count_3}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'4\u20e3 {graph_calculation_4} {graph_poll_count_4}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'5\u20e3 {graph_calculation_5} {graph_poll_count_5}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'6\u20e3 {graph_calculation_6} {graph_poll_count_6}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'7\u20e3 {graph_calculation_7} {graph_poll_count_7}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'8\u20e3 {graph_calculation_8} {graph_poll_count_8}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'9\u20e3 {graph_calculation_9} {graph_poll_count_9}',
                                                   inline=graph_inline)

                            update_embed.add_field(name=graph_name,
                                                   value=f'\U0001F51F {graph_calculation_10} {graph_poll_count_10}',
                                                   inline=graph_inline)

                            await message.edit(embed=update_embed)

                    else:
                        pass

    @tasks.loop(minutes=15)
    async def poll_result(self):
        with open('.\\databases\\scheduler.json', 'r') as schedule_file:
            scheduler_data = json.load(schedule_file)

            for item in scheduler_data.items():
                cur_time = datetime.now()
                prev_time = datetime.strptime(item[1]['poll_start_time'].replace('T', ' '), '%Y-%m-%d %H:%M:%S.%f')

                time_delta = (cur_time - prev_time)
                total_seconds = time_delta.total_seconds()
                calc_minutes = total_seconds / 60

                channel = self.bot.get_channel(int(item[0]))
                message = await channel.fetch_message(item[1]['message_id'])

                with open('.\\databases\\poll.json', 'r') as poll_file:
                    poll_data = json.load(poll_file)

                poll_outcome = max(poll_data[str(message.id)][0].items(), key=lambda i: i[1])

                if int(calc_minutes) > item[1]['scheduler_time'] or poll_outcome[1] >= item[1]['max_vote']:
                    if str(message.id) in poll_data:
                        await channel.send(
                            f':tada: **{poll_outcome[0]}** has won **{message.embeds[0].title}** poll '
                            f'with **{poll_outcome[1]}** votes!')

                        # Remove poll
                        poll_data.pop(str(message.id))
                        with open('.\\databases\\poll.json', 'w') as update_poll_data:
                            json.dump(poll_data, update_poll_data, indent=4)

                        # Remove schedule
                        scheduler_data.pop(str(channel.id))
                        with open('.\\databases\\scheduler.json', 'w') as update_scheduler_data:
                            json.dump(scheduler_data, update_scheduler_data, indent=4)

                            break


def setup(bot):
    bot.add_cog(Poll(bot))

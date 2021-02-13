import json
import discord
import datetime
from tabulate import tabulate
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw


class VoiceLeaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        with open('.\\databases\\voice_leaderboard.json', 'r') as file:
            voice_data = json.load(file)
            new_user = str(member.id)

        # Update existing user
        if new_user in voice_data:
            voice_leave_time = datetime.datetime.now().time().strftime('%H:%M:%S')
            voice_join_time = voice_data[new_user]

            calculate_time = (
                    datetime.datetime.strptime(voice_leave_time, '%H:%M:%S') - datetime.datetime.strptime(
                voice_join_time, '%H:%M:%S'))

            voice_data[new_user] = f'{calculate_time}'

            with open('.\\databases\\voice_leaderboard.json', 'w') as update_user_data:
                json.dump(voice_data, update_user_data, indent=4)

        # Add new user
        else:
            new_voice_join_time = datetime.datetime.now().time().strftime('%H:%M:%S')
            voice_data[new_user] = new_voice_join_time

            with open('.\\databases\\voice_leaderboard.json', 'w') as new_user_data:
                json.dump(voice_data, new_user_data, indent=4)

    @commands.command()
    async def voice(self, ctx):
        with open('.\\databases\\voice_leaderboard.json', 'r') as file:
            voice_data = json.load(file)

        user_ids = list(voice_data.keys())
        user_time_spents = list(voice_data.values())

        new_leaderboard = []

        for index, user_id in enumerate(user_ids, 1):
            new_leaderboard.append([user_id, user_time_spents[index - 1]])

        # Sort leaderboard order by user time spent
        new_leaderboard.sort(key=lambda items: items[1], reverse=True)

        user_rank_column = []
        user_name_column = []
        user_time_spent_column = []

        # User rank
        for rank_index, rank_value in enumerate(new_leaderboard[:10]):
            user_rank_column.append([rank_index + 1])

        # User name
        for name_index, name_value in enumerate(new_leaderboard[:10]):
            user_name_column.append([await self.bot.fetch_user(int(name_value[0]))])

        # User time spend
        for time_spent_index, time_spent_value in enumerate(new_leaderboard[:10]):
            user_time_spent_column.append([time_spent_value[1]])

        # Append column to table
        user_rank_table = tabulate(user_rank_column, tablefmt='plain', headers=['#\n'], numalign='left')
        user_name_table = tabulate(user_name_column, tablefmt='plain', headers=['Name\n'], numalign='left')
        user_time_spent_table = tabulate(user_time_spent_column, tablefmt='plain', headers=['Time Spent\n'],
                                         numalign='left')

        # Image
        image_template = Image.open('.\\assets\\voice_leaderboard_template.png')

        # Font
        font = ImageFont.truetype('theboldfont.ttf', 14)

        # Positions
        rank_text_position = 30, 50
        name_text_position = 80, 50
        rank_time_spent_text_position = 330, 50

        # Draws
        draw_on_image = ImageDraw.Draw(image_template)
        draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
        draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
        draw_on_image.text(rank_time_spent_text_position, user_time_spent_table, 'white', font=font)

        # Save image
        image_template.convert('RGB').save('voice_leaderboard.jpg', 'JPEG')

        await ctx.send(file=discord.File('voice_leaderboard.jpg'))


def setup(bot):
    bot.add_cog(VoiceLeaderboard(bot))

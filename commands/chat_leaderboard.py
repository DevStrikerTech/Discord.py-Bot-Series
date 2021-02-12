import json
import discord
from tabulate import tabulate
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw


class ChatLeaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if not message.content.startswith('!'):
                with open('.\\databases\\chat_leaderboard.json', 'r') as file:
                    chat_data = json.load(file)
                    new_user = str(message.author.id)

                # Update existing user
                if new_user in chat_data:
                    chat_data[new_user] += 1
                    with open('.\\databases\\chat_leaderboard.json', 'w') as update_user_data:
                        json.dump(chat_data, update_user_data, indent=4)

                # Add new user
                else:
                    chat_data[new_user] = 1
                    with open('.\\databases\\chat_leaderboard.json', 'w') as new_user_data:
                        json.dump(chat_data, new_user_data, indent=4)

    @commands.command()
    async def chat(self, ctx):
        with open('.\\databases\\chat_leaderboard.json', 'r') as file:
            chat_data = json.load(file)

        user_ids = list(chat_data.keys())
        user_message_counts = list(chat_data.values())

        new_leaderboard = []

        for index, user_id in enumerate(user_ids, 1):
            new_leaderboard.append([user_id, user_message_counts[index - 1]])

        # Sort leaderboard order by user message count
        new_leaderboard.sort(key=lambda items: items[1], reverse=True)

        user_rank_column = []
        user_name_column = []
        user_message_count_column = []

        # User ranks
        for rank_index, rank_value in enumerate(new_leaderboard[:10]):
            user_rank_column.append([rank_index + 1])

        # User names
        for name_index, name_value in enumerate(new_leaderboard[:10]):
            user_name_column.append([await self.bot.fetch_user(int(name_value[0]))])

        # User message counts
        for message_count_index, message_count_value in enumerate(new_leaderboard[:10]):
            user_message_count_column.append([message_count_value[1]])

        # Add column to table
        user_rank_table = tabulate(user_rank_column, tablefmt='plain', headers=['#\n'], numalign='left')
        user_name_table = tabulate(user_name_column, tablefmt='plain', headers=['Name\n'], numalign='left')
        user_message_count_table = tabulate(user_message_count_column, tablefmt='plain', headers=['Messages\n'],
                                            numalign='left')

        # Image
        image_template = Image.open('.\\assets\\chat_leaderboard_template.png')

        # Font
        font = ImageFont.truetype('theboldfont.ttf', 14)

        # Positions
        rank_text_position = 30, 50
        name_text_position = 80, 50
        message_count_text_position = 350, 50

        # Draws
        draw_on_image = ImageDraw.Draw(image_template)
        draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
        draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
        draw_on_image.text(message_count_text_position, user_message_count_table, 'white', font=font)

        # Save image
        image_template.convert('RGB').save('chat_leaderboard.jpg', 'JPEG')

        await ctx.send(file=discord.File('chat_leaderboard.jpg'))


def setup(bot):
    bot.add_cog(ChatLeaderboard(bot))

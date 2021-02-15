import discord
import pandas as pd
from datetime import datetime
from matplotlib import pyplot
from discord.ext import commands
from apis.covid_api import covid_api_request


class Covid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def covid(self, ctx, country):
        request_result = covid_api_request(f'dayone/country/{country}')

        data_set = [(datetime.strptime(date_index['Date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%b'), death_index['Deaths'])
                    for date_index, death_index in zip(request_result, request_result)]

        # Plot
        data_frame = pd.DataFrame(data_set)
        data_frame.plot(x=0, y=1, color='#00012C', label='Months')

        # Label
        pyplot.title(f'Showing Deaths in {country}')
        pyplot.xlabel('Months')
        pyplot.ylabel('Number of Deaths')

        # Legend
        pyplot.legend(loc='upper left')

        # Color
        pyplot.axes().set_facecolor('#9A1622')

        pyplot.savefig('.\\assets\\covid_death_graph.png', bbox_inches='tight')

        await ctx.send(file=discord.File('.\\assets\\covid_death_graph.png'))


def setup(bot):
    bot.add_cog(Covid(bot))

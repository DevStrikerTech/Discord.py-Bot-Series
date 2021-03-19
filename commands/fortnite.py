import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from apis.fortnite_api import fortnite_api_request


class Fortnite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fs(self, ctx, *args):
        username = list(args)
        format_player_name = '%20'.join(username)

        fortnite_response = fortnite_api_request(username=format_player_name)

        if fortnite_response['status'] == 200:
            # Images
            fortnite_template_image = Image.open('.\\assets\\fortnite_template.png')

            # Fonts
            username_font = ImageFont.truetype('theboldfont.ttf', 50)
            stats_font = ImageFont.truetype('theboldfont.ttf', 40)

            # Positions
            username_position = 135, 163

            # Overall stats
            overall_wins_position = 43, 300
            overall_win_rate_position = 155, 300
            overall_kd_position = 285, 300
            overall_kpm_position = 400, 300
            overall_matches_position = 63, 450
            overall_kills_position = 210, 450
            overall_deaths_position = 350, 450

            # Solo stats
            solo_matches_position = 540, 130
            solo_wins_position = 685, 130
            solo_win_rate_position = 795, 130
            solo_kills_position = 910, 130
            solo_deaths_position = 1050, 130
            solo_kd_position = 1170, 130
            solo_kpm_position = 1270, 130

            # Duo stats
            duo_matches_position = 540, 345
            duo_wins_position = 685, 345
            duo_win_rate_position = 795, 345
            duo_kills_position = 910, 345
            duo_deaths_position = 1050, 345
            duo_kd_position = 1170, 345
            duo_kpm_position = 1270, 345

            # Squad stats
            squad_matches_position = 540, 560
            squad_wins_position = 685, 560
            squad_win_rate_position = 795, 560
            squad_kills_position = 910, 560
            squad_deaths_position = 1050, 560
            squad_kd_position = 1170, 560
            squad_kpm_position = 1270, 560

            # Draws
            draw_on_image = ImageDraw.Draw(fortnite_template_image)

            # Username
            draw_on_image.text(username_position, fortnite_response['data']['account']['name'], 'white',
                               font=username_font)

            # Overall stats
            if fortnite_response['data']['stats']['all']['overall'] is not None:
                draw_on_image.text(overall_wins_position,
                                   str(fortnite_response['data']['stats']['all']['overall']['wins']),
                                   'white', font=stats_font)
                draw_on_image.text(overall_win_rate_position,
                                   str(round(fortnite_response['data']['stats']['all']['overall']['winRate'], 2)),
                                   'white', font=stats_font)
                draw_on_image.text(overall_kd_position,
                                   str(round(fortnite_response['data']['stats']['all']['overall']['kd'], 2)),
                                   'white', font=stats_font)
                draw_on_image.text(overall_kpm_position,
                                   str(round(fortnite_response['data']['stats']['all']['overall']['killsPerMatch'], 2)),
                                   'white', font=stats_font)
                draw_on_image.text(overall_matches_position,
                                   str(fortnite_response['data']['stats']['all']['overall']['matches']),
                                   'white', font=stats_font)
                draw_on_image.text(overall_kills_position,
                                   str(fortnite_response['data']['stats']['all']['overall']['kills']),
                                   'white', font=stats_font)
                draw_on_image.text(overall_deaths_position,
                                   str(fortnite_response['data']['stats']['all']['overall']['deaths']),
                                   'white', font=stats_font)

            # Solo stats
            if fortnite_response['data']['stats']['all']['solo'] is not None:
                draw_on_image.text(duo_matches_position,
                                   str(fortnite_response['data']['stats']['all']['solo']['matches']),
                                   'white', font=stats_font)
                draw_on_image.text(duo_wins_position, str(fortnite_response['data']['stats']['all']['solo']['wins']),
                                   'white', font=stats_font)
                draw_on_image.text(duo_win_rate_position,
                                   str(round(fortnite_response['data']['stats']['all']['solo']['winRate'], 2)),
                                   'white', font=stats_font)
                draw_on_image.text(duo_kills_position,
                                   str(fortnite_response['data']['stats']['all']['solo']['kills']),
                                   'white', font=stats_font)
                draw_on_image.text(duo_deaths_position,
                                   str(fortnite_response['data']['stats']['all']['solo']['deaths']),
                                   'white', font=stats_font)
                draw_on_image.text(duo_kd_position,
                                   str(round(fortnite_response['data']['stats']['all']['solo']['kd'], 2)),
                                   'white', font=stats_font)
                draw_on_image.text(duo_kpm_position,
                                   str(round(fortnite_response['data']['stats']['all']['solo']['killsPerMatch'], 2)),
                                   'white', font=stats_font)

            # Duo stats
            if fortnite_response['data']['stats']['all']['duo'] is not None:
                draw_on_image.text(solo_matches_position,
                                   str(fortnite_response['data']['stats']['all']['duo']['matches']),
                                   'white', font=stats_font)
                draw_on_image.text(solo_wins_position, str(fortnite_response['data']['stats']['all']['duo']['wins']),
                                   'white', font=stats_font)
                draw_on_image.text(solo_win_rate_position,
                                   str(round(fortnite_response['data']['stats']['all']['duo']['winRate'], 2)),
                                   'white', font=stats_font)
                draw_on_image.text(solo_kills_position,
                                   str(fortnite_response['data']['stats']['all']['duo']['kills']),
                                   'white', font=stats_font)
                draw_on_image.text(solo_deaths_position,
                                   str(fortnite_response['data']['stats']['all']['duo']['deaths']),
                                   'white', font=stats_font)
                draw_on_image.text(solo_kd_position,
                                   str(round(fortnite_response['data']['stats']['all']['duo']['kd'], 2)),
                                   'white', font=stats_font)
                draw_on_image.text(solo_kpm_position,
                                   str(round(fortnite_response['data']['stats']['all']['duo']['killsPerMatch'], 2)),
                                   'white', font=stats_font)

            # Squad stats
            if fortnite_response['data']['stats']['all']['squad'] is not None:
                draw_on_image.text(squad_matches_position,
                                   str(fortnite_response['data']['stats']['all']['squad']['matches']),
                                   'white', font=stats_font)
                draw_on_image.text(squad_wins_position, str(fortnite_response['data']['stats']['all']['squad']['wins']),
                                   'white', font=stats_font)
                draw_on_image.text(squad_win_rate_position,
                                   str(round(fortnite_response['data']['stats']['all']['squad']['winRate'], 2)),
                                   'white', font=stats_font)
                draw_on_image.text(squad_kills_position,
                                   str(fortnite_response['data']['stats']['all']['squad']['kills']),
                                   'white', font=stats_font)
                draw_on_image.text(squad_deaths_position,
                                   str(fortnite_response['data']['stats']['all']['squad']['deaths']),
                                   'white', font=stats_font)
                draw_on_image.text(squad_kd_position,
                                   str(round(fortnite_response['data']['stats']['all']['squad']['kd'], 2)),
                                   'white', font=stats_font)
                draw_on_image.text(squad_kpm_position,
                                   str(round(fortnite_response['data']['stats']['all']['squad']['killsPerMatch'], 2)),
                                   'white', font=stats_font)

            # Save image
            fortnite_template_image.convert('RGB').save('fortnite.jpg', 'JPEG')

            await ctx.send(file=discord.File('fortnite.jpg'))

        else:
            await ctx.send(f":no_entry: **{fortnite_response['error']}**")


def setup(bot):
    bot.add_cog(Fortnite(bot))

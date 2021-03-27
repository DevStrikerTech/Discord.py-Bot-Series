import time
import json
from discord.ext import commands, tasks


class VoiceMemberCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.voice_channel_update.start()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        member_id = str(member.id)

        try:
            with open('./databases/voice_member_count.json', 'r') as file:
                voice_member_data = json.load(file)
                new_voice_member_channel = str(member.voice.channel.id)
                new_voice_member_id = str(member.id)

                # Update existing voice data
                if new_voice_member_channel in voice_member_data:
                    for item in list(voice_member_data.values()):
                        if new_voice_member_id not in item:
                            voice_member_data[new_voice_member_channel] += [new_voice_member_id]
                            with open('./databases/voice_member_count.json', 'w') as update_voice_member_data:
                                json.dump(voice_member_data, update_voice_member_data, indent=4)

                                time.sleep(1)

                # Add new voice data
                else:
                    voice_member_data[new_voice_member_channel] = [new_voice_member_id]
                    with open('./databases/voice_member_count.json', 'w') as new_voice_member_data:
                        json.dump(voice_member_data, new_voice_member_data, indent=4)

                        time.sleep(1)

        except AttributeError:
            # Remove voice data
            for remove_keys, remove_values in voice_member_data.items():
                if member_id in remove_values:
                    remove_values.remove(member_id)

            with open('./databases/voice_member_count.json', 'w') as remove_voice_member_data:
                json.dump(voice_member_data, remove_voice_member_data, indent=4)

    @tasks.loop(minutes=10)
    async def voice_channel_update(self):
        # Update all voice channel stats every 10 minutes
        with open('./databases/voice_member_count.json', 'r') as file:
            voice_member_data = json.load(file)

            for routine_update_keys, routine_update_values in voice_member_data.items():
                if not routine_update_values:
                    reset_channel = self.bot.get_channel(int(routine_update_keys))
                    await reset_channel.edit(name=u'\U0001F449 \u0020 0')
                else:
                    update_channel = self.bot.get_channel(int(routine_update_keys))
                    await update_channel.edit(name=u'\U0001F449 \u0020 {}'.format(len(routine_update_values)))


def setup(bot):
    bot.add_cog(VoiceMemberCount(bot))

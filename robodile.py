import os
import discord

class Robodile(discord.Client):

    _WORDLE_BOT_ID = 1211781489931452447
    _WORDLE_OFFENDING_WORDS = ["were playing", "was playing"]

    async def on_ready(self):
        print(f"Logged in as {self.user}!")

    async def on_raw_message_edit(self, payload):        
        # kill "was / were playing" messages by wordle bot
        if payload.data["webhook_id"] == str(self._WORDLE_BOT_ID):
            channel = await client.fetch_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

            if message == None:
                print(f"Unable to find message {payload.data["id"]}")
                return

            for phrase in self._WORDLE_OFFENDING_WORDS:
                if phrase in message.content:
                    try:
                        await message.delete()
                        break
                    except:
                        print(f"Unable to delete message {message.id}. Bad permissions?")
                    
intents = discord.Intents.default()
intents.message_content = True

client = Robodile(intents=intents)
client.run(os.environ["ROBODILE_TOKEN"])

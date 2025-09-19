import os
import discord

class Robodile(discord.Client):

    _WORDLE_BOT_ID = 1211781489931452447
    _WORDLE_OFFENDING_WORDS = ["were playing", "was playing"]
    _INSTAGRAM_REELS_URL = ".instagram.com/reel/"

    async def on_ready(self):
        print(f"Logged in as {self.user}!")

    async def on_message(self, message):
        # Prevents infinite loop on the reels URL embedder
        if message.author.id == self.user.id:
            return

        if self._INSTAGRAM_REELS_URL in message.content:
            index = message.content.find(self._INSTAGRAM_REELS_URL) + 1
            embed_url_buffer = message.content[0:index] + "kk" + message.content[index:]
            sender_name_buffer = None

            if message.author.nick != None:
                sender_name_buffer = message.author.nick
            elif message.author.global_name != None:
                sender_name_buffer = message.author.global_name
            else:
                sender_name_buffer = message.author.name

            message_buffer = f"**{sender_name_buffer} sent a reel:**\n{embed_url_buffer}"

            try:
                await message.channel.send(message_buffer);
                
                try:
                    await message.delete()
                except:
                    print(f"Unable to clean up message {message.id} (embed cleanup).")
            except:
                print(f"Unable to send message to {message.channel.id}. Bad permissions?")

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

from discord.ext import tasks
from discord.ext import commands
import discord

INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.dm_messages = True
INTENTS.members = True
CONDITION_MET = True

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task = self attr

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        self.channel = self.get_channel(1148270150269804634)
        self.target_user = self.get_user(232968815917400064)
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')
        await self.target_user.send("TIMES UP")
        await self.close()

    @tasks.loop(seconds=5)  # task runs every 5 seconds - for running continously with app check/set condition
    async def my_background_task(self):
        # message_pending = False
        # if message_pending:
        #     await self.target_user.send("TIMES UP")
        #     message_pending = False
        pass


    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


# client = MyClient(intents=INTENTS)
# client.run('MTE0ODI2ODM5OTAzODgyODYyNQ.GqAn3o.vk1_BPiB6xeKGO8PDouX4mIhI8d-irbLSxNslE')

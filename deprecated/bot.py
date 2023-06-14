import discord
import random
from collections import Counter

with open("c:/code/dsc") as tokenfile:
    token=tokenfile.readline()
intents=discord.Intents.default()
intents.message_content=True
client=discord.Client(intents=intents)

calcs=[]
brand=["맥","켚엪씌","노","벅어킹","썹"]
brands=[]
users=[]

@client.event
async def on_message(message):
    if message.author=="savethespecies#6225":
        if message.content.startswith("패푸"):
            calcs.append(int(message.content.strip().replace("패푸","")))
            await message.channel.send(f"{sum(calcs)}")
    if message.content=="/햄":
        if not len(users)==3:
            if not message.author in users:
                brands_chosen=random.choice(brand)
                brands.append(brands_chosen)
                brands_count:dict=Counter(brands)
                users.append(message.author)
                await message.channel.send(
                    f"햄버거::{brands_chosen} ({brands_count[brands_chosen]}번 나옴)")
            else:
                await message.channel.send(
                    f"{message.author}는 이미 투표함")
        else:
            await message.channel.send(
                f"{len(users)}")
    elif message.content=="/투":
        await message.channel.send(
            f'''장전된 샌드위치 브랜드 {", ".join(brand)}... {len(brand)}개''')
    elif message.content=="/누":
        await message.channel.send(
            f'''참여자 {len(users)}명''')
client.run(token)
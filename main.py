import asyncio
import random
import time

import discord
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord_slash import SlashCommand
from matplotlib import colors
from selenium import webdriver

intents = discord.Intents.all()
client = commands.Bot(command_prefix="`", intents=intents)
slash = SlashCommand(client, sync_commands=True)
guild_ids = [621266094983872522, 795406865676763178]
memberlist = []
reasonlist = []


def is_Owner_or_admin():
    async def predicate(ctx):
        return ctx.author.id == 398893725842931722 or has_permissions(administrator=True)

    return commands.check(predicate)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="`Jhelp"))
    print("Ready to go")


@client.event
async def on_message(message):
    if message.author in memberlist:
        index = memberlist.index(message.author)
        memberlist.remove(message.author)
        reasonlist.remove(reasonlist[index])
        await message.channel.send(f"Welcome back,Removed your afk status from {message.author.mention}")
    users = message.mentions
    await client.process_commands(message)
    if len(users):
        inter = list(set(users) & set(memberlist))
        if inter:
            for i in inter:
                index = memberlist.index(i)
                await message.channel.send(f"user is not available right now\nreason:{reasonlist[index]}")
        else:
            pass


@client.event
async def on_member_join(member):
    print(f"{member} has joined the server")


@client.command()
async def Jhelp(ctx):
    embed = discord.Embed(
        title="Help center")
    embed.add_field(name="gb", value="Its an 8ball just ask a question ( `gb (question) ) ", inline=True)
    embed.add_field(name="giverole", value="Gives a role to a user $doesnt craete$ (`giverole @user)", inline=True)
    embed.add_field(name="removerole", value="Removes a role from a user (`removerole @user) ", inline=True)
    embed.add_field(name="mute", value="mutes users (`mute @user)", inline=True)
    embed.add_field(name="unmute", value="unmutes user (`unmute @user)", inline=True)
    embed.add_field(name="ban", value="bans a member(`ban @user)", inline=True)
    embed.add_field(name="unban", value="unbans the user (`unban ID)", inline=True)
    embed.add_field(name="kick", value="Kicks user(`kick @user reason)", inline=True)
    embed.add_field(name="make_embed", value="Just makes a simple embed with title and a description (`make_embed)",
                    inline=True)
    embed.add_field(name="invitelink", value="sends a discord bot invite link (`invitelink)")
    embed.add_field(name="clear", value="Deletes messages (`clear number)", inline=True)
    embed.add_field(name="clearmine", value="only deletes your messages (`clearmine number)", inline=True)
    embed.add_field(name="user", value="displays user info (`user @user)", inline=True)
    embed.add_field(name="afk",
                    value="If mentioned,bot will tell them that you are afk with a following reason(`afk sentence)")
    embed.add_field(name="serverinfo", value="displays server info (`serverinfo)", inline=True)
    embed.add_field(name="avatar", value="displays user avatar (`avatar @user)", inline=True)
    embed.add_field(name="members", value="shows every member that has inputted role (`members @role)", inline=True)
    embed.add_field(name="color", value="Shows the hex of that color (`color color)", inline=True)
    embed.add_field(name="unusedroles", value="Displays every unused role in a server (`unusedroles)", inline=True)
    embed.add_field(name="removeallroles", value="Removes all possible roles from user (`removeallroles @user)",
                    inline=True)
    embed.add_field(name="removeallunused", value="Removes all possible unused roles in server (`removeallunused)",
                    inline=True)
    embed.add_field(name="onlyme",
                    value="Everyone who joins vc will be kicked except bots have some alone time (`onlyme)",
                    inline=True)
    embed.add_field(name="onlymeoff",
                    value="Stops OnlyMe and everyone will be able to join, please do this before leaving (`onlymeoff)",
                    inline=True)
    embed.add_field(name="availablevc", value="Shows voice channels with no OnlyMe users (`availablevc)", inline=True)
    embed.add_field(name="requestjoin", value="Requests to join OnlyMe tagged vc (`requestjoin @user)", inline=True)
    embed.add_field(name="removeuser",
                    value="Removes the OnlyMe accepted user (must be the first OnlyMe user in vc) (`removeuser @user)",
                    inline=True)
    embed.add_field(name="img", value="Shows google images of the keyword (`img word)", inline=True)
    about = discord.Embed(title="ABOUT KICK BAN MUTE REMOVEALLROLES REMOVEALLUNUSED", description=
    """ 
    IF the listed commands are not working, its high likely because of permissions
    go in Role settings and make sure to put (the admin role you gave to a bot) at top or just below owner
    the higher it is the more power it has so put that into a consideration.
    """)
    about.set_image(url="https://cdn.discordapp.com/attachments/846048228330962954/856862095614279700/Visual.gif")
    user = ctx.message.author
    await user.send(embed=embed)
    await user.send(embed=about)


@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')


@client.command()
async def invitelink(ctx):
    await ctx.send(
        "https://discord.com/api/oauth2/authorize?client_id=810048628335968288&permissions=0&redirect_uri=https%3A%2F%2Fdiscord.events.stdlib.com%2Fdiscord%2Fauth%2F&scope=bot")


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def gb(ctx, *, question):
    response = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]

    await ctx.send(f"question: {question} \nanswer: {random.choice(response)}")


@gb.error
async def gb_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            "This command is on cooldown 1 use per 5 seconds ({:.2f}s seconds left)".format(error.retry_after))


@client.command(pass_context=True)
@is_Owner_or_admin()
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"hey {user.name} has been given a role called: {role.name}")


@client.command(pass_context=True)
@is_Owner_or_admin()
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f'hey {user.name} has lost a role called: {role.name}')


@client.command(pass_context=True)
@is_Owner_or_admin()
async def mute(ctx, member: discord.Member):
    if member.guild_permissions.administrator:
        await ctx.send("The mentioned user is an admin")
        return
    else:
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(member)
            perms.send_messages = False
            await channel.set_permissions(member, overwrite=perms)

        await ctx.send(F"Muted {member}")


@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Couldn't do that Make sure i have permissions for it")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Couldn't do that Make sure i have permissions for it")
    else:
        raise error


@client.command(pass_context=True)
@is_Owner_or_admin()
async def unmute(ctx, member: discord.Member):
    if member.guild_permissions.administrator:
        await ctx.send("The mentioned user is an admin")
        return
    else:
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(member)
            perms.send_messages = True
            await channel.set_permissions(member, overwrite=perms)

        await ctx.send(F"unMuted {member}")


@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Couldn't do that Make sure i have permissions for it")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("either you are Missing permissions")


@client.command(pass_context=True)
@is_Owner_or_admin()
async def kick(ctx, member: discord.Member, reason: str):
    await member.kick(reason=reason)
    await ctx.send(F"{member.display_name} has been kicked")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Couldn't do that Make sure i have permissions for it")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("User or Reason argument is missing")


@client.command(pass_context=True)
@is_Owner_or_admin()
async def ban(ctx, member: discord.User):
    if member.guild_permissions.administrator:
        await ctx.send("The mentioned user is an admin")
        return
    else:
        await ctx.guild.ban(member)
        await ctx.send(F"{member.display_name} has been banned")


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Couldn't do that Make sure i have permissions for it")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Couldn't do that Make sure i have permissions for it")


@client.command(pass_context=True)
@is_Owner_or_admin()
async def unban(ctx, id: int):
    user = await client.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(F"{user.display_name} has been unbanned")


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Couldn't do that Make sure i have permissions for it")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Couldn't do that Make sure i have permissions for it")


@client.command(pass_context=True)
async def user(ctx, member: discord.Member):
    embed = discord.Embed()
    embed.set_author(name=member.display_name)
    embed.add_field(name="Joined at", value=member.joined_at.strftime("%b %d, %Y"), inline=True)
    embed.add_field(name="Created account", value=member.created_at.strftime("%b %d, %Y"), inline=True)
    embed.set_image(url=member.avatar_url)
    await  ctx.send(embed=embed)


@client.command(pass_context=True)
async def serverinfo(ctx):
    server = ctx.guild
    embed = discord.Embed(title=server.name)
    embed.add_field(name="Created:", value=server.created_at.strftime("%b %d, %Y"), inline=True)
    embed.add_field(name="Owner", value=server.owner, inline=True)
    embed.add_field(name="Member count", value=server.member_count, inline=True)
    embed.add_field(name="Channels", value=len(server.channels), inline=True)
    embed.add_field(name="Categories", value=len(server.categories), inline=True)
    embed.set_thumbnail(url=server.icon_url)
    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def make_embed(ctx):
    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    await ctx.send('Waiting for a title')
    title = await client.wait_for('message', check=check)

    await ctx.send('Waiting for a description')
    desc = await client.wait_for('message', check=check)

    embed = discord.Embed(title=title.content, description=desc.content, color=0x72d345)
    await ctx.send(embed=embed)


@client.command()  # fix
async def clearmine(ctx, amount: int):
    amount += 1
    temp = amount
    count = 0
    while True:
        count = 0
        async for message in ctx.channel.history(limit=temp):
            if message.author == ctx.author:
                count += 1
            if count == amount:
                break
        if count != amount:
            temp += 5
        else:
            await ctx.channel.purge(limit=temp, check=lambda message: message.author == ctx.author)
            break
        await asyncio.sleep(1)


@client.command()
@is_Owner_or_admin()
async def clear(ctx, amount: int):
    amount += 1
    authors = []
    authorcounter = []
    async for message in ctx.channel.history(limit=amount):
        if message.author.name in authors:
            index = authors.index(message.author.name)
            authorcounter[index] += 1
        else:
            authors.append(message.author.name)
            authorcounter.append(1)
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title=" ")
    for i in range(len(authors)):
        embed.add_field(name=authors[i], value=authorcounter[i], inline=False)
    timer = time.time() + 5
    msg = await ctx.send(embed=embed)
    while True:
        if time.time() > timer:
            await msg.delete()
            break
        await asyncio.sleep(1)


@client.command()
async def afk(ctx, *, reason: str):
    user = ctx.message.author
    memberlist.append(user)
    reasonlist.append(reason)
    await ctx.send(f"Set reason:{reason}")


@afk.error
async def afk_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a reason argument")


@client.command()
async def avatar(ctx, user: discord.Member):
    embed = discord.Embed(description="AVATAR")
    embed.set_author(name=user.display_name, url=user.avatar_url, icon_url=user.avatar_url)
    embed.set_image(url=user.avatar_url)
    await ctx.send(embed=embed)


@client.command()
async def color(ctx, *, color: str):  # doesnt need slash for now
    embed = discord.Embed(title=color)
    embed.add_field(name="HEX", value=colors.to_hex(color), inline=True)
    await ctx.channel.send(embed=embed)


@client.command()
@is_Owner_or_admin()
async def softban(ctx, user: discord.User):
    await ctx.guild.ban(user)
    await ctx.guild.unban(user)
    await ctx.send(f"SoftBanned the {user.display_name}")


@softban.error
async def softban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Missing permissions")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Something went wrong")
    else:
        raise error


@client.command()
async def members(ctx, role: discord.Role):
    embed = discord.Embed(title=f"ALL USERS WITH {role.name} ROLE")
    guild = ctx.guild
    for member in guild.members:
        if role in member.roles:
            embed.add_field(name=member.display_name, value="✔️", inline=True)
    await ctx.send(embed=embed)


@members.error
async def member_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send("You either mentioned a user or the role doesn't exist")
    else:
        raise error


@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@client.command()
async def leave(ctx):
    for x in client.voice_clients:
        if ctx.author:
            await x.disconnect(force=True)
            x.cleanup()


OnlyMeUsers = []
OnlyMeChannels = []
Accepted = []
AcceptedChannel = []
servers = []


def firstUser(channel: discord.VoiceChannel):
    global OnlyMeChannels, OnlyMeUsers
    index = OnlyMeChannels.index(channel)
    return OnlyMeUsers[index]


def ifmoved(guild: discord.Guild):  # if user is moved
    global OnlyMeChannels, OnlyMeUsers, Accepted, AcceptedChannel
    all = guild.voice_channels
    blacklisted = []
    whitelisted = []
    for x in all:
        for member in OnlyMeUsers:
            if member in x.members:
                blacklisted.append(x.name)
    for channel in all:
        if channel.name not in blacklisted:
            whitelisted.append(channel)

    for only in OnlyMeChannels:
        if only in whitelisted:
            index = OnlyMeChannels.index(only)
            moveduser = OnlyMeUsers[index]
            if moveduser.voice:
                OnlyMeChannels.remove(OnlyMeChannels[index])
                OnlyMeUsers.remove(moveduser)
            elif moveduser.voice is None:
                OnlyMeChannels.remove(OnlyMeChannels[index])
                OnlyMeUsers.remove(moveduser)


def registered(user: discord.Member):
    global OnlyMeUsers
    if user in OnlyMeUsers:
        return True
    else:
        return False


@client.command()
async def accepted(ctx):
    global Accepted
    await ctx.send(Accepted)


@client.command()
async def onlyme(ctx):
    me = ctx.author
    global OnlyMeUsers, OnlyMeChannels, Accepted, AcceptedChannel, servers
    voice_state = ctx.author.voice
    if registered(me) is False:  # if user is already registered works
        if voice_state is not None:
            if len(me.voice.channel.members) <= 1:
                OnlyMeUsers.append(me)
                OnlyMeChannels.append(me.voice.channel)
                servers.append(ctx.guild)
                await ctx.send(f"Added {me.mention} to OnlyUser priority")
            else:
                await ctx.send(
                    "Users are already in that vc either find an empty one or request joining someone with a similar tag")
        else:
            await ctx.send("Join vc first")
    else:
        await ctx.send("You are already OnlyMe tagged")
    while True:
        for x in servers:
            ifmoved(x)
            for omc in OnlyMeChannels:
                for member in omc.members:
                    if not member.bot:
                        if member in Accepted:
                            mainuser = firstUser(member.voice.channel)
                            index = Accepted.index(member)
                            if mainuser.voice.channel is not AcceptedChannel[index]:
                                await member.move_to(None)
                        elif member in OnlyMeUsers and member is not firstUser(
                                member.voice.channel):
                            await member.move_to(None)
                            ind = OnlyMeUsers.index(member)
                            OnlyMeUsers.remove(member)
                            OnlyMeChannels.remove(OnlyMeChannels[ind])
                        elif member not in OnlyMeUsers:
                            await member.move_to(None)
        await asyncio.sleep(1)

        if not OnlyMeUsers:
            break


@client.command()
async def requestjoin(ctx, user: discord.Member):
    if ctx.author not in Accepted and ctx.author is not firstUser(user.voice.channel):
        voice_channel = user.voice.channel
        mainuser = firstUser(channel=voice_channel)
        msg = await ctx.send(f"{user.mention} Do you want to let {ctx.author.mention} in your OnlyMe session?")
        await msg.add_reaction('✅')
        await msg.add_reaction('❎')

        def check(reaction, member):
            return member == mainuser and str(reaction.emoji) == '❎' or str(reaction.emoji) == '✅'

        while True:
            try:
                voice_channel = user.voice.channel
                mainuser = firstUser(channel=voice_channel)
                reaction, member = await client.wait_for('reaction_add', timeout=5, check=check)
                if str(reaction) == '✅' and member == mainuser:
                    Accepted.append(ctx.author)
                    AcceptedChannel.append(user.voice.channel)
                    await ctx.send("Granted! you can now go in")
                    break
                elif str(reaction == '❎') and member == mainuser:
                    await ctx.send("User declined")
                    break
            except asyncio.TimeoutError:
                await ctx.send("Time ran out")
                break
        await asyncio.sleep(1)
    elif ctx.author in Accepted:
        await ctx.send("You are already Accepted by someone")
    elif ctx.author is firstUser(user.voice.channel):
        await ctx.send("You cant request yourself")


@requestjoin.error
async def _requestjoinerror(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Who?")


@client.command()
async def removeuser(ctx, user: discord.Member):
    global OnlyMeChannels, OnlyMeUsers, Accepted, AcceptedChannel
    if ctx.author is firstUser(ctx.author.voice.channel):
        if user in Accepted:
            index = Accepted.index(user)
            Accepted.remove(user)
            AcceptedChannel.remove(AcceptedChannel[index])
            await ctx.send(f"Removed {user.mention} from Granted Access")
            if user in OnlyMeUsers:
                ind = OnlyMeUsers.index(user)
                OnlyMeUsers.remove(user)
                OnlyMeChannels.remove(OnlyMeChannels[ind])
        elif user not in Accepted:
            await ctx.send("They are not accepted")
        else:
            await ctx.send("You are not the first author for OnlyMe in that channel")


@client.command()
async def availablevc(ctx):
    global OnlyMeUsers
    embed = discord.Embed(title="All available vc")
    all = ctx.guild.voice_channels
    blacklisted = []
    global OnlyMeUsers
    for x in all:
        for member in OnlyMeUsers:
            if member in x.members:
                blacklisted.append(x.name)
    for channel in all:
        if channel.name not in blacklisted:
            embed.add_field(name=channel.name, value='\u200b', inline=False)
    await ctx.send(embed=embed)


@client.command()
async def onlymeoff(ctx):
    global OnlyMeUsers
    if ctx.author in OnlyMeUsers:
        OnlyMeUsers.remove(ctx.author)
        await ctx.send(f"Removed {ctx.author.display_name} from OnlyUser priority")
    elif ctx.author not in OnlyMeUsers:
        await ctx.send("You are already tagged off")


# end of only me ------------------------------------------------------------


@client.command()
async def unusedroles(ctx):
    embed = discord.Embed(title="UNUSED ROLES")
    guild = ctx.guild
    role_names = []
    rolecheck = []
    for member in guild.members:
        for role in member.roles:
            role_names.append(role.name)
    for role in guild.roles:
        if role.name not in role_names:
            rolecheck = role
            embed.add_field(name=role, value='\u200b', inline=False)
    if rolecheck:
        await ctx.send(embed=embed)
    else:
        await ctx.send("Every role is currently used")


@client.command()
@is_Owner_or_admin()
async def removeallroles(ctx, user: discord.Member):
    for role in user.roles:
        if role.name != '@everyone':
            await user.remove_roles(role)
    await ctx.send(f"Removed all Roles From {user.display_name}")


@removeallroles.error
async def removellaroles_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Removed all possible roles but missed permissions for some")
    else:
        raise error


@client.command()
@is_Owner_or_admin()
async def removeallunused(ctx):
    guild = ctx.guild
    role_names = []
    for member in guild.members:
        for role in member.roles:
            role_names.append(role.name)
    for role in guild.roles:
        if role.name not in role_names:
            if role.name != '@everyone' and role.id != 810048628335968288:
                await  role.delete()
    await ctx.send(f"Removed all unused roles")


@removeallunused.error
async def removellunused_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Removed all possible roles but missed permissions for some")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("Removed all possible roles but missed permissions for some")
    else:
        raise error


@client.command()
async def img(ctx, *, word: str):
    await ctx.send("Scrolling...")
    embed = discord.Embed(title=f"(BETA refactor) Showing results with keyword {word}")
    imagelist = []
    url = f"https://www.pinterest.com/search/pins/?q={word}&rs=typed&term_meta[]={word}%7Ctyped.html"
    scrollnumber = 3
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome()
    driver.get(url)
    for _ in range(1, scrollnumber):
        driver.execute_script("window.scrollTo(1,100000)")
        time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for link in soup.find_all('img'):
        imagelist.append(link.get('src'))

    index = 0
    embed.set_image(url=imagelist[index])
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('⬅️')
    await msg.add_reaction('➡️')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '⬅️' or str(reaction.emoji) == '➡️'

    while True:
        try:
            reaction, user = await client.wait_for('reaction_add', check=check, timeout=30)
            if str(reaction) == '⬅️' and user == ctx.author:
                if index - 1 >= 0:
                    index -= 1
                    embed.set_image(url=imagelist[index])
                    await msg.edit(embed=embed)
                else:
                    await ctx.send("You cant go further back")
            elif str(reaction) == '➡️' and user == ctx.author:
                if index + 1 <= len(imagelist):
                    index += 1
                    embed.set_image(url=imagelist[index])
                    await msg.edit(embed=embed)
        except asyncio.TimeoutError:
            break
        await asyncio.sleep(1)


client.run("ODEwMDQ4NjI4MzM1OTY4Mjg4.YCd-kg.fu2q4SxiSe0Td00FuUqBk_E98C4")

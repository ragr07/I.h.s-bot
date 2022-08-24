import asyncio
import random

import discord
from discord import Member, Guild

client = discord.Client()


@client.event
async def on_ready():
    print('Ich bin der neue Bot auf dem Server mit dem Namen {}'.format(client.user.name))
    client.loop.create_task(status_task())


async def status_task():
    colors = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold(), discord.Colour.green(),
              discord.Colour.blue, discord.Colour.purple]
    while True:
        await client.change_presence(activity=discord.Game('?help'), status=discord.Status.online)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game('In his steps'), status=discord.Status.online)
        await asyncio.sleep(5)
        guild: Guild = client.get_guild(945658700163588108)
        if guild:
            role = guild.get_role(946344547905073152)
            if role:
                if role.position < guild.get_member(client.user.id).top_role.position:
                    await role.edit(colour=random.choice(colors))


def is_not_pinned(mess):
    return not mess.pinned


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if '?help' in message.content:
        await message.channel.send('**Hilfe zum Bot**\r\n'
                                   '?help - Zeigt diese Hilfe an')
    if message.content.startswith('?userinfo'):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title='Userinfo für {}'.format(member.name),
                                      description='Dies ist eine Information für den User {}'.format(member.mention),
                                      colour=0x22a7f0)
                embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                rollen = ''
                for role in member.roles:
                    if not role.is_default():
                        rollen += '{} \r\n'.format(role.mention)
                if rollen:
                    embed.add_field(name='Rollen', value=rollen, inline=True)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text='Ich bin ein Embedfooter.')
                mess = await message.channel.send(embed=embed)
                await mess.add_reaction(':grinning:')
                await mess.add_reaction('a:ablobhammer:586031065219596302')

    if message.content.startswith('?pin'):
        args = message.content.split(' ')
        if len(args) == 2:
            mess = await message.channel.fetch_message(args[1])
            if is_not_pinned(mess):
                await mess.pin()
                await message.channel.send('{} wurde gepinnt.'.format(mess.content))
            else:
                await message.channel.send('{} ist bereits gepinnt.'.format(mess.content))

    if message.content.startswith('?unpin'):
        args = message.content.split(' ')
        if len(args) == 2:
            mess = await message.channel.fetch_message(args[1])
            if mess.pinned:
                await mess.unpin()
                await message.channel.send('{} wurde entpinnt.'.format(mess.content))
            else:
                await message.channel.send('{} ist nicht gepinnt.'.format(mess.content))

    if message.content.startswith('?pinlist'):
        args = message.content.split(' ')
        if len(args) == 2:
            channel = message.guild.get_channel(args[1])
            if channel:
                await message.channel.send('**Pinliste**\r\n'
                                           '{}'.format('\r\n'.join([mess.content for mess in channel.pins])))

                                           
@client.event
async def on_message(message):
    if message.author.bot:
        return
    if '?hello' in message.content:
        await message.channel.send('**Guten Tag, ich bin der neue Bot auf dem Server!**')


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if '?bye' in message.content:
        await message.channel.send('Auf Wiedersehen, ich wünsche dir noch einen schönen Tag!')

    if message.content.startswith('?clear'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    await message.channel.send('{} Nachrichten gelöscht.'.format(len(deleted)-1))


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if '?Ping' in message.content:
        await message.channel.send('Pong!')


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if '?kick' in message.content:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.kick()
                await message.channel.send('{} wurde gekickt.'.format(member.mention))


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if '?ban' in message.content:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.ban()
                await message.channel.send('{} wurde gebannt.'.format(member.mention))


@client.event
async def on_message(message):
    if message.author.bot:
        return
    if '?unban' in message.content:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await message.guild.unban(member)
                await message.channel.send('{} wurde entbannt.'.format(member.mention))



client.run('')

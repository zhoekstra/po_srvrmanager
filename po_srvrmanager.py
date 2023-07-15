import os
from typing import List

import discord
from po_util import reply, role_emoji, get_roles, po_roles

client = discord.Client(
    intents=discord.Intents.all(),
    chunk_guilds_at_startup=True
)


async def handle_clear_attendees(message: discord.Message):
    guild: discord.Guild = message.guild
    sroles = await get_roles(guild)
    if sroles[po_roles.ORGANIZER_ROLE_ID] in message.author.roles:
        async for attendee in guild.fetch_members(limit=None):
            if sroles[po_roles.ATTENDEE_ROLE_ID] in attendee.roles \
                    or sroles[po_roles.PLAYTESTER_ROLE_ID] in attendee.roles \
                    or sroles[po_roles.DESIGNER_ROLE_ID] in attendee.roles \
                    or sroles[po_roles.PRESS_ROLE_ID] in attendee.roles \
                    or sroles[po_roles.PUBLISHER_ROLE_ID] in attendee.roles:
                pronoun_end_index = attendee.nick.index(")") + 1
                new_name = role_emoji[po_roles.ALUMNI_ROLE_ID] + attendee.nick[1:pronoun_end_index]
                print("Moving " + attendee.nick + " to " + new_name)
                await reply(message, "Moving " + attendee.nick + "from Attendee to Alumni")
                await attendee.remove_roles(
                    sroles[po_roles.ATTENDEE_ROLE_ID],
                    sroles[po_roles.PLAYTESTER_ROLE_ID],
                    sroles[po_roles.DESIGNER_ROLE_ID],
                    sroles[po_roles.PRESS_ROLE_ID],
                    sroles[po_roles.PUBLISHER_ROLE_ID],
                    sroles[po_roles.FIRST_PO_ROLE_ID],
                    sroles[po_roles.TEAM_PLAYER_ROLE_ID],
                    sroles[po_roles.TEAM_HEARTS_ROLE_ID],
                    sroles[po_roles.TEAM_CLUBS_ROLE_ID],
                    sroles[po_roles.TEAM_SPADES_ROLE_ID],
                    sroles[po_roles.TEAM_DIAMONDS_ROLE_ID],
                    sroles[po_roles.MODERATOR_BUDDY_ROLE_ID],
                    sroles[po_roles.TASK_1_ROLE_ID],
                    sroles[po_roles.TASK_2_ROLE_ID],
                    sroles[po_roles.TASK_3_ROLE_ID],
                    sroles[po_roles.TASK_4_ROLE_ID],
                    sroles[po_roles.TASK_5_ROLE_ID],
                    sroles[po_roles.TASK_6_ROLE_ID],
                    sroles[po_roles.CONTRATULATIONS_ROLE_ID],
                    reason="RegistrationBot")
                if sroles[po_roles.ORGANIZER_ROLE_ID] not in attendee.roles:
                    await attendee.edit(nick=new_name)
                await attendee.add_roles(sroles[po_roles.ALUMNI_ROLE_ID], reason="RegistrationBot")

        await message.add_reaction('✔️')
    else:
        await reply(message, "Command author is not an organizer")


async def handle_open_halls(message: discord.Message):
    guild: discord.Guild = message.guild
    sroles = await get_roles(guild)
    attendee_role = sroles[po_roles.ATTENDEE_ROLE_ID]
    halls: List[discord.CategoryChannel] = [c for c in guild.categories if c.name.endswith(' Hall')]
    for hall in halls:
        await reply(message, f"Opening Hall {hall.name}")
        await hall.set_permissions(attendee_role, view_channel=True, connect=True)
        for channel in hall.channels:
            await channel.set_permissions(attendee_role, view_channel=True)


async def handle_close_halls(message: discord.Message):
    guild: discord.Guild = message.guild
    sroles = await get_roles(guild)
    attendee_role = sroles[po_roles.ATTENDEE_ROLE_ID]
    halls: List[discord.CategoryChannel] = [c for c in guild.categories if c.name.endswith(' Hall')]
    for hall in halls:
        await reply(message, f"Closing Hall {hall.name}")
        await hall.set_permissions(attendee_role, view_channel=False)
        for channel in hall.channels:
            await channel.set_permissions(attendee_role, view_channel=False)


@client.event
async def on_ready():
    print("Server Manager Connected")


@client.event
async def on_message(message: discord.Message):
    try:
        print(f"Received '{message.content}'")
        if message.author == client.user:
            return
        elif message.content == "!srvrmanager clearattendees":
            await handle_clear_attendees(message)
        elif message.content == "!srvrmanager openhalls":
            await handle_open_halls(message)
        elif message.content == "!srvrmanager closehalls":
            await handle_close_halls(message)
    except Exception as e:
        await message.add_reaction('❌')
        raise e


client.run(os.environ.get('PROTOSPIEL_ONLINE_BOT_DISCORD_TOKEN'))

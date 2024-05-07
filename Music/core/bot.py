from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand

import config

from ..logging import LOGGER


class Laky(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Bot Starting..")
        super().__init__(
            name="Bot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=5,
        )

    async def start(self):
        await super().start()       
        me = await self.get_me()
        mention = me.mention
        botname = me.first_name
        botid = me.id
        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{mention} Started",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        if config.SET_CMDS == str(True):
            try:
                await self.set_bot_commands(
                    [
                        BotCommand("ping", "Check that bot is alive or dead"),
                        BotCommand("play", "Starts playing the requested song"),
                        BotCommand("skip", "Moves to the next track in queue"),
                        BotCommand("pause", "Pause the current playing song"),
                        BotCommand("resume", "Resume the paused song"),
                        BotCommand("end", "Clear the queue and leave voice chat"),
                        BotCommand("shuffle", "Randomly shuffles the queued playlist."),
                        BotCommand("playmode", "Allows you to change the default playmode for your chat"),
                        BotCommand("settings", "Open the settings of the music bot for your chat."), 
                        BotCommand("restart", "use this command in chat to restart your musicbot for chat."), 
                        BotCommand("calldev", "use this command to call bot developer for help"), 
                        ]
                    )
            except:
                pass
        else:
            pass
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            exit()

        a = await self.get_chat_member(config.TG_LOGGER, botid)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote your bot as an admin in your log group/channel."
            )
            exit()
        LOGGER(__name__).info(f"Music Bot Started as {botname}")

    async def stop(self):
        await super().stop()

import typing as t
import logging
import urllib.parse
import asyncio
from datetime import datetime, UTC
from threading import Thread

import twitchio.ext.commands
import twitchio.message

from cph.vote.model import VoteOption
from cph.vote.client import VoteClient, VoteEntry
from cph.resources.secrets import Secrets


class TwitchBot(twitchio.ext.commands.Bot):
    def __init__(self, channel: str, secrets: Secrets, logger: logging.Logger):
        super().__init__(token=secrets.TWITCH_ACCESS_TOKEN,
                         prefix='!',
                         initial_channels=[channel],
                         case_insensitive=True)
        self._channel = channel
        self._logger = logger
        self._entries: list[VoteEntry] = []

    async def event_ready(self):
        self._logger.debug(f'Logged in as | {self.nick}')
        self._logger.debug(f'User id is | {self.user_id}')

    async def event_message(self, message: twitchio.message.Message) -> None:
        if message.echo:
            return

        ts = datetime.fromtimestamp(int(message._timestamp) / 1000, tz=UTC)
        uid = message.author.name or ''
        msg = message.content or ''
        self._entries.append(VoteEntry(ts=ts, uid=uid, msg=msg))

    async def start_vote(self, vote_options: list[VoteOption], max_count: int):
        channel = self.get_channel(self._channel)
        if channel is None:
            self._logger.warning('Channel not found')
            return
        options = ', '.join(f'{v.alias}: {v.option}' for v in vote_options)
        await channel.send(f'Vote started for {max_count} option(s): {options}!')

    async def stop_vote(self, winners: list[VoteOption]):
        channel = self.get_channel(self._channel)
        if channel is None:
            self._logger.warning('Channel not found')
            return
        if len(winners) == 1:
            winner_name = winners[0].option
            await channel.send(f'Winner is {winner_name}!')
        else:
            winner_names = ', '.join([w.option for w in winners])
            await channel.send(f'Winners are {winner_names}!')

    async def fetch_entries(self) -> list[VoteEntry]:
        entries = self._entries
        self._entries = []
        return entries


class TwitchVoteClient(VoteClient):
    def __init__(self, channel: str, secrets: Secrets, logger: logging.Logger):
        self._bot = TwitchBot(channel, secrets, logger)
        self._logger = logger

        self._loop = self._bot.loop
        self._bot_thread = Thread(target=self._run_bot)

    def _run_bot(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def connect(self, url: urllib.parse.ParseResult) -> bool:
        try:
            task = self._loop.create_task(self._bot.connect())
            self._loop.run_until_complete(task)
        except twitchio.TwitchIOException:
            return False
        self._bot_thread.start()
        return True

    def disconnect(self):
        asyncio.run_coroutine_threadsafe(self._bot.close(), self._loop) \
            .result(timeout=None)  # block until done
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._bot_thread.join()

    def start(self, vote_options: list[VoteOption], max_count: int):
        asyncio.run_coroutine_threadsafe(
            self._bot.start_vote(vote_options, max_count),
            self._loop)

    def stop(self, winners: list[VoteOption]):
        asyncio.run_coroutine_threadsafe(
            self._bot.stop_vote(winners),
            self._loop)

    def fetch(self) -> t.Iterable[VoteEntry]:
        future = asyncio.run_coroutine_threadsafe(
            self._bot.fetch_entries(),
            self._loop)
        entries = future.result(timeout=None)
        return entries

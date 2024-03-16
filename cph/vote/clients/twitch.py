import typing as t
import logging
import urllib.parse
import asyncio
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
        self._logger = logger

    async def event_ready(self):
        self._logger.info(f'Logged in as | {self.nick}')
        self._logger.info(f'User id is | {self.user_id}')

    async def event_message(self, message: twitchio.message.Message) -> None:
        self._logger.info(f'[{message.author.name}]: {message.content}')
        await super().event_message(message)

    @twitchio.ext.commands.command()
    async def vote(self, ctx: twitchio.ext.commands.Context):
        self._logger.info(f'vote: {ctx.message.content}')
        await ctx.send('vote')


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
        self._logger.info('VoteClient started')

    def stop(self):
        self._logger.info('VoteClient stopped')

    def fetch(self) -> t.Iterable[VoteEntry]:
        self._logger.info('VoteClient fetched')
        return []

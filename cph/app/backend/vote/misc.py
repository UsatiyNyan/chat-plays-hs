from cph.game.model import GameOption

MISC_GROUP = 'Misc'

EMOTE_OPTION_NAME = 'Emote'
EMOTE_SUBOPTIONS = (
    'Greetings', 'Well Played', 'Thanks', 'Wow', 'Oops', 'Threaten'
)

END_TURN_OPTION_NAME = 'End Turn'
END_TURN_OPTION = GameOption(
    option=END_TURN_OPTION_NAME,
    group=MISC_GROUP,
    suboptions=[]
)


def _make_emote_option(suboptions: list[GameOption]):
    return [
        GameOption(option=emote, group=MISC_GROUP, suboptions=suboptions)
        for emote in EMOTE_SUBOPTIONS
    ]


def add_emote_option(game_options: list[GameOption]):
    if len(game_options) == 0:
        return
    last_option = game_options[-1]
    if last_option.option == END_TURN_OPTION_NAME and \
            last_option.group == MISC_GROUP:
        game_options.append(GameOption(
            option=EMOTE_OPTION_NAME,
            group=MISC_GROUP,
            suboptions=_make_emote_option(game_options)
        ))


def remove_emote_option(game_options: list[GameOption]):
    if len(game_options) == 0:
        return
    last_option = game_options[-1]
    if last_option.option == EMOTE_OPTION_NAME and \
            last_option.group == MISC_GROUP:
        game_options.pop()

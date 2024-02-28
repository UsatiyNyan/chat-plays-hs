from dataclasses import dataclass


# reflects option available for vote in chat
@dataclass
class VoteOption:
    option: str  # as in options
    alias: str   # key for chat
    votes: int = 0

# vote_regex = re.compile("^!vote (\w+)$", re.IGNORECASE)
# match = vote_regex.match(chat_message)
# if match:
#     chosen_alias = match.group(1)
#     vote_option = vote_options.get(chosen_alias)

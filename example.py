from twitch_irc_parser import TwitchIRC
import json

# User ids of bots
BOTS = [
    440504421,  # hachubot
    429526376,  # irltoolkit
    19264788,   # nightbot
    100135110,  # streamelements
]

# Emotes in temotes API format
EMOTES = [
    {
        "provider": 1,
        "code": "FeelsDankMan",
        "urls": [
            {
                "size": "1x",
                "url": "https://cdn.7tv.app/emote/63071bb9464de28875c52531/1x.webp",
            },
            {
                "size": "2x",
                "url": "https://cdn.7tv.app/emote/63071bb9464de28875c52531/2x.webp",
            },
            {
                "size": "3x",
                "url": "https://cdn.7tv.app/emote/63071bb9464de28875c52531/3x.webp",
            },
            {
                "size": "4x",
                "url": "https://cdn.7tv.app/emote/63071bb9464de28875c52531/4x.webp",
            }
        ],
        "zero_width": False,
    },
    {
        "provider": 1,
        "code": "TeaTime",
        "urls": [
            {
                "size": "1x",
                "url": "https://cdn.7tv.app/emote/62e5c88ba1a665fe6efd5aa2/1x.webp",
            },
            {
                "size": "2x",
                "url": "https://cdn.7tv.app/emote/62e5c88ba1a665fe6efd5aa2/2x.webp",
            },
            {
                "size": "3x",
                "url": "https://cdn.7tv.app/emote/62e5c88ba1a665fe6efd5aa2/3x.webp",
            },
            {
                "size": "4x",
                "url": "https://cdn.7tv.app/emote/62e5c88ba1a665fe6efd5aa2/4x.webp",
            }
        ],
        "zero_width": False,
    },
]

raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['Kappa this is a test FeelsDankMan TeaTime'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': '25:0-4'}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"

message = TwitchIRC.Message(raw, emotes=EMOTES, bots=BOTS)

if message.is_parsed:
    print(json.dumps(vars(message), indent=4))

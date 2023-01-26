# twitch-irc-parser
Parser for Twitch IRC messages.

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/CrippledByte/twitch-irc-parser/python-test.yml)

- [Usage](#usage)
- [Installation](#installation)
- [Message class](#message-class)
- [Development](#development)
    - [Download repo](#download-repo)
    - [Run tests](#run-tests)

## Installation
```bash
git clone https://github.com/CrippledByte/twitch-irc-parser
cd twitch-irc-parser
```

## Usage
```python
from twitch_irc_parser import TwitchIRC

raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['Kappa this is a test FeelsDankMan TeaTime'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': '25:0-4'}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"

message = TwitchIRC.Message(raw)

if message.is_parsed:
    print('User: @' + message.user['display_name'])
    print('Channel: #' + message.channel['name'])
    print('Text: ' + message.text)
    print('Timestamp: ' + message.timestamp)
```

which outputs:
```text
User: @CrippledByte
Channel: #testchannel
Text: Kappa this is a test FeelsDankMan TeaTime
Timestamp: 2023-01-25T15:15:03.223000
```

It's possible to define emotes and bots (see [example.py](example.py)):
```python
message = TwitchIRC.Message(raw, emotes=EMOTES, bots=BOTS)
```

## Message class
Notes:
- Unavailable values are `None`.

key | type | examples | description
---|:---:|---|---
`"raw"` | string | `"type: pubmsg, source: ..."` | Input IRC message.
`"is_parsed"` | boolean | `True` | Message was parsed successfully.
`"id"` | string | `"e35baca3-0653-4502-aa6d-ed25006905ea"` | Message identifier in GUID format.
`"channel"` | dict |  [Channel dict](#channel-dict) | Contains information about the channel that the message was sent in.
`"user"` | dict |  [User dict](#user-dict) | Contains information about the user that sent the message.
`"text"` | string | 👋 hello! FeelsDankMan TeaTime | Message text including emote text.
`"timestamp"` | string | `"2023-01-25T15:15:03.223000"` | Message sent timestamp in ISO 8601 format.
`"text_color"` | string | `None`, `"#3FB5BA"` | Color of the message text (same as user color if '/me' action was used).
`"badges"` | OrderedDict | `{"vip": "1", "subscriber": "3012", "sub-gift-leader": "1"}` | Badges of user that are visible in message.
`"emotes"` | list | list of [Emotes dict](#emotes-dict) |  Emotes used in message.
`"tmi_sent_ts"` | int | `1674656103223` | Message sent Unix timestamp with milliseconds.

### Channel dict
key | type | examples | description
---|:---:|---|---
`"id"` | int | `123456789` | Channel id.
`"name"` | string | `"testchannel"` | Channel name (lowercase, room id without # prefix).

### User dict
key | type | examples | description
---|:---:|---|---
`"id"` | int | `53862903` | User id.
`"type"` | string | | Unknown.
`"name"` | string | `"crippledbyte"` | User name (lower case).
`"display_name"` | string | `"CrippledByte"` | User name with capitalization.
`"color"` | string | `"#3FB5BA"` | Color of user name.
`"subscription_time_months"` | int | `25` | Number of months the user has been subscribed to this channel.
`"is_bot"` | boolean | | User is pre-defined bot.
`"is_mod"` | boolean | | User is moderator in this channel.
`"is_vip"` | boolean | | User is vip in this channel.
`"is_partner"` | boolean | | User is Twitch partner.
`"is_broadcaster"` | boolean | | User is broadcaster in this channel.
`"is_subscribed"` | boolean | | The user is currenly subscribed to the channel.
`"is_first_message_in_channel"` | boolean | | First message in this channel by user.
`"has_twitch_turbo"` | boolean | | User has Twitch Turbo.

### Emotes dict
key | type | examples | description
---|:---:|---|---
`"id"` | int | `"25"`, `"emotesv2_9df75c0cd2204b6c9f4d079c066e6245"` | Twitch emote id (optional).
`"code"` | string | `"Kappa"`, `"popCat"` | Text of emote.
`"provider"` | int | `0`, `1`, `2`, `3` | 0=twitch, 1=7tv, 2=bttv, 3=ffz
`"range"` | list | `[0, 4]`, `[21, 32]` | `[start, end]` of emote code position in message text.
`"urls"` | list | [Url dict](#url-dict) | List of image urls and sizes.
`"zero_width"` | boolean | | Emote is a zero width emote.

#### Url dict
key | type | examples | description
---|:---:|---|---
`"id"` | int | `"1x"`, `"2x"`, `"3x"`, `"4x"`,  | Size of emote the url points to. Not all sizes are always available.
`"code"` | string | `"https://static-cdn.jtvnw.net/emoticons/v2/25/default/light/1.0"`, `"https://cdn.7tv.app/emote/63071bb9464de28875c52531/1x.webp"` | Url of emote image.

## Development
### Download repo
```bash
git clone https://github.com/CrippledByte/twitch-irc-parser
cd twitch-irc-parser
```
### Run tests
```bash
python3 -m unittest
```

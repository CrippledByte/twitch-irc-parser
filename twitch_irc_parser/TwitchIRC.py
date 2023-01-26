import re
import json
import ast
from datetime import datetime
from collections import OrderedDict

class Message:
    """A parsed IRC message."""

    def __init__(self, raw, emotes={}, bots=[]):
        """Parse an IRC message.

        Parameters
        ----------
        raw : str
          Input IRC message.
        emotes : dict
          Emote data from temotes API as dict.
        bots : list
          List of user names that are bots.
        """

        self.raw = raw.strip()                      # input IRC message ('type: pubmsg, source...')
        self.is_parsed = False                      # message was parsed successfully

        self.id = None                              # message id (GUID)

        self.channel = {                            # twitch channel where the message was sent in
            'id': None,                             # room id
            'name': None,                           # channel name (lowercase)
        }

        self.user = {                               # user who sent the message
            'id': None,                             # user id
            'type': None,                           # unknown
            'name': None,                           # user name (lowercase)
            'display_name': None,                   # user name with capitalization as specified by user
            'color': None,                          # color of user name in chat
            'subscription_time_months': 0,          # Number of months the user has been subscribed to this channel.
            'is_bot': None,                         # user is pre-defined bot
            'is_mod': None,                         # user is moderator in this channel

            'is_vip': None,                         # user is vip in this channel
            'is_partner': None,                     # user is twitch partner
            'is_broadcaster': None,                 # user is broadcaster in this channel

            'is_subscribed': None,                  # user has a subscription to this channel 
            'is_first_message_in_channel': None,    # first message in this channel by user
            'has_twitch_turbo': None,               # user has Twitch Turbo
        }

        self.text = None                            # message text
        self.timestamp = None                       # timestamp of message in ISO 8601 format ('2023-01-20T17:34:48.571000')
        self.text_color = None                      # color of text in message (when user starts message with '/me ' the text color will be the same as the user name color)

        self.badges = OrderedDict()                 # badges of user that are visible in message
        self.emotes = list()                        # emotes used in message

        def str_to_bool(s):
            if s == '1':
                return True
            return s == 'True'

        match = re.match(r'type: (.*), source: (?:(.*)\!.*), target: (.*), arguments: (?:\[[\'\"](.*)[\'\"]\]), tags: (\[.*\])', self.raw) # https://regex101.com/r/WjRH49/1

        if not match:
            return

        if match.group(1) not in ['pubmsg', 'action']: # assuming that the action is /me
            return

        # Get message info
        info = dict()
        for pair in ast.literal_eval(match.group(5)):
            key = re.sub(r'\-', '_', pair['key']) # convert dashes in keys to underscores
            info[key] = pair['value']

        # message
        self.id = info['id']

        self.tmi_sent_ts = int(info['tmi_sent_ts'])
        dt = datetime.fromtimestamp(self.tmi_sent_ts / 1000)
        self.timestamp = dt.isoformat()

        # Get message text
        text = match.group(4)
        text = re.sub(r'\\U000e0000', '', text) # remove invisible character
        text = text.strip() # remove whitespace at start and end
        self.text = text

        if match.group(1) == 'action':
            # assuming that the action is /me
            self.text_color = info['color']

        # channel
        self.channel['id'] = int(info['room_id'])
        self.channel['name'] = match.group(3).replace('#', '').lower()

        # user
        self.user['id'] = int(info['user_id'])
        self.user['name'] = match.group(2).lower()
        self.user['display_name'] = info['display_name']
        self.user['type'] = info['user_type']
        self.user['color'] = info['color']
        self.user['is_bot'] = self.user['name'] in bots # assuming bot names are lowercase
        self.user['is_mod'] = str_to_bool(info['mod'])
        self.user['is_subscribed'] = str_to_bool(info['subscriber'])
        self.user['is_first_message_in_channel'] = str_to_bool(info['first_msg'])
        self.user['has_twitch_turbo'] = str_to_bool(info['turbo'])

        # TODO parse 'flags'

        # Parse badges
        if info['badges'] is not None:
            for badge_str in info['badges'].split(','):
                badge_split = badge_str.split('/')
                # [0]: subscriber, moderator, vip, bits, sub-gift-leader, glitchcon2020, partner
                # [1]: 12, 1, 1, 100, 2, 1, 1, pink-2
                self.badges[badge_split[0]] = badge_split[1]

        # Get additional information from 'badge-info' key
        badge_infos = dict()
        if info['badge_info'] is not None:
            for badge_info_str in info['badge_info'].split(','):
                badge_info_split = badge_info_str.split('/')
                # [0]: subscriber, sub-gift-leader, glitchcon2020
                # [1]: 23, 2, 1, No
                badge_infos[badge_info_split[0]] = badge_info_split[1]

        # Get subscription time
        if 'subscriber' in badge_infos.keys():
            self.user['subscription_time_months'] = int(badge_infos['subscriber'])

        # user is broadcaster if channel and user name are the same, or if user has broadcaster badge
        self.user['is_broadcaster'] = False
        if self.user['name'] == self.channel['name'] or 'broadcaster' in self.badges.keys():
            self.user['is_broadcaster'] = True

        # user is partner if partner badge is present
        self.user['is_partner'] = False
        if 'partner' in self.badges.keys():
            self.user['is_partner'] = True

        # user is vip if vip badge is present
        self.user['is_vip'] = False
        if 'vip' in self.badges.keys():
            self.user['is_vip'] = True

        # Find Twitch emotes in comment
        message_emotes = list()
        if info['emotes'] is not None:
            if info['emotes'].count(':') >= 1:
                # get individual emotes
                for value in info['emotes'].split('/'):
                    # split to get id and ranges (emotesv2_9df75c0cd2204b6c9f4d079c066e6245:0-8,15-23)
                    id_and_ranges = value.split(':')
                    emote_id = id_and_ranges[0]
                    ranges = id_and_ranges[1]

                    # split ranges to iterate through ranges (0-8,15-23)
                    for range_ in ranges.split(','):
                        # Get range
                        range_split = range_.split('-')
                        start = int(range_split[0])
                        end = int(range_split[1])

                        emote_code = self.text[start:(end + 1)]
                        
                        emote = {
                            'id': emote_id,
                            'code': emote_code,
                            'provider': 0,
                            'range': [start, end],
                            'urls': [
                                {
                                    'size': '1x',
                                    'url': 'https://static-cdn.jtvnw.net/emoticons/v2/{}/default/light/1.0'.format(emote_id),
                                },
                                {
                                    'size': '2x',
                                    'url': 'https://static-cdn.jtvnw.net/emoticons/v2/{}/default/light/2.0'.format(emote_id),
                                },
                                {
                                    'size': '4x',
                                    'url': 'https://static-cdn.jtvnw.net/emoticons/v2/{}/default/light/3.0'.format(emote_id),
                                },
                            ],
                            'zero_width': False,
                        }

                        message_emotes.append(emote)

        # Find emotes from third party providers
        if len(emotes.keys()) > 0: # skip if third party emote data is not passed
            words = self.text.split(' ')
            temp = message_emotes[:] # create clone of Twitch emotes list, used to prevent only adding 1 same other emote per comment
            temptext = self.text # copy text, used to get range and remove emotes afterwards
            remove_character_count = 0
            for word in words:
                if word in emotes and not any(e['code'] == word for e in temp):
                    # Get range of emote
                    start = temptext.find(word)
                    end = start + len(word)

                    emote = emotes[word]
                    emote['code'] = word # overwrite code
                    emote['range'] = [
                        start + remove_character_count,
                        end + remove_character_count - 1
                    ]

                    if 'zero_width' not in emote.keys():
                        emote['zero_width'] = False

                    # Remove emote from temptext
                    temptext = temptext[:start] + temptext[(end):]
                    remove_character_count += (end - start)

                    message_emotes.append(emote)

        self.emotes = message_emotes

        self.is_parsed = True

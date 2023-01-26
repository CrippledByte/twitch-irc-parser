import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from twitch_irc_parser import TwitchIRC

EMOTES = {
    "TeaTime": {
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
    "SteerR": {
      "provider": 1,
      "code": "SteerR",
      "urls": [
          {
              "size": "1x",
              "url": "https://cdn.7tv.app/emote/612fc78b9a14cebbb339b113/1x.webp"
          },
          {
              "size": "2x",
              "url": "https://cdn.7tv.app/emote/612fc78b9a14cebbb339b113/2x.webp"
          },
          {
              "size": "3x",
              "url": "https://cdn.7tv.app/emote/612fc78b9a14cebbb339b113/3x.webp"
          },
          {
              "size": "4x",
              "url": "https://cdn.7tv.app/emote/612fc78b9a14cebbb339b113/4x.webp"
          }
      ],
      "zero_width": True,
    },
}

class TestEmotes(unittest.TestCase):
    def test_emote_passthrough(self):
        # test if input emote data is passed through correctly
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['Kappa TeaTime'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': '25:0-4'}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        expected_kappa_emote = {
            'id': '25',
            'code': 'Kappa',
            'provider': 0,
            'range': [0, 4],
            'urls': [
                {
                    'size': '1x',
                    'url': 'https://static-cdn.jtvnw.net/emoticons/v2/25/default/light/1.0',
                },
                {
                    'size': '2x',
                    'url': 'https://static-cdn.jtvnw.net/emoticons/v2/25/default/light/2.0',
                },
                {
                    'size': '4x',
                    'url': 'https://static-cdn.jtvnw.net/emoticons/v2/25/default/light/3.0',
                },
            ],
            'zero_width': False,
        }
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(len(message.emotes), 2)
        self.assertEqual(message.emotes[0], expected_kappa_emote)
        self.assertEqual(message.emotes[1], EMOTES['TeaTime'])

        # without input emote data, use emote data provided by Twitch in IRC message
        message = TwitchIRC.Message(raw)
        self.assertEqual(len(message.emotes), 1)
        self.assertEqual(message.emotes[0], expected_kappa_emote)

    def test_twitch_emote_recognition(self):
        # Test if emotes of third party providers are selected correctly.
        # single emote
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['Kappa'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emote-only', 'value': '1'}, {'key': 'emotes', 'value': '25:0-4'}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(len(message.emotes), 1)

        message = TwitchIRC.Message(raw) # should produce same result since emote data is provided by Twitch in IRC message
        self.assertEqual(len(message.emotes), 1)

        # emote in text
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['test Kappa test'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': '25:5-9'}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(len(message.emotes), 1)

        message = TwitchIRC.Message(raw)
        self.assertEqual(len(message.emotes), 1)

        # no emotes (no space between emotes)
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['KappaKappa'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(len(message.emotes), 0)

        message = TwitchIRC.Message(raw)
        self.assertEqual(len(message.emotes), 0)

        # no emotes (symbol attached to emote)
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['Kappa_'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(len(message.emotes), 0)

        message = TwitchIRC.Message(raw)
        self.assertEqual(len(message.emotes), 0)

    def test_third_party_emote_recognition(self):
        # Test if emotes of third party providers are selected correctly.
        # single emote
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['TeaTime'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(len(message.emotes), 1)

        message = TwitchIRC.Message(raw) # third party emote not passed, should find no emotes
        self.assertEqual(len(message.emotes), 0)

        # emote in text
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['test TeaTime test'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(len(message.emotes), 1)

        message = TwitchIRC.Message(raw)
        self.assertEqual(len(message.emotes), 0)

        # no emotes (no space between emotes)
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['TeaTimeTeaTime'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(len(message.emotes), 0)

        message = TwitchIRC.Message(raw)
        self.assertEqual(len(message.emotes), 0)

        # no emotes (symbol attached to emote)
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['TeaTime_'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(len(message.emotes), 0)

        message = TwitchIRC.Message(raw)
        self.assertEqual(len(message.emotes), 0)

    def test_range(self):
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['Kappa TeaTime'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': '25:0-4'}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(message.emotes[0]['range'], [0, 4])
        self.assertEqual(message.emotes[1]['range'], [6, 12])

    def test_combined_emote_recognition(self):
        # 2 emotes (twitch + 3rd party)
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['Kappa TeaTime'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': '25:0-4'}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(len(message.emotes), 2)
        self.assertEqual(message.emotes[0]['code'], 'Kappa')
        self.assertEqual(message.emotes[1]['code'], 'TeaTime')

    def test_duplicate_emote_names(self):
        # 2 emotes (twitch + 3rd party) with same name.
        # If a subscription emote is also offered on a third party service on the same channel,
        # the Twitch version should be returned when the user has a subscription (this version will then be included in the emotes tag in the IRC message).
        # In this test, the emote TeaTime is set to be a subscription emote by using :0-6.
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['TeaTime'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': '12345:0-6'}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"

        # Check if twitch version is returned
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(message.emotes[0]['code'], 'TeaTime')
        self.assertEqual(message.emotes[0]['provider'], 0)
    
    def test_zero_width(self):
        # twitch emote, is not zero width
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['Kappa'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emote-only', 'value': '1'}, {'key': 'emotes', 'value': '25:0-4'}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.emotes[0]['zero_width'], False)

        # 7tv emote, is not zero width
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['TeaTime'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(message.emotes[0]['zero_width'], False)

        # 7tv emote, is zero width
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['SteerR'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw, emotes=EMOTES)
        self.assertEqual(message.emotes[0]['zero_width'], True)

if __name__ == '__main__':
    unittest.main()

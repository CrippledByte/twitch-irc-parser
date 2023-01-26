import os
import sys
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from twitch_irc_parser import TwitchIRC

MESSAGES = [
    "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['FeelsDankMan Clap'], tags: [{'key': 'badge-info', 'value': 'subscriber/25'}, {'key': 'badges', 'value': 'subscriber/24,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '1'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]",
]

class TestOther(unittest.TestCase):
    def test_user(self):
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.user['id'], 53862903)
        self.assertEqual(message.user['name'], 'crippledbyte')
        self.assertEqual(message.user['display_name'], 'CrippledByte')
        self.assertEqual(message.user['color'], '#3FB5BA')

    def test_subscription_time_months(self):
        # has subscribed
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.user['subscription_time_months'], 25)

        # has never subscribed
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['hello'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': None}, {'key': 'color', 'value': '#FF0000'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '1'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.user['subscription_time_months'], 0)

    def test_is_bot(self):
        # is not a bot
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.user['is_bot'], False)

        message = TwitchIRC.Message(MESSAGES[0], bots=['custombot'])
        self.assertEqual(message.user['is_bot'], False)

        # is a bot
        raw = "type: pubmsg, source: custombot!custombot@custombot.tmi.twitch.tv, target: #testchannel, arguments: ['@CrippledByte, popCat has been used 7,353 times.'], tags: [{'key': 'badge-info', 'value': 'subscriber/25'}, {'key': 'badges', 'value': 'moderator/1,subscriber/24'}, {'key': 'color', 'value': '#FF69B4'}, {'key': 'display-name', 'value': 'CustomBOT'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '1'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '1'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '1122334455'}, {'key': 'user-type', 'value': 'mod'}]"
        message = TwitchIRC.Message(raw, bots=[1122334455])
        self.assertEqual(message.user['is_bot'], True)

    def test_is_broadcaster(self):
        # is not broadcaster in channel
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.user['is_broadcaster'], False)

        # is broadcaster in channel
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #crippledbyte, arguments: ['FeelsDankMan TeaTime'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '53862903'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.user['is_broadcaster'], True)

    def test_is_mod(self):
        # is not a mod in channel
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.user['is_mod'], False)

        # is mod in channel
        raw = "type: pubmsg, source: custombot!custombot@custombot.tmi.twitch.tv, target: #testchannel, arguments: ['@CrippledByte, popCat has been used 7,353 times.'], tags: [{'key': 'badge-info', 'value': 'subscriber/25'}, {'key': 'badges', 'value': 'moderator/1,subscriber/24'}, {'key': 'color', 'value': '#FF69B4'}, {'key': 'display-name', 'value': 'CustomBOT'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '1'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '1'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '1122334455'}, {'key': 'user-type', 'value': 'mod'}]"
        message = TwitchIRC.Message(raw, bots=['custombot'])
        self.assertEqual(message.user['is_mod'], True)

    def test_is_partner(self):
        # is not partner
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.user['is_partner'], False)

        # is partner
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['test'], tags: [{'key': 'badge-info', 'value': 'subscriber/41'}, {'key': 'badges', 'value': 'broadcaster/1,subscriber/3012,partner/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '1'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.user['is_partner'], True)

    def test_is_subscribed(self):
        # is not subscribed
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['PepeLaugh'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.user['is_subscribed'], False)

        # is subscribed
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.user['is_subscribed'], True)

    def test_is_vip(self):
        # is not vip in channel
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.user['is_vip'], False)

        # is vip in channel
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['test'], tags: [{'key': 'badge-info', 'value': 'subscriber/27'}, {'key': 'badges', 'value': 'vip/1,subscriber/3012,sub-gift-leader/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '1'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.user['is_vip'], True)

    def test_is_first_message_in_channel(self):
        # is not first message in channel
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.user['is_first_message_in_channel'], False)

        # is first message in channel
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['hello'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': None}, {'key': 'color', 'value': '#FF0000'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '1'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.user['is_first_message_in_channel'], True)

    def test_has_twitch_turbo(self):
        # does not have Twitch Turbo
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.user['has_twitch_turbo'], False)

        # has Twitch Turbo
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['hello'], tags: [{'key': 'badge-info', 'value': 'subscriber/6'}, {'key': 'badges', 'value': 'subscriber/6,turbo/1'}, {'key': 'color', 'value': '#FF0000'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '1'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '1'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.user['has_twitch_turbo'], True)

if __name__ == '__main__':
    unittest.main()

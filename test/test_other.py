import os
import sys
import unittest
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from twitch_irc_parser import TwitchIRC

with open('test/test_other.txt') as file:
	MESSAGES = file.read().splitlines()

class TestOther(unittest.TestCase):
    def test_is_parsed(self):
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.is_parsed, True)

    def test_id(self):
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.id, 'e35baca3-0653-4502-aa6d-ed25006905ea')

    def test_channel(self):
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.channel['id'], 123456789)
        self.assertEqual(message.channel['name'], 'testchannel')

    def test_text(self):
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.text, 'FeelsDankMan Clap')

        message = TwitchIRC.Message(MESSAGES[1])
        self.assertEqual(message.text, '"I\'m serious" Kappa')

        # text with emoji
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['monkaLaugh 👍'], tags: [{'key': 'badge-info', 'value': 'subscriber/19'}, {'key': 'badges', 'value': 'subscriber/18,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '1'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.text, 'monkaLaugh 👍')

        # text with non-text characters
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['⠄⠄⢀⡤⠤⠤⣄⢀⣶⣛⣛⣒⣄⠄⠄⠄⠄⠄⠄⠄⠄⠄ 𝓢𝓣𝓡𝓔𝓐𝓜𝓔𝓡 ⠄⢀⡾⠛⠉⢩⣭⡾⣭⡀⠄⣰⣬⣦⡀⠄⡿⠋⡉⠻⣿⠋⣉⠙⡇ 𝓐𝓦𝓐𝓨, ⢀⣼⣛⡷⠖⣚⣩⣿⣾⣭⡭⠍⣛⠻⣿⢠⠁⣾⣿⢀⡇⢸⣿⢶⠇⠄ 𝓒𝓗𝓐𝓣 ⣾⣿⢋⣭⣭⣭⣭⣭⣥⠶⠾⣛⣹⡇⣽⢸⣄⣈⣁⣼⣧⣈⣁⣼⠄⠄ 𝓗𝓔𝓡𝓔 ⠹⣿⣜⡛⠶⠶⠶⠶⠶⠿⢟⣛⣭⡾⠋⢸⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄ 𝓣𝓞 ⠄⠈⠙⠻⠿⣿⣿⣿⣿⣿⠿⠛⠋⠄⣴⣿⣷⠄⠄⠄⠄⠄⠄⠄⠄⠄ 𝓢𝓣𝓐𝓨'], tags: [{'key': 'badge-info', 'value': 'subscriber/24'}, {'key': 'badges', 'value': 'subscriber/24,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '1'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.text, '⠄⠄⢀⡤⠤⠤⣄⢀⣶⣛⣛⣒⣄⠄⠄⠄⠄⠄⠄⠄⠄⠄ 𝓢𝓣𝓡𝓔𝓐𝓜𝓔𝓡 ⠄⢀⡾⠛⠉⢩⣭⡾⣭⡀⠄⣰⣬⣦⡀⠄⡿⠋⡉⠻⣿⠋⣉⠙⡇ 𝓐𝓦𝓐𝓨, ⢀⣼⣛⡷⠖⣚⣩⣿⣾⣭⡭⠍⣛⠻⣿⢠⠁⣾⣿⢀⡇⢸⣿⢶⠇⠄ 𝓒𝓗𝓐𝓣 ⣾⣿⢋⣭⣭⣭⣭⣭⣥⠶⠾⣛⣹⡇⣽⢸⣄⣈⣁⣼⣧⣈⣁⣼⠄⠄ 𝓗𝓔𝓡𝓔 ⠹⣿⣜⡛⠶⠶⠶⠶⠶⠿⢟⣛⣭⡾⠋⢸⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄ 𝓣𝓞 ⠄⠈⠙⠻⠿⣿⣿⣿⣿⣿⠿⠛⠋⠄⣴⣿⣷⠄⠄⠄⠄⠄⠄⠄⠄⠄ 𝓢𝓣𝓐𝓨')

        # text with whitespace characters (\U000e0000)
        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['pepeJAM \\U000e0000'], tags: [{'key': 'badge-info', 'value': 'subscriber/12'}, {'key': 'badges', 'value': 'subscriber/12'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '1'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.text, 'pepeJAM')

    def test_tmi_sent_ts(self):
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.tmi_sent_ts, 1674656103223)

    def test_timestamp(self):
        # Test in different timezones
        utc_timestamp = '2023-01-25T14:15:03.223000'

        os.environ['TZ'] = 'Europe/London'
        time.tzset()
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.timestamp, utc_timestamp)

        os.environ['TZ'] = 'Europe/Amsterdam'
        time.tzset()
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.timestamp, utc_timestamp)

        os.environ['TZ'] = 'US/Eastern'
        time.tzset()
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.timestamp, utc_timestamp)

    def test_text_color(self):
        message = TwitchIRC.Message(MESSAGES[0])
        self.assertEqual(message.text_color, None)

        raw = "type: action, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['this text has the same color as the username'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        self.assertEqual(message.text_color, '#3FB5BA')

    def test_badges(self):
        message = TwitchIRC.Message(MESSAGES[0])
        badges = {
            'subscriber': '24',
            'twitchconEU2022': '1'
        }
        self.assertEqual(message.badges, badges)

        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['Sadge'], tags: [{'key': 'badge-info', 'value': 'subscriber/15'}, {'key': 'badges', 'value': 'subscriber/12,overwatch-league-insider_2019A/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '1'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        badges = {
            'subscriber': '12',
            'overwatch-league-insider_2019A': '1',
        }
        self.assertEqual(message.badges, badges)

        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['test'], tags: [{'key': 'badge-info', 'value': 'subscriber/27'}, {'key': 'badges', 'value': 'vip/1,subscriber/3012,sub-gift-leader/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '1'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        badges = {
            'vip': '1',
            'subscriber': '3012',
            'sub-gift-leader': '1',
        }
        self.assertEqual(message.badges, badges)

        raw = "type: pubmsg, source: crippledbyte!crippledbyte@crippledbyte.tmi.twitch.tv, target: #testchannel, arguments: ['FeelsDankMan TeaTime'], tags: [{'key': 'badge-info', 'value': None}, {'key': 'badges', 'value': 'broadcaster/1,twitchconEU2022/1'}, {'key': 'color', 'value': '#3FB5BA'}, {'key': 'display-name', 'value': 'CrippledByte'}, {'key': 'emotes', 'value': None}, {'key': 'first-msg', 'value': '0'}, {'key': 'flags', 'value': None}, {'key': 'id', 'value': 'e35baca3-0653-4502-aa6d-ed25006905ea'}, {'key': 'mod', 'value': '0'}, {'key': 'returning-chatter', 'value': '0'}, {'key': 'room-id', 'value': '123456789'}, {'key': 'subscriber', 'value': '0'}, {'key': 'tmi-sent-ts', 'value': '1674656103223'}, {'key': 'turbo', 'value': '0'}, {'key': 'user-id', 'value': '53862903'}, {'key': 'user-type', 'value': None}]"
        message = TwitchIRC.Message(raw)
        badges = {
            'broadcaster': '1',
            'twitchconEU2022': '1',
        }
        self.assertEqual(message.badges, badges)
    
if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""Web-of-Science query parser unit tests."""
import typing
import unittest

from search_query.constants import Fields
from search_query.constants import QueryErrorCode
from search_query.constants import Token
from search_query.constants import TokenTypes
from search_query.parser_wos import WOSListParser
from search_query.parser_wos import WOSParser
from search_query.query import Query
from search_query.query import SearchField

# ruff: noqa: E501
# pylint: disable=too-many-lines
# flake8: noqa: E501


class TestWOSListParser(unittest.TestCase):
    def test_list_parser_case_1(self) -> None:
        query_list = '1. TS=("Peer leader*" OR "Shared leader*" OR "Distributed leader*" OR \u201cDistributive leader*\u201d OR \u201cCollaborate leader*\u201d OR "Collaborative leader*" OR "Team leader*" OR "Peer-led" OR "Athlete leader*" OR "Team captain*" OR "Peer mentor*" OR "Peer Coach")\n2. TS=("acrobatics" OR "acrobat" OR "acrobats" OR "acrobatic" OR "aikido" OR "aikidoists" OR "anetso" OR "archer" OR "archers" OR "archery" OR "airsoft" OR "angling" OR "aquatics" OR "aerobics" OR "athlete" OR "athletes" OR "athletic" OR "athletics" OR "ball game*" OR "ballooning" OR "basque pelota" OR "behcup" OR "bicycling" OR "BMX" OR "bodyboarding" OR "boule lyonnaise" OR "bridge" OR "badminton" OR "balle au tamis" OR "baseball" OR "basketball" OR "battle ball" OR "battleball" OR "biathlon" OR "billiards" OR "boating" OR "bobsledding" OR "bobsled" OR "bobsledder" OR "bobsledders" OR "bobsleigh" OR "boccia" OR "bocce" OR "buzkashi" OR "bodybuilding" OR "bodybuilder" OR "bodybuilders" OR "bowling" OR "bowler" OR "bowlers" OR "bowls" OR "boxing" OR "boxer" OR "boxers" OR "bandy" OR "breaking" OR "breakdanc*" OR "broomball" OR "budo" OR "bullfighting" OR "bullfights" OR "bullfight" OR "bullfighter" OR "bullfighters" OR "mountain biking" OR "mountain bike" OR "carom billiards" OR "camogie" OR "canoe slalom" OR "canoeing" OR "canoeist" OR "canoeists" OR "canoe" OR "climbing" OR "coasting" OR "cricket" OR "croquet" OR "crossfit" OR "curling" OR "curlers" OR "curler" OR "cyclist" OR "cyclists" OR "combat*" OR "casting" OR "cheerleading" OR "cheer" OR "cheerleader*" OR "chess" OR "charrerias" OR "cycling" OR "dancesport" OR "darts" OR "decathlon" OR "draughts" OR "dancing" OR "dance" OR "dancers" OR "dancer" OR "diving" OR "dodgeball" OR "e-sport" OR "dressage" OR "endurance" OR "equestrian" OR "eventing" OR "eskrima" OR "escrima" OR "fencer" OR "fencing" OR "fencers" OR "fishing" OR "finswimming" OR "fistball" OR "floorball" OR "flying disc" OR "foosball" OR "futsal" OR "flickerball" OR "football" OR "frisbee" OR "gliding" OR "go" OR "gongfu" OR "gong fu" OR "goalball" OR "golf" OR "golfer" OR "golfers" OR "gymnast" OR "gymnasts" OR "gymnastics" OR "gymnastic" OR "gymkhanas" OR "half rubber" OR "highland games" OR "hap ki do" OR "halfrubber" OR "handball" OR "handballers" OR "handballer" OR "hapkido" OR "hiking" OR "hockey" OR "hsing-I" OR "hurling" OR "Hwa rang do" OR "hwarangdo" OR "horsemanship" OR "horseshoes" OR "orienteer" OR "orienteers" OR "orienteering" OR "iaido" OR "iceboating" OR "icestock" OR "intercrosse" OR "jousting" OR "jai alai" OR "jeet kune do" OR "jianzi" OR "jiu-jitsu" OR "jujutsu" OR "ju-jitsu" OR "kung fu" OR "kungfu" OR "kenpo" OR "judo" OR "judoka" OR "judoists" OR "judoist" OR "jump" OR "jumping" OR "jumper" OR "jian zi" OR "kabaddi" OR "kajukenbo" OR "karate" OR "karateists" OR "karateist" OR "karateka" OR "kayaking" OR "kendo" OR "kenjutsu" OR "kickball" OR "kickbox*" OR "kneeboarding" OR "krav maga" OR "kuk sool won" OR "kun-tao" OR "kuntao" OR "kyudo" OR "korfball" OR "lacrosse" OR "life saving" OR "lapta" OR "lawn tempest" OR "bowling" OR "bowls" OR "logrolling" OR "luge" OR "marathon" OR "marathons" OR "marathoning" OR "martial art" OR "martial arts" OR "martial artist" OR "martial artists" OR "motorsports" OR "mountainboarding" OR "mountain boarding" OR "mountaineer" OR "mountaineering" OR "mountaineers" OR "muay thai" OR "mallakhamb" OR "motorcross" OR "modern arnis" OR "naginata do" OR "netball" OR "ninepins" OR "nine-pins" OR "nordic combined" OR "nunchaku" OR "olympic*" OR "pes\u00e4pallo" OR "pitch and putt" OR "pool" OR "pato" OR "paddleball" OR "paddleboarding" OR "pankration" OR "pancratium" OR "parachuting" OR "paragliding" OR "paramotoring" OR "paraski" OR "paraskiing" OR "paraskier" OR "paraskier" OR "parakour" OR "pelota" OR "pencak silat" OR "pentathlon" OR "p\u00e9tanque" OR "petanque" OR "pickleball" OR "pilota" OR "pole bending" OR "pole vault" OR "polo" OR "polocrosse" OR "powerlifting" OR "player*" OR "powerboating" OR "pegging" OR "parathletic" OR "parathletics" OR "parasport*" OR "paraathletes" OR "paraathlete" OR "pushball" OR "push ball" OR "quidditch" OR "races" OR "race" OR "racing" OR "racewalking" OR "racewalker" OR "racewalkers" OR "rackets" OR "racketlon" OR "racquetball" OR "racquet" OR "racquets" OR "rafting" OR "regattas" OR "riding" OR "ringette" OR "rock-it-ball" OR "rogaining" OR "rock climbing" OR "roll ball" OR "roller derby" OR "roping" OR "rodeos" OR "rodeo" OR "riding" OR "rider" OR "riders" OR "rounders" OR "rowing" OR "rower" OR "rowers" OR "rug ball" OR "running" OR "runner" OR "runners" OR "rugby" OR "sailing" OR "san shou" OR "sepaktakraw" OR "sepak takraw" OR "san-jitsu" OR "savate" OR "shinty" OR "shishimai" OR "shooting" OR "singlestick" OR "single stick" OR "skateboarding" OR "skateboarder" OR "skateboarders" OR "skater" OR "skaters" OR "skating" OR "skipping" OR "racket game*" OR "rollerskating" OR "skelton" OR "skibobbing" OR "ski" OR "skiing" OR "skier" OR "skiers" OR "skydive" OR "skydiving" OR "skydivers" OR "skydiver" OR "skysurfing" OR "sledding" OR "sledging" OR "sled dog" OR "sleddog" OR "snooker" OR "sleighing" OR "snowboarder" OR "snowboarding" OR "snowboarders" OR "snowshoeing" OR "soccer" OR "softball" OR "spear fighting" OR "speed-a-way" OR "speedball" OR "sprint" OR "sprinting" OR "sprints" OR "squash" OR "stick fighting" OR "stickball" OR "stoolball" OR "stunt flying" OR "sumo" OR "surfing" OR "surfer" OR "surfers" OR "swimnastics" OR "swimming" OR "snowmobiling" OR "swim" OR "swimmer" OR "swimmers" OR "shot-put" OR "shot-putters" OR "shot-putter" OR "sport" OR "sports" OR "tae kwon do" OR "taekwondo" OR "taekgyeon" OR "taekkyeon" OR "taekkyon" OR "taekyun" OR "tang soo do" OR "tchoukball" OR "tennis" OR "tetherball" OR "throwing" OR "thrower" OR "throwers" OR "tai ji" OR "tai chi" OR "taiji" OR "t ai chi" OR "throwball" OR "tug of war" OR "tobogganing" OR "track and field" OR "track & field" OR "trampoline" OR "trampolining" OR "trampolinists" OR "trampolinist" OR "trapball" OR "trapshooting" OR "triathlon" OR "triathlete" OR "triathletes" OR "tubing" OR "tumbling" OR "vaulting" OR "volleyball" OR "wakeboarding" OR "wallyball" OR "weightlifting" OR "weightlifter" OR "weightlifters" OR "wiffle ball" OR "windsurfing" OR "windsurfer" OR "windsurfers" OR "walking" OR "wingwalking" OR "woodchopping" OR "wood chopping" OR "woodball" OR "wushu" OR "weight lifter" OR "weight lift" OR "weight lifters" OR "wrestling" OR "wrestler" OR "wrestlers" OR "vovinam" OR "vx" OR "yoga")\n3. #1 AND #2\n'

        list_parser = WOSListParser(
            query_list=query_list, search_field_general="", linter_mode=""
        )
        list_parser.parse()


class TestWOSParser(unittest.TestCase):
    """
    Unit tests for the WOSParser class.

    TestWOSParser is a unittest.TestCase subclass that tests
    the functionality of the WOSParser class.
    It includes the following test methods:

    - setUp: Initializes the test case with a sample query string and a WOSParser instance.
    - test_tokenize: Tests the tokenization of a simple query string.
    - test_tokenize_with_combined_terms:
        Tests the tokenization of a query string with combined terms.
    - test_tokenize_with_special_characters:
        Tests the tokenization of a query string with special characters.

    Each test method verifies that the tokens generated by the WOSParser match the expected tokens.
    """

    def setUp(self) -> None:
        self.query_str = "TI=example AND AU=John Doe"
        self.parser = WOSParser(
            query_str=self.query_str, search_field_general="", mode=""
        )

    def test_tokenize(self) -> None:
        """
        Test the tokenize method of the parser.

        This test verifies that the tokenize method correctly tokenizes
        a given input string into the expected list of tokens with their
        respective positions.

        The expected tokens are:
        - ("TI=", (0, 3))
        - ("example", (3, 10))
        - ("AND", (11, 14))
        - ("AU=", (15, 18))
        - ("John Doe", (18, 26))

        Asserts that the parser's tokens match the expected tokens.
        """
        self.parser.tokenize()
        expected_tokens = [
            Token(value="TI=", type=TokenTypes.FIELD, position=(0, 3)),
            Token(value="example", type=TokenTypes.SEARCH_TERM, position=(3, 10)),
            Token(value="AND", type=TokenTypes.LOGIC_OPERATOR, position=(11, 14)),
            Token(value="AU=", type=TokenTypes.FIELD, position=(15, 18)),
            Token(value="John Doe", type=TokenTypes.SEARCH_TERM, position=(18, 26)),
        ]
        self.assertEqual(self.parser.tokens, expected_tokens)

    def test_tokenize_with_combined_terms(self) -> None:
        """
        Test the `tokenize` method of the parser with a query string that contains combined terms.

        This test sets the `query_str` attribute of the parser to a string with combined terms
        and logical operators, then calls the `tokenize` method. It verifies that the tokens
        generated by the `tokenize` method match the expected tokens.

        The query string used in this test is:
            "TI=example example2 AND AU=John Doe"

        Asserts:
            self.assertEqual(self.parser.tokens, expected_tokens) -> None : Checks if the tokens
            generated by the `tokenize` method match the expected tokens.
        """
        self.parser.query_str = "TI=example example2 AND AU=John Doe"
        self.parser.tokenize()
        expected_tokens = [
            Token(value="TI=", type=TokenTypes.FIELD, position=(0, 3)),
            Token(
                value="example example2", type=TokenTypes.SEARCH_TERM, position=(3, 19)
            ),
            Token(value="AND", type=TokenTypes.LOGIC_OPERATOR, position=(20, 23)),
            Token(value="AU=", type=TokenTypes.FIELD, position=(24, 27)),
            Token(value="John Doe", type=TokenTypes.SEARCH_TERM, position=(27, 35)),
        ]
        self.assertEqual(self.parser.tokens, expected_tokens)

    def test_tokenize_with_multiple_combined_terms(self) -> None:
        """
        Test the `tokenize` method of the parser with a query string that contains combined terms.

        This test sets the `query_str` attribute of the parser to a string with combined terms
        and logical operators, then calls the `tokenize` method. It verifies that the tokens
        generated by the `tokenize` method match the expected tokens.

        The query string used in this test is:
            "TI=example example2 example3 AND AU=John Doe"

        The expected tokens are:
            [

        Asserts:
            self.assertEqual(self.parser.tokens, expected_tokens) -> None : Checks if the tokens
            generated by the `tokenize` method match the expected tokens.
        """
        self.parser.query_str = "TI=example example2 example3 AND AU=John Doe"
        self.parser.tokenize()
        expected_tokens = [
            Token(value="TI=", type=TokenTypes.FIELD, position=(0, 3)),
            Token(
                value="example example2 example3",
                type=TokenTypes.SEARCH_TERM,
                position=(3, 28),
            ),
            Token(value="AND", type=TokenTypes.LOGIC_OPERATOR, position=(29, 32)),
            Token(value="AU=", type=TokenTypes.FIELD, position=(33, 36)),
            Token(value="John Doe", type=TokenTypes.SEARCH_TERM, position=(36, 44)),
        ]
        self.assertEqual(self.parser.tokens, expected_tokens)

    def test_tokenize_with_special_characters(self) -> None:
        """
        Test the `tokenize` method of the parser with a query string containing special characters.

        This test sets the `query_str` attribute of the parser to a string with special characters
        and calls the `tokenize` method. It then checks if the tokens generated by the `tokenize`
        method match the expected tokens.

        The query string used in this test is:
        "TI=ex$mple* AND AU=John?Doe"

        The expected tokens are:
        [

        Asserts:
            self.assertEqual(self.parser.tokens, expected_tokens) -> None : Checks if the tokens generated
            by the `tokenize` method match the expected tokens.
        """
        self.parser.query_str = "TI=ex$mple* AND AU=John?Doe"
        self.parser.tokenize()
        expected_tokens = [
            Token(value="TI=", type=TokenTypes.FIELD, position=(0, 3)),
            Token(value="ex$mple*", type=TokenTypes.SEARCH_TERM, position=(3, 11)),
            Token(value="AND", type=TokenTypes.LOGIC_OPERATOR, position=(12, 15)),
            Token(value="AU=", type=TokenTypes.FIELD, position=(16, 19)),
            Token(value="John?Doe", type=TokenTypes.SEARCH_TERM, position=(19, 27)),
        ]
        self.assertEqual(self.parser.tokens, expected_tokens)

    def test_handle_closing_parenthesis_single_child(self) -> None:
        """
        Test the `handle_closing_parenthesis` method with a single child.

        This test verifies that the `handle_closing_parenthesis` method correctly returns
        the single child when there is only one child in the list.
        """
        children = [Query(value="example", operator=False)]
        result = self.parser.handle_closing_parenthesis(children, current_operator="")
        self.assertEqual(result, children[0])

    def test_handle_closing_parenthesis_with_operator(self) -> None:
        """
        Test the `handle_closing_parenthesis` method with an operator.

        This test verifies that the `handle_closing_parenthesis` method correctly returns
        a Query object with the given operator and children when there is an operator.
        """
        children = [
            Query(value="example1", operator=False),
            Query(value="example2", operator=False),
        ]
        current_operator = "AND"
        result = self.parser.handle_closing_parenthesis(children, current_operator)
        expected_result = Query(
            value=current_operator, operator=True, children=list(children)
        )
        self.assertEqual(result.value, expected_result.value)
        self.assertEqual(result.operator, expected_result.operator)
        self.assertEqual(result.children, expected_result.children)

    def test_handle_operator_uppercase(self) -> None:
        """
        Test the `handle_operator` method with an uppercase operator.

        This test verifies that the `handle_operator` method correctly handles
        an uppercase operator and returns the expected values.
        """
        token = Token(value="AND", type=TokenTypes.LOGIC_OPERATOR, position=(0, 3))
        current_operator = ""
        current_negation = False

        (
            result_operator,
            result_negation,
        ) = self.parser.handle_operator(token, current_operator, current_negation)

        self.assertEqual(result_operator, "AND")
        self.assertFalse(result_negation)

    def test_handle_operator_near_with_distance(self) -> None:
        """
        Test the `handle_operator` method with an uppercase operator.

        This test verifies that the `handle_operator` method correctly handles
        a NEAR operator with a given distance and returns the expected values.
        """
        token = Token(
            value="NEAR/2", type=TokenTypes.PROXIMITY_OPERATOR, position=(0, 6)
        )
        current_operator = ""
        current_negation = False

        (
            result_operator,
            result_negation,
        ) = self.parser.handle_operator(token, current_operator, current_negation)

        self.assertEqual(result_operator, "NEAR/2")
        self.assertFalse(result_negation)

    def test_handle_operator_not(self) -> None:
        """
        Test the `handle_operator` method with the NOT operator.

        This test verifies that the `handle_operator` method correctly handles
        the NOT operator, sets the negation flag, and changes the operator to AND.
        """
        token = Token(value="NOT", type=TokenTypes.LOGIC_OPERATOR, position=(0, 3))
        current_operator = ""
        current_negation = False

        (
            result_operator,
            result_negation,
        ) = self.parser.handle_operator(token, current_operator, current_negation)

        self.assertEqual(result_operator, "AND")
        self.assertTrue(result_negation)

    def test_combine_subsequent_terms_single_term(self) -> None:
        """
        Test the `combine_subsequent_terms` method with a single term.

        This test verifies that the `combine_subsequent_terms` method correctly handles
        a list of tokens with a single term and does not combine it with anything.
        """
        self.parser.tokens = [
            Token(value="example", type=TokenTypes.SEARCH_TERM, position=(0, 7))
        ]
        self.parser.combine_subsequent_terms()
        expected_tokens = [
            Token(value="example", type=TokenTypes.SEARCH_TERM, position=(0, 7))
        ]
        self.assertEqual(self.parser.tokens, expected_tokens)

    def test_combine_subsequent_terms_multiple_terms(self) -> None:
        """
        Test the `combine_subsequent_terms` method with multiple terms.

        This test verifies that the `combine_subsequent_terms` method correctly combines
        subsequent terms into a single token.
        """
        self.parser.tokens = [
            Token(value="example", type=TokenTypes.SEARCH_TERM, position=(0, 7)),
            Token(value="example2", type=TokenTypes.SEARCH_TERM, position=(8, 16)),
        ]
        self.parser.combine_subsequent_terms()
        expected_tokens = [
            Token(
                value="example example2", type=TokenTypes.SEARCH_TERM, position=(0, 16)
            )
        ]
        self.assertEqual(self.parser.tokens, expected_tokens)

    def test_combine_subsequent_terms_with_operators(self) -> None:
        """
        Test the `combine_subsequent_terms` method with terms and operators.

        This test verifies that the `combine_subsequent_terms` method correctly combines
        subsequent terms into a single token and does not combine terms with operators.
        """
        self.parser.tokens = [
            Token(value="example", type=TokenTypes.SEARCH_TERM, position=(0, 7)),
            Token(value="AND", type=TokenTypes.LOGIC_OPERATOR, position=(8, 11)),
            Token(value="example2", type=TokenTypes.SEARCH_TERM, position=(12, 20)),
        ]
        self.parser.combine_subsequent_terms()
        expected_tokens = [
            Token(value="example", type=TokenTypes.SEARCH_TERM, position=(0, 7)),
            Token(value="AND", type=TokenTypes.LOGIC_OPERATOR, position=(8, 11)),
            Token(value="example2", type=TokenTypes.SEARCH_TERM, position=(12, 20)),
        ]
        self.assertEqual(self.parser.tokens, expected_tokens)

    def test_combine_subsequent_terms_with_special_characters(self) -> None:
        """
        Test the `combine_subsequent_terms` method with terms containing special characters.

        This test verifies that the `combine_subsequent_terms` method correctly combines
        subsequent terms containing special characters into a single token.
        """
        self.parser.tokens = [
            Token(value="ex$mple", type=TokenTypes.SEARCH_TERM, position=(0, 7)),
            Token(value="example2", type=TokenTypes.SEARCH_TERM, position=(8, 16)),
        ]
        self.parser.combine_subsequent_terms()
        expected_tokens = [
            Token(
                value="ex$mple example2", type=TokenTypes.SEARCH_TERM, position=(0, 16)
            )
        ]
        self.assertEqual(self.parser.tokens, expected_tokens)

    def test_combine_subsequent_terms_with_mixed_case(self) -> None:
        """
        Test the `combine_subsequent_terms` method with terms in mixed case.

        This test verifies that the `combine_subsequent_terms` method correctly combines
        subsequent terms in mixed case into a single token.
        """
        self.parser.tokens = [
            Token(value="Example", type=TokenTypes.SEARCH_TERM, position=(0, 7)),
            Token(value="example2", type=TokenTypes.SEARCH_TERM, position=(8, 16)),
        ]
        self.parser.combine_subsequent_terms()
        expected_tokens = [
            Token(
                value="Example example2", type=TokenTypes.SEARCH_TERM, position=(0, 16)
            )
        ]
        self.assertEqual(self.parser.tokens, expected_tokens)

    def test_append_children_with_same_operator(self) -> None:
        """
        Test the `append_children` method with the same operator.

        This test verifies that the `append_children` method correctly appends
        the children of the sub expression to the last child when the current operator
        is the same as the last child and the sub expression value.
        """
        children = [
            Query(
                value="AND",
                operator=True,
                children=[Query(value="example1", operator=False)],
            )
        ]
        sub_expr = Query(
            value="AND",
            operator=True,
            children=[Query(value="example2", operator=False)],
        )
        current_operator = "AND"

        result = self.parser.append_children(children, sub_expr, current_operator)
        expected_result = [
            Query(
                value="AND",
                operator=True,
                children=[
                    Query(value="example1", operator=False),
                    Query(value="example2", operator=False),
                ],
            )
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].children[0].value, expected_result[0].children[0].value
        )
        self.assertEqual(
            result[0].children[0].operator, expected_result[0].children[0].operator
        )
        self.assertEqual(
            result[0].children[1].value, expected_result[0].children[1].value
        )
        self.assertEqual(
            result[0].children[1].operator, expected_result[0].children[1].operator
        )

    def test_append_children_with_operator_and_term(self) -> None:
        """
        Test the `append_children` method with an operator and a term.

        This test verifies that the `append_children` method correctly appends
        the sub expression to the last child when the last child is an operator
        and the sub expression is a term.
        """
        children = [
            Query(
                value="AND",
                operator=True,
                children=[Query(value="example1", operator=False)],
            )
        ]
        sub_expr = Query(value="example2", operator=False)
        current_operator = "AND"

        result = self.parser.append_children(children, sub_expr, current_operator)
        expected_result = [
            Query(
                value="AND",
                operator=True,
                children=[
                    Query(value="example1", operator=False),
                    Query(value="example2", operator=False),
                ],
            )
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].children[0].value, expected_result[0].children[0].value
        )
        self.assertEqual(
            result[0].children[0].operator, expected_result[0].children[0].operator
        )
        self.assertEqual(
            result[0].children[1].value, expected_result[0].children[1].value
        )
        self.assertEqual(
            result[0].children[1].operator, expected_result[0].children[1].operator
        )

    def test_append_children_with_different_operator(self) -> None:
        """
        Test the `append_children` method with a different operator.

        This test verifies that the `append_children` method correctly appends
        the sub expression to the list of children when the current operator
        is different from the last child.
        """
        children = [
            Query(
                value="AND",
                operator=True,
                children=[Query(value="example1", operator=False)],
            )
        ]
        sub_expr = Query(
            value="OR",
            operator=True,
            children=[Query(value="example2", operator=False)],
        )
        current_operator = "OR"

        result = self.parser.append_children(children, sub_expr, current_operator)
        expected_result = [
            Query(
                value="AND",
                operator=True,
                children=[Query(value="example1", operator=False)],
            ),
            Query(value="example2", operator=False),
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].children[0].value, expected_result[0].children[0].value
        )
        self.assertEqual(
            result[0].children[0].operator, expected_result[0].children[0].operator
        )
        self.assertEqual(result[1].value, expected_result[1].value)
        self.assertEqual(result[1].operator, expected_result[1].operator)

    def test_append_children_with_empty_children(self) -> None:
        """
        Test the `append_children` method with empty children.

        This test verifies that the `append_children` method correctly appends
        the sub expression to the list of children when the children list is empty.
        """
        children: typing.List[Query] = []
        sub_expr = Query(value="example1", operator=False)
        current_operator = "AND"

        result = self.parser.append_children(children, sub_expr, current_operator)
        expected_result = [Query(value="example1", operator=False)]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)

    def test_append_children_with_operator_and_sub_expr_operator(self) -> None:
        """
        Test the `append_children` method with an operator and a sub expression operator.

        This test verifies that the `append_children` method correctly appends
        the sub expression to the last child when the last child is an operator
        and the sub expression is also an operator.
        """
        children = [
            Query(
                value="AND",
                operator=True,
                children=[Query(value="example1", operator=False)],
            )
        ]
        sub_expr = Query(
            value="AND",
            operator=True,
            children=[Query(value="example2", operator=False)],
        )
        current_operator = "AND"

        result = self.parser.append_children(children, sub_expr, current_operator)
        expected_result = [
            Query(
                value="AND",
                operator=True,
                children=[
                    Query(value="example1", operator=False),
                    Query(value="example2", operator=False),
                ],
            )
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].children[0].value, expected_result[0].children[0].value
        )
        self.assertEqual(
            result[0].children[0].operator, expected_result[0].children[0].operator
        )
        self.assertEqual(
            result[0].children[1].value, expected_result[0].children[1].value
        )
        self.assertEqual(
            result[0].children[1].operator, expected_result[0].children[1].operator
        )

    def test_add_linter_message_new_message(self) -> None:
        """
        Test the `add_linter_message` method with a new message.

        This test verifies that the `add_linter_message` method correctly adds
        a new linter message to the `linter_messages` list.
        """
        rule = QueryErrorCode.OPERATOR_CAPITALIZATION
        position = (0, 10)

        self.parser.add_linter_message(rule, pos=position)
        expected_message = {
            "code": "W0005",
            "label": "operator-capitalization",
            "message": "Operators should be capitalized",
            "is_fatal": False,
            "pos": (0, 10),
        }
        self.assertIn(expected_message, self.parser.linter_messages)

    def test_add_linter_message_duplicate_message(self) -> None:
        """
        Test the `add_linter_message` method with a duplicate message.

        This test verifies that the `add_linter_message` method does not add
        a duplicate linter message to the `linter_messages` list.
        """
        rule = QueryErrorCode.OPERATOR_CAPITALIZATION
        position = (0, 10)
        self.parser.linter_messages = []

        self.parser.add_linter_message(rule, pos=position)
        self.parser.add_linter_message(rule, pos=position)
        print(self.parser.linter_messages)
        self.assertEqual(len(self.parser.linter_messages), 1)

    def test_add_linter_message_different_position(self) -> None:
        """
        Test the `add_linter_message` method with the same message but different positions.

        This test verifies that the `add_linter_message` method correctly adds
        the same message with different positions to the `linter_messages` list.
        """
        rule = QueryErrorCode.OPERATOR_CAPITALIZATION
        position1 = (0, 10)
        position2 = (11, 20)

        self.parser.add_linter_message(rule, pos=position1)
        self.parser.add_linter_message(rule, pos=position2)
        expected_message1 = {
            "code": "W0005",
            "label": "operator-capitalization",
            "message": "Operators should be capitalized",
            "is_fatal": False,
            "pos": (0, 10),
        }
        expected_message2 = {
            "code": "W0005",
            "label": "operator-capitalization",
            "message": "Operators should be capitalized",
            "is_fatal": False,
            "pos": (11, 20),
        }
        self.assertIn(expected_message1, self.parser.linter_messages)
        self.assertIn(expected_message2, self.parser.linter_messages)

    def test_handle_year_search_valid_year_span(self) -> None:
        """
        Test the `handle_year_search` method with a valid year span.

        This test verifies that the `handle_year_search` method correctly handles
        a valid year span and adds the year search field to the list of children.
        """
        token = Token(value="2015-2019", type=TokenTypes.SEARCH_TERM, position=(0, 9))
        children: typing.List[Query] = []
        current_operator = "AND"

        result = self.parser.handle_year_search(token, children, current_operator)
        expected_result = [
            Query(
                value="AND",
                operator=True,
                children=[
                    Query(
                        value=token.value,
                        operator=False,
                        search_field=SearchField(
                            value=Fields.YEAR, position=token.position
                        ),
                        position=token.position,
                    )
                ],
            )
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].children[0].search_field.value,  # type: ignore
            expected_result[0].children[0].search_field.value,  # type: ignore
        )
        self.assertEqual(
            result[0].children[0].position, expected_result[0].children[0].position
        )

    def test_handle_year_search_single_year(self) -> None:
        """
        Test the `handle_year_search` method with a single year.

        This test verifies that the `handle_year_search` method correctly handles
        a single year and adds the year search field to the list of children.
        """
        token = Token(value="2015", type=TokenTypes.SEARCH_TERM, position=(0, 4))
        children: typing.List[Query] = []
        current_operator = "AND"

        result = self.parser.handle_year_search(token, children, current_operator)
        expected_result = [
            Query(
                value="AND",
                operator=True,
                children=[
                    Query(
                        value=token.value,
                        operator=False,
                        search_field=SearchField(
                            value=Fields.YEAR, position=token.position
                        ),
                        position=token.position,
                    )
                ],
            )
        ]
        self.assertEqual(
            result[0].children[0].value, expected_result[0].children[0].value
        )
        self.assertEqual(
            result[0].children[0].operator, expected_result[0].children[0].operator
        )
        self.assertEqual(
            result[0].children[0].search_field.value,  # type: ignore
            expected_result[0].children[0].search_field.value,  # type: ignore
        )
        self.assertEqual(
            result[0].children[0].position, expected_result[0].children[0].position
        )

    def test_add_term_node_without_current_operator(self) -> None:
        """
        Test the `add_term_node` method without a current operator.

        This test verifies that the `add_term_node` method correctly adds
        a term node to the list of children when there is no current operator.
        """
        tokens = [Token(value="example", type=TokenTypes.SEARCH_TERM, position=(0, 7))]
        self.parser.tokens = tokens
        index = 0
        value = "example"
        operator = False
        search_field = SearchField(value="TI=", position=(0, 3))
        position = (0, 7)
        current_operator = ""
        children: typing.List[Query] = []

        result = self.parser.add_term_node(
            index,
            value,
            operator,
            search_field,
            position,
            current_operator,
            children,
        )
        expected_result = [
            Query(
                value=value,
                operator=operator,
                search_field=search_field,
                position=position,
            )
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].search_field.value, expected_result[0].search_field.value  # type: ignore
        )
        self.assertEqual(result[0].position, expected_result[0].position)

    def test_add_term_node_with_current_operator(self) -> None:
        """
        Test the `add_term_node` method with a current operator.

        This test verifies that the `add_term_node` method correctly adds
        a term node to the list of children when there is a current operator.
        """
        tokens = [Token(value="example", type=TokenTypes.SEARCH_TERM, position=(0, 7))]
        self.parser.tokens = tokens
        index = 0
        value = "example"
        operator = False
        search_field = SearchField(value="TI=", position=(0, 3))
        position = (0, 7)
        current_operator = "AND"
        children: typing.List[Query] = []

        result = self.parser.add_term_node(
            index,
            value,
            operator,
            search_field,
            position,
            current_operator,
            children,
        )
        expected_result = [
            Query(
                value=current_operator,
                operator=True,
                children=[
                    Query(
                        value=value,
                        operator=operator,
                        search_field=search_field,
                        position=position,
                    )
                ],
            )
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].children[0].value, expected_result[0].children[0].value
        )
        self.assertEqual(
            result[0].children[0].operator, expected_result[0].children[0].operator
        )
        self.assertEqual(
            result[0].children[0].search_field.value,  # type: ignore
            expected_result[0].children[0].search_field.value,  # type: ignore
        )
        self.assertEqual(
            result[0].children[0].position, expected_result[0].children[0].position
        )

    def test_add_term_node_with_near_operator(self) -> None:
        """
        Test the `add_term_node` method with a NEAR operator.

        This test verifies that the `add_term_node` method correctly adds
        a term node to the list of children when there is a NEAR operator.
        """
        tokens = [
            Token(value="example", type=TokenTypes.SEARCH_TERM, position=(0, 7)),
            Token(value="example2", type=TokenTypes.SEARCH_TERM, position=(8, 16)),
            Token(value="example3", type=TokenTypes.SEARCH_TERM, position=(17, 25)),
        ]
        self.parser.tokens = tokens
        index = 1
        value = "example2"
        operator = False
        search_field = SearchField(value="TI=", position=(0, 3))
        position = (8, 16)
        current_operator = "NEAR/5"
        children = [
            Query(
                value="NEAR",
                operator=True,
                children=[
                    Query(
                        value="example",
                        operator=False,
                        search_field=search_field,
                        position=(0, 7),
                    ),
                    Query(
                        value="example2",
                        operator=False,
                        search_field=search_field,
                        position=(8, 16),
                    ),
                ],
                distance=5,
            )
        ]

        result = self.parser.add_term_node(
            index,
            value,
            operator,
            search_field,
            position,
            current_operator,
            children,
        )
        expected_result = [
            Query(
                value="AND",
                operator=True,
                children=[
                    Query(
                        value="NEAR",
                        operator=True,
                        children=[
                            Query(
                                value="example",
                                operator=False,
                                search_field=search_field,
                                position=(0, 7),
                            ),
                            Query(
                                value="example2",
                                operator=False,
                                search_field=search_field,
                                position=(8, 16),
                            ),
                        ],
                        distance=5,
                    ),
                    Query(
                        value="example2",
                        operator=False,
                        search_field=search_field,
                        position=(8, 16),
                    ),
                    Query(
                        value="example3",
                        operator=False,
                        search_field=search_field,
                        position=(17, 25),
                    ),
                ],
            )
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].children[0].value, expected_result[0].children[0].value
        )
        self.assertEqual(
            result[0].children[0].operator, expected_result[0].children[0].operator
        )
        self.assertEqual(
            result[0].children[0].children[0].value,
            expected_result[0].children[0].children[0].value,
        )
        self.assertEqual(
            result[0].children[0].children[0].operator,
            expected_result[0].children[0].children[0].operator,
        )
        self.assertEqual(
            result[0].children[0].children[1].value,
            expected_result[0].children[0].children[1].value,
        )
        self.assertEqual(
            result[0].children[0].children[1].operator,
            expected_result[0].children[0].children[1].operator,
        )

    def test_add_term_node_with_existing_children(self) -> None:
        """
        Test the `add_term_node` method with existing children.

        This test verifies that the `add_term_node` method correctly adds
        a term node to the existing list of children.
        """
        tokens = [Token(value="example", type=TokenTypes.SEARCH_TERM, position=(0, 7))]
        self.parser.tokens = tokens
        index = 0
        value = "example"
        operator = False
        search_field = SearchField(value="TI=", position=(0, 3))
        position = (0, 7)
        current_operator = ""
        children = [
            Query(
                value="existing",
                operator=False,
                search_field=search_field,
                position=(0, 8),
            )
        ]

        result = self.parser.add_term_node(
            index,
            value,
            operator,
            search_field,
            position,
            current_operator,
            children,
        )
        expected_result = [
            Query(
                value="existing",
                operator=False,
                search_field=search_field,
                position=(0, 8),
            ),
            Query(
                value=value,
                operator=operator,
                search_field=search_field,
                position=position,
            ),
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].search_field.value, expected_result[0].search_field.value  # type: ignore
        )
        self.assertEqual(result[0].position, expected_result[0].position)
        self.assertEqual(result[1].value, expected_result[1].value)
        self.assertEqual(result[1].operator, expected_result[1].operator)
        self.assertEqual(
            result[1].search_field.value, expected_result[1].search_field.value  # type: ignore
        )
        self.assertEqual(result[1].position, expected_result[1].position)

    def test_add_term_node_with_current_negation(self) -> None:
        """
        Test the `add_term_node` method with current negation.

        This test verifies that the `add_term_node` method correctly adds
        a term node to the list of children when there is a current negation.
        """
        tokens = [Token(value="example", type=TokenTypes.SEARCH_TERM, position=(0, 7))]
        self.parser.tokens = tokens
        index = 0
        value = "example"
        operator = False
        search_field = SearchField(value="TI=", position=(0, 3))
        position = (0, 7)
        current_operator = "AND"
        children: typing.List[Query] = []
        current_negation = True

        result = self.parser.add_term_node(
            index,
            value,
            operator,
            search_field,
            position,
            current_operator,
            children,
            current_negation,
        )
        expected_result = [
            Query(
                value=current_operator,
                operator=True,
                children=[
                    Query(
                        value=value,
                        operator=operator,
                        search_field=search_field,
                        position=position,
                    )
                ],
            )
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].children[0].value, expected_result[0].children[0].value
        )
        self.assertEqual(
            result[0].children[0].operator, expected_result[0].children[0].operator
        )
        self.assertEqual(
            result[0].children[0].search_field.value,  # type: ignore
            expected_result[0].children[0].search_field.value,  # type: ignore
        )
        self.assertEqual(
            result[0].children[0].position, expected_result[0].children[0].position
        )

    def test_check_search_fields_title(self) -> None:
        """
        Test the `check_search_fields` method with title search fields.

        This test verifies that the `check_search_fields` method correctly translates
        title search fields into the base search field "TI=".
        """
        title_fields = ["TI=", "Title", "ti=", "title=", "ti", "title", "TI", "TITLE"]
        for field in title_fields:
            result = self.parser._map_default_field(field)
            self.assertEqual(result, "ti")

    def test_check_search_fields_abstract(self) -> None:
        """
        Test the `check_search_fields` method with abstract search fields.

        This test verifies that the `check_search_fields` method correctly translates
        abstract search fields into the base search field "AB=".
        """
        abstract_fields = [
            "AB=",
            "ab=",
            "abstract=",
            # "Abstract",
            # "ab",
            # "abstract",
            # "AB",
            # "ABSTRACT",
        ]
        for field in abstract_fields:
            result = self.parser._map_default_field(field)
            self.assertEqual(result, "ab")

    def test_check_search_fields_author(self) -> None:
        """
        Test the `check_search_fields` method with author search fields.

        This test verifies that the `check_search_fields` method correctly translates
        author search fields into the base search field "AU=".
        """
        author_fields = [
            "AU=",
            "Author",
            "au=",
            "author=",
            # "au",
            # "author",
            # "AU",
            # "AUTHOR",
        ]
        for field in author_fields:
            result = self.parser._map_default_field(field)
            self.assertEqual(result, "au")

    def test_check_search_fields_topic(self) -> None:
        """
        Test the `check_search_fields` method with topic search fields.

        This test verifies that the `check_search_fields` method correctly translates
        topic search fields into the base search field "TS=".
        """
        topic_fields = [
            "TS=",
            "ts=",
            "topic=",
            # "Topic",
            # "ts",
            # "topic",
            # "TS",
            # "TOPIC",
            # "Topic Search",
            # "Topic TS",
        ]
        for field in topic_fields:
            result = self.parser._map_default_field(field)
            self.assertEqual(result, "ts")

    def test_check_search_fields_language(self) -> None:
        """
        Test the `check_search_fields` method with language search fields.

        This test verifies that the `check_search_fields` method correctly translates
        language search fields into the base search field "LA=".
        """
        language_fields = [
            "LA=",
            "la=",
            "language=",
            # "Languages",
            # "la",
            # "language",
            # "LA",
            # "LANGUAGE",
        ]
        for field in language_fields:
            result = self.parser._map_default_field(field)
            self.assertEqual(result, "la")

    def test_check_search_fields_year(self) -> None:
        """
        Test the `check_search_fields` method with year search fields.

        This test verifies that the `check_search_fields` method correctly translates
        year search fields into the base search field "PY=".
        """
        year_fields = [
            "PY=",
            "py=",
            "py",
            # "Publication Year",
            # "publication year",
            # "PY",
            # "PUBLICATION YEAR",
        ]
        for field in year_fields:
            result = self.parser._map_default_field(field)
            self.assertEqual(result, "py")

    def test_check_search_fields_misc(self) -> None:
        """
        Test the `check_search_fields` method with unknown search fields.
        """
        misc_fields = ["INVALID", "123", "random", "field"]
        for field in misc_fields:
            result = self.parser._map_default_field(field)
            self.assertEqual(result, field)

    def test_safe_children_with_single_child(self) -> None:
        """
        Test the `safe_children` method with a single child.

        This test verifies that the `safe_children` method correctly wraps
        a single child in a Query object with the given operator.
        """
        children = [Query(value="example", operator=False)]
        current_operator = "AND"
        result = self.parser.wrap_with_operator_node(children, current_operator)
        expected_result = [
            Query(value=current_operator, operator=True, children=list(children))
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].children[0].value, expected_result[0].children[0].value
        )
        self.assertEqual(
            result[0].children[0].operator, expected_result[0].children[0].operator
        )

    def test_safe_children_with_multiple_children(self) -> None:
        """
        Test the `safe_children` method with multiple children.

        This test verifies that the `safe_children` method correctly wraps
        multiple children in a Query object with the given operator.
        """
        children = [
            Query(value="example1", operator=False),
            Query(value="example2", operator=False),
        ]
        current_operator = "OR"
        result = self.parser.wrap_with_operator_node(children, current_operator)
        expected_result = [
            Query(value=current_operator, operator=True, children=list(children))
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(
            result[0].children[0].value, expected_result[0].children[0].value
        )
        self.assertEqual(
            result[0].children[0].operator, expected_result[0].children[0].operator
        )
        self.assertEqual(
            result[0].children[1].value, expected_result[0].children[1].value
        )
        self.assertEqual(
            result[0].children[1].operator, expected_result[0].children[1].operator
        )

    def test_safe_children_with_empty_children(self) -> None:
        """
        Test the `safe_children` method with empty children.

        This test verifies that the `safe_children` method correctly handles
        an empty list of children and wraps it in a Query object with the given operator.
        """
        children: typing.List[Query] = []
        current_operator = "AND"
        result = self.parser.wrap_with_operator_node(children, current_operator)
        expected_result = [
            Query(value=current_operator, operator=True, children=list(children))
        ]
        self.assertEqual(result[0].value, expected_result[0].value)
        self.assertEqual(result[0].operator, expected_result[0].operator)
        self.assertEqual(result[0].children, expected_result[0].children)

    def test_query_parsing_1(self) -> None:
        parser = WOSParser(
            query_str="TI=example AND AU=John Doe", search_field_general="", mode=""
        )
        query = parser.parse()
        self.assertEqual(query.value, "AND")
        self.assertTrue(query.operator)
        self.assertEqual(len(query.children), 2)
        self.assertEqual(query.children[0].value, "example")
        self.assertFalse(query.children[0].operator)
        self.assertEqual(query.children[1].value, "John Doe")
        self.assertEqual(query.children[1].search_field.value, "au")  # type: ignore
        self.assertFalse(query.children[1].operator)

    def test_query_parsing_2(self) -> None:
        parser = WOSParser(
            query_str="TI=example AND (AU=John Doe OR AU=John Wayne)",
            search_field_general="",
            mode="",
        )
        query = parser.parse()
        self.assertEqual(query.value, "AND")
        self.assertTrue(query.operator)
        self.assertEqual(len(query.children), 2)
        self.assertEqual(query.children[0].value, "example")
        self.assertFalse(query.children[0].operator)
        self.assertEqual(query.children[1].value, "OR")

        self.assertEqual(query.children[1].children[1].value, "John Wayne")
        self.assertEqual(query.children[1].children[1].search_field.value, "au")  # type: ignore

    def test_query_parsing_basic_vs_advanced(self) -> None:
        # TODO : clarify basic vs advanced search in the docs!

        # Basic search
        parser = WOSParser(
            query_str="digital AND online", search_field_general="ALL=", mode=""
        )
        parser.parse()
        self.assertEqual(len(parser.linter_messages), 0)

        # search field could be nested
        parser = WOSParser(
            query_str="(TI=digital AND AB=online)", search_field_general="ALL=", mode=""
        )
        parser.parse()
        self.assertEqual(len(parser.linter_messages), 0)

        # Advanced search
        parser = WOSParser(
            query_str="ALL=(digital AND online)", search_field_general="", mode=""
        )
        parser.parse()
        self.assertEqual(len(parser.linter_messages), 0)
        parser = WOSParser(
            query_str="(ALL=digital AND ALL=online)", search_field_general="", mode=""
        )
        parser.parse()
        self.assertEqual(len(parser.linter_messages), 0)

        # ERROR: Basic search without search_field_general
        parser = WOSParser(
            query_str="digital AND online", search_field_general="", mode=""
        )
        parser.parse()
        self.assertEqual(len(parser.linter_messages), 1)

        # ERROR: Advanced search with search_field_general
        parser = WOSParser(
            query_str="ALL=(digital AND online)", search_field_general="ALL=", mode=""
        )
        parser.parse()
        self.assertEqual(len(parser.linter_messages), 1)

        # ERROR: Advanced search with search_field_general
        parser = WOSParser(
            query_str="TI=(digital AND online)", search_field_general="ALL=", mode=""
        )
        parser.parse()
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "E0002",
                "label": "search-field-contradiction",
                "message": "Contradictory search fields specified",
                "is_fatal": False,
                "pos": (0, 3),
            },
        )


if __name__ == "__main__":
    unittest.main()

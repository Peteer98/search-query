"""Web-of-Science linter unit tests."""
import unittest

from search_query.constants import Token
from search_query.constants import TokenTypes
from search_query.linter_wos import QueryLinter
from search_query.parser_wos import WOSParser

# ruff: noqa: E501
# flake8: noqa: E501


class TestQueryLinter(unittest.TestCase):
    """Test suite for the QueryLinter class."""

    def setUp(self) -> None:
        self.linter_messages: list = []

    def test_no_parentheses(self) -> None:
        """
        Test that the QueryLinter correctly identifies a query with no unmatched parentheses.

        This test initializes a QueryLinter instance with a test query and checks that
        the `check_unmatched_parentheses` method returns False, indicating no unmatched
        parentheses are present. It also verifies that no linter messages are generated.

        Assertions:
            - The `check_unmatched_parentheses` method should return False.
            - The length of `self.linter_messages` should be 0.
        """
        parser = WOSParser("test query")
        linter = QueryLinter(parser)
        linter.check_unmatched_parentheses()
        self.assertEqual(len(parser.linter_messages), 0)

    def test_matched_parentheses(self) -> None:
        """
        Test case for checking matched parentheses in a query string.

        This test initializes a QueryLinter object with
        a query string containing matched parentheses
        and verifies that the linter does not detect any unmatched parentheses. It also checks that
        no linter messages are generated.

        Assertions:
            - The linter should not detect any unmatched parentheses.
            - The length of linter messages should be 0.
        """
        parser = WOSParser("(test query)")
        linter = QueryLinter(parser)
        linter.check_unmatched_parentheses()
        self.assertEqual(len(parser.linter_messages), 0)

    def test_unmatched_opening_parenthesis(self) -> None:
        """
        Test case for detecting an unmatched opening parenthesis in a query.

        This test initializes a QueryLinter instance with a query containing an unmatched
        opening parenthesis and checks if the linter correctly identifies the issue.
        It verifies that the linter messages contain the appropriate rule, message, and position
        for the unmatched parenthesis.

        Asserts:
            - The linter detects unmatched parentheses.
            - The length of linter messages is 1.
            - The rule in the linter message is "F0002".
            - The message in the linter message is "Unmatched opening parenthesis '('."
            - The position in the linter message is (0, 1).
        """
        parser = WOSParser("(test query")
        linter = QueryLinter(parser)
        linter.check_unmatched_parentheses()
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F1002",
                "is_fatal": True,
                "details": "",
                "label": "unmatched-opening-parenthesis",
                "message": "Unmatched opening parenthesis",
                "position": (0, 1),
            },
        )

    def test_unmatched_closing_parenthesis(self) -> None:
        """
        Test case for detecting an unmatched closing parenthesis in a query string.

        This test initializes a QueryLinter object with a query string containing
        an unmatched closing parenthesis and checks if the linter correctly identifies
        the unmatched parenthesis. It verifies that the linter messages contain the
        appropriate rule, message, and position for the unmatched parenthesis.

        Assertions:
            - The linter should detect the unmatched closing parenthesis.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F0002".
            - The message in the linter message should indicate an unmatched closing parenthesis.
            - The position in the linter message should be (10, 11).
        """
        parser = WOSParser("test query)")
        linter = QueryLinter(parser)
        linter.check_unmatched_parentheses()
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F1003",
                "is_fatal": True,
                "details": "",
                "label": "unmatched-closing-parenthesis",
                "message": "Unmatched closing parenthesis",
                "position": (10, 11),
            },
        )

    def test_multiple_unmatched_parentheses(self) -> None:
        """
        Test case for checking unmatched parentheses in a query string.

        This test verifies that the QueryLinter correctly identifies and reports
        an unmatched closing parenthesis in the query string. It checks that:
        - The linter detects the unmatched parenthesis.
        - The linter messages list contains exactly one message.
        - The message rule is "F0002".
        - The message text indicates an unmatched closing parenthesis.
        - The position of the unmatched parenthesis is correctly reported.
        """
        parser = WOSParser("(test query))")
        linter = QueryLinter(parser)
        linter.check_unmatched_parentheses()
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F1003",
                "is_fatal": True,
                "details": "",
                "label": "unmatched-closing-parenthesis",
                "message": "Unmatched closing parenthesis",
                "position": (12, 13),
            },
        )

    def test_nested_unmatched_parentheses(self) -> None:
        """
        Test case for checking unmatched parentheses in a nested query.

        This test initializes a QueryLinter instance with a query containing
        unmatched parentheses and verifies that the linter correctly identifies
        the unmatched opening parenthesis. It checks that the linter messages
        contain the appropriate rule, message, and position for the unmatched
        parenthesis.

        Assertions:
            - The linter's check_unmatched_parentheses method returns True.
            - The length of linter_messages is 1.
            - The rule in the first linter message is "F0002".
            - The message in the first linter message is "Unmatched opening parenthesis '('."
            - The position in the first linter message is (0, 1).
        """
        parser = WOSParser("((test query)")
        linter = QueryLinter(parser)
        linter.check_unmatched_parentheses()
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F1002",
                "is_fatal": True,
                "details": "",
                "label": "unmatched-opening-parenthesis",
                "message": "Unmatched opening parenthesis",
                "position": (0, 1),
            },
        )

    def test_two_operators_in_a_row(self) -> None:
        """
        Test case for detecting two operators in a row in a query string.

        This test initializes a QueryLinter object with a query string containing
        two operators in a row and checks if the linter correctly identifies the issue.
        It verifies that the linter messages contain the appropriate rule, message, and position
        for the two operators.

        Assertions:
            - The linter should detect two operators in a row.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F0005".
            - The message in the linter message should indicate two operators in a row.
            - The position in the linter message should be (5, 6).
        """

        parser = WOSParser("term1 AND OR")
        parser.tokenize()
        linter = QueryLinter(parser)
        linter.check_order_of_tokens()
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F1004",
                "is_fatal": True,
                "details": "",
                "label": "invalid-token-sequence",
                "message": "The sequence of tokens is invalid.",
                "position": (10, 12),
            },
        )

    def test_two_search_fields_in_a_row(self) -> None:
        """
        Test case for detecting two search fields in a row in a query string.

        This test initializes a QueryLinter object with a query string containing
        two search fields in a row and checks if the linter correctly identifies the issue.
        It verifies that the linter messages contain the appropriate rule, message, and position
        for the two search fields.

        Assertions:
            - The linter should detect two search fields in a row.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F0003".
            - The message in the linter message should indicate two search fields in a row.
            - The position in the linter message should be (5, 10).
        """
        [
            Token(value="term1", type=TokenTypes.SEARCH_TERM, position=(0, 5)),
            Token(value="au=", type=TokenTypes.FIELD, position=(5, 10)),
            Token(value="ti=", type=TokenTypes.FIELD, position=(10, 15)),
        ]

        parser = WOSParser("term1 au= ti=")
        parser.tokenize()
        linter = QueryLinter(parser)
        linter.check_order_of_tokens()
        self.assertEqual(len(parser.linter_messages), 2)
        self.assertEqual(
            parser.linter_messages[0],
            # TODO : this shows that the message can be ambiguous
            {
                "code": "F1004",
                "label": "invalid-token-sequence",
                "message": "The sequence of tokens is invalid.",
                "is_fatal": True,
                "details": "",
                "position": (6, 9),
            },
            {
                "code": "F1005",
                "label": "invalid-token-sequence-two-search-fields",
                "message": "Invalid token sequence: two search fields in a row.",
                "is_fatal": True,
                "details": "",
                "position": (10, 13),
            },
        )

    def test_missing_operator_between_term_and_parenthesis(self) -> None:
        """
        Test case for detecting missing operator between term and parenthesis in a query string.

        This test initializes a QueryLinter object with a query string containing
        a term followed by an opening parenthesis without an operator in between.
        It verifies that the linter messages contain the appropriate rule, message, and position
        for the missing operator.

        Assertions:
            - The linter should detect the missing operator between term and parenthesis.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F0003".
            - The message in the linter message should indicate
                a missing operator between term and parenthesis.
            - The position in the linter message should be (5, 6).
        """
        parser = WOSParser("term1 (query)")
        parser.tokenize()
        linter = QueryLinter(parser)
        linter.check_order_of_tokens()
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F1004",
                "is_fatal": True,
                "details": "",
                "label": "invalid-token-sequence",
                "message": "The sequence of tokens is invalid.",
                "position": (6, 7),
            },
        )

    def test_missing_operator_between_parentheses(self) -> None:
        """
        Test case for detecting missing operator between
        closing and opening parenthesis in a query string.

        This test initializes a QueryLinter object with a query string containing
        a closing parenthesis followed by an opening parenthesis without an operator in between.
        It verifies that the linter messages contain the appropriate rule, message, and position
        for the missing operator.

        Assertions:
            - The linter should detect the missing operator between closing and opening parenthesis.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F0003".
            - The message in the linter message should indicate
                a missing operator between closing and opening parenthesis.
            - The position in the linter message should be (5, 6).
        """
        parser = WOSParser(") (query)")
        parser.tokenize()
        linter = QueryLinter(parser)
        linter.check_order_of_tokens()
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F1004",
                "is_fatal": True,
                "details": "",
                "label": "invalid-token-sequence",
                "message": "The sequence of tokens is invalid.",
                "position": (2, 3),
            },
        )

    def test_missing_operator_between_term_and_search_field(self) -> None:
        """
        Test case for detecting missing operator between term and search field in a query string.

        This test initializes a QueryLinter object with a query string containing
        a term followed by a search field without an operator in between.
        It verifies that the linter messages contain the appropriate rule, message, and position
        for the missing operator.

        Assertions:
            - The linter should detect the missing operator between term and search field.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F0003".
            - The message in the linter message should
                indicate a missing operator between term and search field.
            - The position in the linter message should be (5, 10).
        """
        parser = WOSParser("term1 au=")
        parser.tokenize()
        linter = QueryLinter(parser)
        linter.check_order_of_tokens()
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F1004",
                "is_fatal": True,
                "details": "",
                "label": "invalid-token-sequence",
                "message": "The sequence of tokens is invalid.",
                "position": (6, 9),
            },
        )

    def test_near_distance_within_range(self) -> None:
        """
        Test case for NEAR operator with a specified distance within the allowed range.

        This test initializes a QueryLinter object with a query string containing
        the NEAR operator with a distance within the allowed range (<= 15).
        It verifies that the linter does not detect any issues with the NEAR distance.

        Assertions:
            - The linter should not detect any NEAR distance out of range.
            - The linter messages list should be empty.
        """
        parser = WOSParser("term1 NEAR/10 term2")
        parser.tokenize()
        linter = QueryLinter(parser)
        linter.check_near_distance_in_range(1)
        self.assertEqual(len(parser.linter_messages), 0)

    def test_near_distance_out_of_range(self) -> None:
        """
        Test case for NEAR operator with a specified distance out of the allowed range.

        This test initializes a QueryLinter object with a query string containing
        the NEAR operator with a distance out of the allowed range (> 15).
        It verifies that the linter correctly identifies the NEAR distance out of range.

        Assertions:
            - The linter should detect the NEAR distance out of range.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F0006".
            - The message in the linter message should indicate NEAR operator distance out of range.
            - The position in the linter message should be (5, 13).
        """
        parser = WOSParser("term1 NEAR/20 term2")
        parser.tokenize()
        linter = QueryLinter(parser)
        linter.check_near_distance_in_range(1)
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2007",
                "is_fatal": True,
                "details": "",
                "label": "near-distance-too-large",
                "message": "NEAR distance is too large (max: 15).",
                "position": (6, 13),
            },
        )

    def test_near_without_distance(self) -> None:
        """
        Test case for NEAR operator without a specified distance.

        This test initializes a QueryLinter object with a query string containing
        the NEAR operator without a specified distance.
        It verifies that the linter does not detect any issues with the NEAR operator.

        Assertions:
            - The linter should not detect any NEAR distance out of range.
            - The linter messages list should be empty.
        """
        parser = WOSParser("term1 NEAR term2")
        parser.tokenize()
        linter = QueryLinter(parser)
        linter.check_near_distance_in_range(0)
        self.assertEqual(len(parser.linter_messages), 0)

    def test_no_unsupported_wildcards(self) -> None:
        """
        Test case for a query string with no unsupported wildcards.

        This test initializes a QueryLinter object with a query string containing
        no unsupported wildcards and verifies that the linter does not detect any issues.

        Assertions:
            - The linter should not detect any unsupported wildcards.
            - The linter messages list should be empty.
        """
        parser = WOSParser("term1 term2")
        linter = QueryLinter(parser)
        linter.check_unsupported_wildcards()
        self.assertEqual(len(parser.linter_messages), 0)

    def test_unsupported_wildcards(self) -> None:
        """
        Test case for a query string with unsupported wildcards.

        This test initializes a QueryLinter object with a query string containing
        unsupported wildcards and verifies that the linter correctly identifies the issue.

        Assertions:
            - The linter should detect unsupported wildcards.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F1001".
            - The message in the linter message should indicate unsupported wildcards.
            - The position in the linter message should be (5, 6).
        """
        parser = WOSParser("term1 !term2")
        linter = QueryLinter(parser)
        linter.check_unsupported_wildcards()
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2001",
                "label": "wildcard-unsupported",
                "message": "Unsupported wildcard in search string.",
                "is_fatal": True,
                "details": "",
                "position": (6, 7),
            },
        )

    def test_standalone_wildcard(self) -> None:
        """
        Test case for a query string with a standalone wildcard.

        This test initializes a QueryLinter object with a query string containing
        a standalone wildcard and verifies that the linter correctly identifies the issue.

        Assertions:
            - The linter should detect the standalone wildcard.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F1002".
            - The message in the linter message should indicate a standalone wildcard.
            - The position in the linter message should be (5, 6).
        """
        parser = WOSParser('term1 "?" term2')
        parser.tokenize()
        linter = QueryLinter(parser)
        linter.check_wildcards(
            Token(value='"?"', type=TokenTypes.SEARCH_TERM, position=(0, 3))
        )
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2006",
                "is_fatal": True,
                "details": "",
                "label": "wildcard-standalone",
                "message": "Wildcard cannot be standalone.",
                "position": (0, 3),
            },
        )

    def test_wildcard_within_term(self) -> None:
        """
        Test case for a query string with a wildcard within a term.

        This test initializes a QueryLinter object with a query string containing
        a wildcard within a term and verifies that the linter does not detect any issues.

        Assertions:
            - The linter should not detect any unsupported wildcards.
            - The linter messages list should be empty.
        """
        parser = WOSParser("term1 te?m2")
        linter = QueryLinter(parser)
        linter.check_unsupported_wildcards()
        self.assertEqual(len(parser.linter_messages), 0)

    def test_no_unsupported_right_hand_wildcards(self) -> None:
        """
        Test case for a query string with no unsupported right-hand wildcards.

        This test initializes a QueryLinter object with a query string containing
        no unsupported right-hand wildcards and verifies that the linter does not detect any issues.

        Assertions:
            - The linter should not detect any unsupported right-hand wildcards.
            - The linter messages list should be empty.
        """
        parser = WOSParser("term1 term2*")
        linter = QueryLinter(parser)
        linter.check_unsupported_right_hand_wildcards(
            Token(value="term2*", type=TokenTypes.SEARCH_TERM, position=(6, 7)), 5
        )
        self.assertEqual(len(parser.linter_messages), 0)

    def test_unsupported_right_hand_wildcard_after_special_character(self) -> None:
        """
        Test case for a query string with an unsupported
        right-hand wildcard after a special character.

        This test initializes a QueryLinter object with a query string containing
        an unsupported right-hand wildcard after a special character and verifies that the linter
        correctly identifies the issue.

        Assertions:
            - The linter should detect the unsupported right-hand wildcard.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F1001".
            - The message in the linter message should
                indicate unsupported wildcard after a special character.
            - The position in the linter message should be (5, 6).
        """
        parser = WOSParser("term1 term2!*")
        linter = QueryLinter(parser)
        linter.check_unsupported_right_hand_wildcards(
            Token(value="term2!*", type=TokenTypes.SEARCH_TERM, position=(6, 7)), 6
        )
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2005",
                "is_fatal": True,
                "details": "",
                "label": "wildcard-after-special-char",
                "message": "Wildcard cannot be preceded by special characters.",
                "position": (6, 7),
            },
        )

    def test_unsupported_right_hand_wildcard_with_less_than_three_characters(
        self,
    ) -> None:
        """
        Test case for a query string with an unsupported
        right-hand wildcard preceded by less than three characters.

        This test initializes a QueryLinter object with a query string containing
        an unsupported right-hand wildcard preceded by less than
        three characters and verifies that the linter
        correctly identifies the issue.

        Assertions:
            - The linter should detect the unsupported right-hand wildcard.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F1001".
            - The message in the linter message should indicate
                right-hand wildcard must be preceded by at least three characters.
            - The position in the linter message should be (0, 2).
        """
        parser = WOSParser("te*")
        linter = QueryLinter(parser)
        linter.check_unsupported_right_hand_wildcards(
            Token(value="te*", type=TokenTypes.SEARCH_TERM, position=(0, 2)), 2
        )
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2003",
                "is_fatal": True,
                "details": "",
                "label": "wildcard-right-short-length",
                "message": "Right-hand wildcard must preceded by at least three characters.",
                "position": (0, 2),
            },
        )

    def test_no_left_hand_wildcard(self) -> None:
        """
        Test case for a query string with no left-hand wildcard.

        This test initializes a QueryLinter object with a query string containing
        no left-hand wildcard and verifies that the linter does not detect any issues.

        Assertions:
            - The linter should not detect any wrong left-hand wildcard usage.
            - The linter messages list should be empty.
        """
        parser = WOSParser("term1 term2")
        linter = QueryLinter(parser)
        linter.check_format_left_hand_wildcards(
            Token(value="term2", type=TokenTypes.SEARCH_TERM, position=(6, 11))
        )
        self.assertEqual(len(parser.linter_messages), 0)

    def test_valid_left_hand_wildcard(self) -> None:
        """
        Test case for a query string with a valid left-hand wildcard.

        This test initializes a QueryLinter object with a query string containing
        a valid left-hand wildcard and verifies that the linter does not detect any issues.

        Assertions:
            - The linter should not detect any wrong left-hand wildcard usage.
            - The linter messages list should be empty.
        """
        parser = WOSParser("term1 *term2")
        linter = QueryLinter(parser)
        linter.check_format_left_hand_wildcards(
            Token(value="*term2", type=TokenTypes.SEARCH_TERM, position=(6, 12))
        )
        self.assertEqual(len(parser.linter_messages), 0)

    def test_invalid_left_hand_wildcard(self) -> None:
        """
        Test case for a query string with an invalid left-hand wildcard.

        This test initializes a QueryLinter object with a query string containing
        an invalid left-hand wildcard and verifies that the linter correctly identifies the issue.

        Assertions:
            - The linter should detect the wrong left-hand wildcard usage.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F1001".
            - The message in the linter message should indicate
                left-hand wildcard must be followed by at least three characters.
            - The position in the linter message should be (0, 2).
        """
        parser = WOSParser("*te")
        linter = QueryLinter(parser)
        linter.check_format_left_hand_wildcards(
            Token(value="*te", type=TokenTypes.SEARCH_TERM, position=(0, 2))
        )
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2004",
                "is_fatal": True,
                "details": "",
                "label": "wildcard-left-short-length",
                "message": "Left-hand wildcard must be preceded by at least three characters.",
                "position": (0, 2),
            },
        )

    def test_valid_issn_format(self) -> None:
        """
        Test case for a query string with a valid ISSN format.

        This test initializes a QueryLinter object with a query string containing
        a valid ISSN and verifies that the linter does not detect any issues.

        Assertions:
            - The linter should not detect any ISSN format issues.
            - The linter messages list should be empty.
        """
        parser = WOSParser("1234-5678")
        linter = QueryLinter(parser)
        linter.check_issn_isbn_format(
            Token(value="1234-5678", type=TokenTypes.SEARCH_TERM, position=(0, 3))
        )
        self.assertEqual(len(parser.linter_messages), 0)

    def test_invalid_issn_format(self) -> None:
        """
        Test case for a query string with an invalid ISSN format.

        This test initializes a QueryLinter object with a query string containing
        an invalid ISSN and verifies that the linter correctly identifies the issue.

        Assertions:
            - The linter should detect the ISSN format issue.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F0008".
            - The message in the linter message should indicate ISSN/ISBN format is incorrect.
            - The position in the linter message should be (0, 3).
        """
        parser = WOSParser("1234-567")
        linter = QueryLinter(parser)
        linter.check_issn_isbn_format(
            Token(value="1234-567", type=TokenTypes.SEARCH_TERM, position=(0, 3)),
        )
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2008",
                "is_fatal": True,
                "details": "",
                "label": "isbn-format-invalid",
                "message": "Invalid ISBN format.",
                "position": (0, 3),
            },
        )

    def test_valid_isbn_format(self) -> None:
        """
        Test case for a query string with a valid ISBN format.

        This test initializes a QueryLinter object with a query string containing
        a valid ISBN and verifies that the linter does not detect any issues.

        Assertions:
            - The linter should not detect any ISBN format issues.
            - The linter messages list should be empty.
        """
        parser = WOSParser("978-3-16-148410-0")
        linter = QueryLinter(parser)
        linter.check_issn_isbn_format(
            Token(
                value="978-3-16-148410-0", type=TokenTypes.SEARCH_TERM, position=(0, 3)
            ),
        )
        self.assertEqual(len(parser.linter_messages), 0)

    def test_invalid_isbn_format(self) -> None:
        """
        Test case for a query string with an invalid ISBN format.

        This test initializes a QueryLinter object with a query string containing
        an invalid ISBN and verifies that the linter correctly identifies the issue.

        Assertions:
            - The linter should detect the ISBN format issue.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F0008".
            - The message in the linter message should indicate ISSN/ISBN format is incorrect.
            - The position in the linter message should be (0, 3).
        """
        parser = WOSParser("978-3-16-148410")
        linter = QueryLinter(parser)
        linter.check_issn_isbn_format(
            Token(
                value="978-3-16-148410", type=TokenTypes.SEARCH_TERM, position=(0, 3)
            ),
        )
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2008",
                "is_fatal": True,
                "details": "",
                "label": "isbn-format-invalid",
                "message": "Invalid ISBN format.",
                "position": (0, 3),
            },
        )

    def test_valid_doi_format(self) -> None:
        """
        Test case for a query string with a valid DOI format.

        This test initializes a QueryLinter object with a query string containing
        a valid DOI and verifies that the linter does not detect any issues.

        Assertions:
            - The linter should not detect any DOI format issues.
            - The linter messages list should be empty.
        """
        parser = WOSParser("10.1000/xyz123")
        linter = QueryLinter(parser)
        linter.check_doi_format(
            Token(value="10.1000/xyz123", type=TokenTypes.SEARCH_TERM, position=(0, 3)),
        )
        self.assertEqual(len(parser.linter_messages), 0)

    def test_invalid_doi_format(self) -> None:
        """
        Test case for a query string with an invalid DOI format.

        This test initializes a QueryLinter object with a query string containing
        an invalid DOI and verifies that the linter correctly identifies the issue.

        Assertions:
            - The linter should detect the DOI format issue.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F0008".
            - The message in the linter message should indicate DOI format is incorrect.
            - The position in the linter message should be (0, 3).
        """
        parser = WOSParser("12.1000/xyz")
        linter = QueryLinter(parser)
        linter.check_doi_format(
            Token(value="12.1000/xyz", type=TokenTypes.SEARCH_TERM, position=(0, 3)),
        )
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2009",
                "is_fatal": True,
                "details": "",
                "label": "doi-format-invalid",
                "message": "Invalid DOI format.",
                "position": (0, 3),
            },
        )

    def test_handle_multiple_same_level_operators_change(self) -> None:
        """
        Test the handle_multiple_same_level_operators method of the QueryLinter class.

        This test checks if the linter correctly identifies and handles multiple operators
        at the same level in a query string. It verifies that the linter sets the
        multiple_same_level_operators attribute to True and adds the appropriate message
        to the linter_messages list.

        The test uses the following tokens:
        - ("term1", (0, 5))
        - ("AND", (5, 8))
        - ("term2", (8, 13))
        - ("OR", (13, 15))
        - ("term3", (15, 20))

        The expected linter message is:
        - rule: "F0007"
        - message: "The operator changed at the same level. Please introduce parentheses."
        - position: (13, 15)
        """

        tokens = [
            Token(value="term1", type=TokenTypes.SEARCH_TERM, position=(0, 5)),
            Token(value="AND", type=TokenTypes.LOGIC_OPERATOR, position=(5, 8)),
            Token(value="term2", type=TokenTypes.SEARCH_TERM, position=(8, 13)),
            Token(value="OR", type=TokenTypes.LOGIC_OPERATOR, position=(13, 15)),
            Token(value="term3", type=TokenTypes.SEARCH_TERM, position=(15, 20)),
        ]
        parser = WOSParser("term1 AND term2 OR term3")
        linter = QueryLinter(parser)
        linter.handle_multiple_same_level_operators(tokens, 0)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "W0007",
                "is_fatal": False,
                "details": "",
                "label": "implicit-precedence",
                "message": "Operator changed at the same level (currently relying on implicit operator precedence, explicit parentheses are recommended)",
                "position": (13, 15),
            },
        )

    def test_handle_multiple_same_level_operators_issue(self) -> None:
        """
        Test case for handle_multiple_same_level_operators with issues.

        This test initializes a QueryLinter object with a query string containing
        multiple operators at the same level with issues. It verifies that the linter
        correctly identifies the issue with the operators.

        Assertions:
            - The linter should detect issues with the operators.
            - The linter messages list should contain exactly one message.
            - The rule in the linter message should be "F0007".
            - The message in the linter message should indicate operator change at the same level.
            - The position in the linter message should be (13, 17).
        """
        tokens = [
            Token(value="term1", type=TokenTypes.SEARCH_TERM, position=(0, 5)),
            Token(value="AND", type=TokenTypes.LOGIC_OPERATOR, position=(5, 8)),
            Token(value="term2", type=TokenTypes.SEARCH_TERM, position=(8, 13)),
            Token(value="NEAR", type=TokenTypes.LOGIC_OPERATOR, position=(13, 17)),
            Token(value="term3", type=TokenTypes.SEARCH_TERM, position=(17, 22)),
        ]
        parser = WOSParser("term1 AND term2 NEAR term3")
        linter = QueryLinter(parser)
        linter.handle_multiple_same_level_operators(tokens, 0)
        self.assertEqual(len(parser.linter_messages), 1)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "W0007",
                "is_fatal": False,
                "details": "",
                "label": "implicit-precedence",
                "message": "Operator changed at the same level (currently relying on implicit operator precedence, explicit parentheses are recommended)",
                "position": (13, 17),
            },
        )

    def test_handle_multiple_same_level_operators_nested_no_issue(self) -> None:
        """
        Test case for handling multiple same level operators
        within nested parentheses without any issues.

        This test verifies that the QueryLinter correctly
        handles a query with multiple same level operators
        (AND, OR) nested within parentheses and does not flag any issues.

        Steps:
        1. Define a list of tokens representing the query "term1 AND (term2 OR term3)".
        2. Initialize the QueryLinter with the query and an empty list for linter messages.
        3. Call the handle_multiple_same_level_operators method on the linter instance.
        4. Assert that the linter does not flag multiple same level operators.
        5. Assert that no linter messages are generated.

        Assertions:
        - linter.multiple_same_level_operators should be False.
        - len(self.linter_messages) should be 0.
        """

        tokens = [
            Token(value="term1", type=TokenTypes.SEARCH_TERM, position=(0, 5)),
            Token(value="AND", type=TokenTypes.LOGIC_OPERATOR, position=(5, 8)),
            Token(value="(", type=TokenTypes.PARENTHESIS_OPEN, position=(8, 9)),
            Token(value="term2", type=TokenTypes.SEARCH_TERM, position=(9, 14)),
            Token(value="OR", type=TokenTypes.LOGIC_OPERATOR, position=(14, 16)),
            Token(value="term3", type=TokenTypes.SEARCH_TERM, position=(16, 21)),
            Token(value=")", type=TokenTypes.PARENTHESIS_CLOSED, position=(21, 22)),
        ]
        parser = WOSParser("term1 AND (term2 OR term3)")
        linter = QueryLinter(parser)
        linter.handle_multiple_same_level_operators(tokens, 0)
        self.assertEqual(len(parser.linter_messages), 0)

    def test_handle_multiple_same_level_operators_with_near(self) -> None:
        """
        Test the handling of multiple same-level operators with the 'NEAR' operator.

        This test checks if the QueryLinter correctly identifies and handles the
        presence of multiple same-level operators, specifically when 'NEAR' and 'AND'
        operators are used in the query. It verifies that the linter sets the
        `multiple_same_level_operators` flag and adds the appropriate message to
        `linter_messages`.

        The test uses the following tokens:
        - ("term1", (0, 5))
        - ("NEAR/5", (5, 11))
        - ("term2", (11, 16))
        - ("AND", (16, 19))
        - ("term3", (19, 24))

        Assertions:
        - `linter.multiple_same_level_operators` is set to True.
        - The first message in `linter_messages` has:
          - 'rule' set to "F0007".
          - 'message' set to "The operator changed at the same level. Please introduce parentheses."
          - 'position' set to (16, 19).
        """

        tokens = [
            Token(value="term1", type=TokenTypes.SEARCH_TERM, position=(0, 5)),
            Token(value="NEAR/5", type=TokenTypes.LOGIC_OPERATOR, position=(5, 11)),
            Token(value="term2", type=TokenTypes.SEARCH_TERM, position=(11, 16)),
            Token(value="AND", type=TokenTypes.LOGIC_OPERATOR, position=(16, 19)),
            Token(value="term3", type=TokenTypes.SEARCH_TERM, position=(19, 24)),
        ]
        parser = WOSParser("term1 NEAR/5 term2 AND term3")
        linter = QueryLinter(parser)
        linter.handle_multiple_same_level_operators(tokens, 0)
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "W0007",
                "is_fatal": False,
                "details": "",
                "label": "implicit-precedence",
                "message": "Operator changed at the same level (currently relying on implicit operator precedence, explicit parentheses are recommended)",
                "position": (16, 19),
            },
        )

    def test_handle_near_without_distance(self) -> None:
        """
        Test case for handling the NEAR operator without a specified distance.
        """

        parser = WOSParser("term1 NEAR term2")
        parser.tokenize()
        linter = QueryLinter(parser)

        linter.check_implicit_near()
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "W0006",
                "is_fatal": False,
                "details": "",
                "label": "implicit-near-value",
                "message": "The value of NEAR operator is implicit",
                "position": (6, 10),
            },
        )
        self.assertEqual(parser.tokens[1].value, "NEAR/15")

    def test_handle_operator_lowercase(self) -> None:
        """
        Test case for handling lowercase operators in the query string.
        """

        parser = WOSParser("term1 and term2")
        parser.tokenize()
        linter = QueryLinter(parser)

        linter.check_operator_capitalization()
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "W0005",
                "is_fatal": False,
                "details": "",
                "label": "operator-capitalization",
                "message": "Operators should be capitalized",
                "position": (6, 9),
            },
        )
        self.assertEqual(parser.tokens[1].value, "AND")

    def test_year_format(self) -> None:
        """
        Test case for checking the year format in the query string.
        """

        parser = WOSParser("term1 and PY=202*")
        parser.tokenize()
        linter = QueryLinter(parser)

        linter.check_year_format()
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2002",
                "is_fatal": True,
                "details": "",
                "label": "wildcard-in-year",
                "message": "Wildcard characters (*, ?, $) not supported in year search.",
                "position": (13, 17),
            },
        )

    def test_invalid_field(self) -> None:
        """
        Test invalid field in the query string.
        """

        parser = WOSParser("term1 and IY=digital")
        parser.tokenize()
        linter = QueryLinter(parser)

        linter.check_fields()
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2011",
                "label": "search-field-unsupported",
                "message": "Search field is not supported for this database",
                "is_fatal": True,
                "details": "",
                "position": (10, 13),
            },
        )

    def test_year_span_violation(self) -> None:
        """
        Test case for checking the year span violation in the query string.
        """

        parser = WOSParser("term1 and PY=1900-2000")
        parser.tokenize()
        linter = QueryLinter(parser)

        linter.check_year_format()
        self.assertEqual(
            parser.linter_messages[0],
            {
                "code": "F2010",
                "is_fatal": True,
                "details": "",
                "label": "year-span-violation",
                "message": "Year span must be five or less.",
                "position": (13, 22),
            },
        )
        self.assertEqual(parser.tokens[3].value, "1995-2000")

    def test_check_search_fields_from_json_with_non_matching_field(self) -> None:
        """
        Test the `check_search_fields_from_json` method with a non-matching search field.

        This test verifies that the `check_search_fields_from_json` method correctly identifies
        a search field that does not match any of the search
        fields from JSON and adds a linter message.
        """
        parser = WOSParser("TI=digital", search_field_general="AB=")
        parser.tokenize()
        linter = QueryLinter(parser)
        linter.check_search_fields_from_json()
        self.assertIn(
            {
                "code": "E0002",
                "label": "search-field-contradiction",
                "message": "Contradictory search fields specified",
                "is_fatal": False,
                "details": "",
                "position": (0, 3),
            },
            parser.linter_messages,
        )


if __name__ == "__main__":
    unittest.main()

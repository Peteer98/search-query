#!/usr/bin/env python3
"""Web-of-Science query linter."""

import re

from search_query.constants import WOSRegex
# vielleichtr regex in constants.py packen und dann jeweil importieren?

class QueryLinter:
    """Linter for wos query"""

    language_list = ["LA=", "Languages", "la=", "language=", "la", "language", "LA", "LANGUAGE"]

    def __init__(self, search_str: str, linter_messages: dict):
        self.search_str = search_str
        self.linter_messages = linter_messages

    def pre_linting(self, tokens: list) -> bool:
        """Performs a pre-linting"""
        index = 0
        out_of_order = False
        near_operator_without_distance = False
        year_without_other_search_fields = False
        year_search_field_detected = False
        count_search_fields = 0

        while index < len(tokens) - 1:
            token, span = tokens[index]
            if self._check_order_of_tokens(tokens, token, span, index):
                out_of_order = True

            if "NEAR" in token:
                if self._check_near_distance_in_range(tokens, index):
                    near_operator_without_distance = True

            if re.match(WOSRegex.YEAR_REGEX, token):
                year_search_field_detected = True

            if re.match(WOSRegex.SEARCH_FIELD_REGEX, token):
                count_search_fields += 1

            index += 1

        if year_search_field_detected and count_search_fields < 2:
            # Year detected without other search fields
            year_without_other_search_fields = True
            self.linter_messages.append({
                "rule": "YearWithoutSearchField",
                "message": "Year detected without other search parameter.",
                "position": span,
            })

        # return True if any of the checks failed
        return (self._check_unmatched_parentheses()
                or out_of_order
                or near_operator_without_distance
                or year_without_other_search_fields)

    def _check_unmatched_parentheses(self) -> bool:
        """Check for unmatched parentheses in the query."""
        unmatched_parentheses  = False
        stack = []
        for i, char in enumerate(self.search_str):
            if char == "(":
                stack.append(i)
            elif char == ")":
                if stack:
                    stack.pop()
                else:
                    unmatched_parentheses = True
                    self.linter_messages.append({
                        "rule": "UnmatchedParenthesis",
                        "message": "Unmatched closing parenthesis ')'.",
                        "position": (i, i+1)
                    })

        for unmatched_index in stack:
            unmatched_parentheses = True
            self.linter_messages.append({
                "rule": "UnmatchedParenthesis",
                "message": "Unmatched opening parenthesis '('.",
                "position": (unmatched_index, unmatched_index+1)
            })

        return unmatched_parentheses

    def _check_order_of_tokens(self, tokens, token, span, index) -> bool:
        missplaced_order = False
        # Check for two operators in a row
        if (
            re.match(WOSRegex.OPERATOR_REGEX, token) and
            re.match(WOSRegex.OPERATOR_REGEX, tokens[index+1][0])
        ):
            self.linter_messages.append({
                "rule": "TwoOperatorInRow",
                "message": "Two operators in a row.",
                "position": tokens[index+1][1]
            })
            missplaced_order = True

        #Check for two search fields in a row
        if (
            re.match(WOSRegex.SEARCH_FIELD_REGEX, token) and
            re.match(WOSRegex.SEARCH_FIELD_REGEX, tokens[index+1][0])
        ):
            self.linter_messages.append({
                "rule": "TwoSearchFieldsInRow",
                "message": "Two Search Fields in a row.",
                "position": tokens[index+1][1]
            })
            missplaced_order = True

        # Check for opening parenthesis after term
        if (
            (
                not re.match(WOSRegex.SEARCH_FIELD_REGEX, token) and
                not re.match(WOSRegex.OPERATOR_REGEX, token.upper()) and
                not re.match(WOSRegex.PARENTHESIS_REGEX, token) and
                re.match(WOSRegex.TERM_REGEX, token)
            ) and
                (tokens[index+1][0] == "("
            ) and
                not (tokens[index-1][0].upper() == "NEAR")
        ):
            self.linter_messages.append({
                "rule": "ParenthesisAfterTerm",
                "message": "Missing Operator between term and parenthesis.",
                "position": span
            })
            missplaced_order = True

        # Check for closing parenthesis after term
        if (
            (token == ")") and
                (
                    not re.match(WOSRegex.SEARCH_FIELD_REGEX, tokens[index+1][0]) and
                    not re.match(WOSRegex.OPERATOR_REGEX, tokens[index+1][0].upper()) and
                    not re.match(WOSRegex.PARENTHESIS_REGEX, tokens[index+1][0]) and
                    not tokens[index+1][0] in self.language_list and
                    re.match(WOSRegex.TERM_REGEX, tokens[index+1][0])
                )
            ):
            self.linter_messages.append({
                "rule": "ParenthesisBeforeTerm",
                "message": "Missing Operator between term and parenthesis.",
                "position": tokens[index+1][1]
            })
            missplaced_order = True

        # Check for opening parenthesis after closing parenthesis
        if (
            (token == ")") and
                (tokens[index+1][0] == "(")
            ):
            self.linter_messages.append({
                "rule": "MissingOperatorBetweenParenthesis",
                "message": "Missing Operator between closing and opening parenthesis.",
                "position": span
            })
            missplaced_order = True

        # Check for search field after term
        if (
            (
                not re.match(WOSRegex.SEARCH_FIELD_REGEX, token) and
                not re.match(WOSRegex.OPERATOR_REGEX, token.upper()) and
                not re.match(WOSRegex.PARENTHESIS_REGEX, token) and
                re.match(WOSRegex.TERM_REGEX, token)
            ) and
                re.match(WOSRegex.SEARCH_FIELD_REGEX, tokens[index+1][0])
            ):
            self.linter_messages.append({
                "rule": "SearchFieldAfterTerm",
                "message": "Missing Operator between term and search field.",
                "position": span
            })
            missplaced_order = True

        return missplaced_order

    def _check_near_distance_in_range(self, tokens: list, index: int) -> bool:
        """Check for NEAR with a specified distance out of range."""
        near_distance = re.findall(r'\d{1,2}', tokens[index][0])
        near_distance_out_of_range = False
        if near_distance and int(near_distance[0]) > 15:
            near_distance_out_of_range = True
            self.linter_messages.append({
                "rule": "NearDistanceOutOfRange",
                "message": "NEAR operator distance out of range (max. 15).",
                "position": tokens[index][1]
            })

        return near_distance_out_of_range

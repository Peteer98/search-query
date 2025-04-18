#!/usr/bin/env python
"""Tests for search query translation"""
import unittest

from search_query.and_query import AndQuery
from search_query.constants import Fields
from search_query.not_query import NotQuery
from search_query.or_query import OrQuery
from search_query.query import Query
from search_query.query import SearchField

# pylint: disable=line-too-long
# flake8: noqa: E501


class TestQuery(unittest.TestCase):
    """Testing class for query translator"""

    def setUp(self) -> None:
        self.test_node = Query(
            "testvalue", position=(1, 10), search_field=SearchField(Fields.TITLE)
        )
        self.query_robot = NotQuery(["robot*"], search_field=SearchField(Fields.TITLE))
        self.query_ai = OrQuery(
            [
                '"AI"',
                '"Artificial Intelligence"',
                '"Machine Learning"',
                self.query_robot,
            ],
            search_field=SearchField(
                Fields.TITLE,
            ),
        )
        self.query_health = OrQuery(
            ['"health care"', "medicine"],
            search_field=SearchField(Fields.TITLE),
        )
        self.query_ethics = OrQuery(
            ["ethic*", "moral*"], search_field=SearchField(Fields.ABSTRACT)
        )
        self.query_complete = AndQuery(
            [self.query_ai, self.query_health, self.query_ethics],
            search_field=SearchField(Fields.TITLE),
        )

    def test_print_node(self) -> None:
        expected = "value: testvalue operator: False search field: ti"
        self.assertEqual(
            self.test_node.print_node(), expected, "Print Node Method does not work."
        )

    def test_append_children(self) -> None:
        """test whether the children are appended correctly"""
        healthCareChild = Query('"health care"', search_field=SearchField(Fields.TITLE))
        medicineChild = Query("medicine", search_field=SearchField(Fields.TITLE))
        expected = [healthCareChild, medicineChild]
        self.assertEqual(
            self.query_health.children[0].print_node(),
            expected[0].print_node(),
            "Children were appended incorrectly!",
        )
        self.assertEqual(
            self.query_health.children[1].print_node(),
            expected[1].print_node(),
            "Children were appended incorrectly!",
        )

    def test_or_query(self) -> None:
        """test whether OR node is created correctly"""
        expected = Query("OR", operator=True, search_field=SearchField(Fields.TITLE))
        self.assertEqual(
            self.query_ai.print_node(),
            expected.print_node(),
            "OR root was not created correctly!",
        )

    def test_and_query(self) -> None:
        """test whether AND node is created correctly"""
        expected = Query("AND", operator=True, search_field=SearchField(Fields.TITLE))
        self.assertEqual(
            self.query_complete.print_node(),
            expected.print_node(),
            "AND root was not created correctly!",
        )

    def test_not_query(self) -> None:
        """test whether NOT node is created correctly"""
        expected = Query("NOT", operator=True, search_field=SearchField(Fields.TITLE))
        self.assertEqual(
            self.query_robot.print_node(),
            expected.print_node(),
            "NOT root was not created correctly!",
        )

    def test_nested_queries(self) -> None:
        """test whether roots of nested Queries are appended as children"""
        self.assertListEqual(
            self.query_complete.children,
            [
                self.query_ai,
                self.query_health,
                self.query_ethics,
            ],
            "Nested Queries were not appended correctly!",
        )

    def test_translation_wos_part(self) -> None:
        """test whether the translation of the tool is identical to the manually translated WoS Query
        testing only a simple tree with 1 level"""

        expected = 'TI=("health care" OR medicine)'
        self.assertEqual(
            self.query_health.to_string(syntax="wos"),
            expected,
            "Health Query was not translated to Web of Science Syntax",
        )

    def test_translation_wos_complete(self) -> None:
        """test whether the translation of the tool is identical to the manually translated WoS Query,
        testing the complete, multi-level Query"""
        expected = '(TI=("AI" OR "Artificial Intelligence" OR "Machine Learning" NOT robot*) AND TI=("health care" OR medicine) AND AB=(ethic* OR moral*))'
        self.assertEqual(
            self.query_complete.to_string(syntax="wos"),
            expected,
            "Complete Query was not translated to Web of Science Syntax",
        )

    def test_translation_pubmed_part(self) -> None:
        """test whether the translation of the tool is identical to the manually translated IEEE Query,
        testing only a simple tree with 1 level"""

        expected = '("health care"[ti] OR medicine[ti])'
        self.assertEqual(
            self.query_health.to_string(syntax="pubmed"),
            expected,
            "Health Query was not translated to PubMed Syntax",
        )

    def test_translation_pubmed_complete(self) -> None:
        """test whether the translation of the tool is identical to the manually translated IEEE Query,
        testing the complete, multi-level Query"""

        expected = '(("AI"[ti] OR "Artificial Intelligence"[ti] OR "Machine Learning"[ti] NOT robot*[ti]) AND ("health care"[ti] OR medicine[ti]) AND (ethic*[ab] OR moral*[ab]))'
        self.assertEqual(
            self.query_complete.to_string(syntax="pubmed"),
            expected,
            "Query was not translated to PubMed Syntax",
        )

    def test_invalid_tree_structure(self) -> None:
        """test wheter an invalid Query (which includes a cycle), correctly raises an exception"""
        with self.assertRaises(ValueError):
            AndQuery(
                ["invalid", self.query_complete, self.query_ai],
                search_field=SearchField("Author Keywords"),
            )

    def test_selects(self) -> None:
        """Test whether the 'selects' method correctly evaluates records."""

        record_1 = {
            "title": "Artificial Intelligence in Health Care",
            "abstract": "This study explores the role of AI and machine learning in improving health outcomes.",
        }

        record_2 = {
            "title": "Moral Implications of Artificial Intelligence",
            "abstract": "Examines ethical concerns in AI development.",
        }

        record_3 = {
            "title": "Unrelated Title",
            "abstract": "This abstract is about something else entirely.",
        }

        record_4 = {
            "title": "Title with AI and medicine",
            "abstract": "abstract containing ethics.",
        }

        self.assertTrue(
            self.query_ai.selects(record_dict=record_1),
            "Query should select record_1 based on title match.",
        )
        self.assertFalse(
            self.query_health.selects(record_dict=record_2),
            "Query should not select record_2 as it doesn't match health-related keywords.",
        )
        self.assertFalse(
            self.query_health.selects(record_dict=record_3),
            "Query should not select record_3 as it has no matching keywords.",
        )

        self.assertTrue(
            self.query_complete.selects(record_dict=record_4),
            "Query should select record_4 as it matches AI, health, and ethics conditions.",
        )
        self.assertFalse(
            self.query_complete.selects(record_dict=record_3),
            "Query should not select record_3 as it doesn't meet any conditions.",
        )


if __name__ == "__main__":
    unittest.main()

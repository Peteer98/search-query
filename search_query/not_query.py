#!/usr/bin/env python
"""NOT Query"""
import typing

from search_query.constants import Operators
from search_query.query import Query
from search_query.query import SearchField

# pylint: disable=duplicate-code


class NotQuery(Query):
    """NOT Query"""

    def __init__(
        self,
        children: typing.List[typing.Union[str, Query]],
        *,
        search_field: typing.Union[SearchField, str],
        position: typing.Optional[tuple] = None,
    ) -> None:
        """init method
        search terms: strings which you want to include in the search query
        nested queries: queries whose roots are appended to the query
        search field: search field to which the query should be applied
        """

        super().__init__(
            value=Operators.NOT,
            operator=True,
            children=children,
            search_field=search_field
            if isinstance(search_field, SearchField)
            else SearchField(search_field),
            position=position,
        )

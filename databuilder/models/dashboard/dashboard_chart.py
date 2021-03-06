import logging

from typing import Optional, Dict, Any, Union, Iterator  # noqa: F401

from databuilder.models.dashboard.dashboard_query import DashboardQuery
from databuilder.models.neo4j_csv_serde import (
    Neo4jCsvSerializable, NODE_LABEL, NODE_KEY, RELATION_START_KEY, RELATION_END_KEY, RELATION_START_LABEL,
    RELATION_END_LABEL, RELATION_TYPE, RELATION_REVERSE_TYPE)

LOGGER = logging.getLogger(__name__)


class DashboardChart(Neo4jCsvSerializable):
    """
    A model that encapsulate Dashboard's charts
    """
    DASHBOARD_CHART_LABEL = 'Chart'
    DASHBOARD_CHART_KEY_FORMAT = '{product}_dashboard://{cluster}.{dashboard_group_id}/' \
                                 '{dashboard_id}/query/{query_id}/chart/{chart_id}'
    CHART_RELATION_TYPE = 'HAS_CHART'
    CHART_REVERSE_RELATION_TYPE = 'CHART_OF'

    def __init__(self,
                 dashboard_group_id,  # type: Optional[str]
                 dashboard_id,  # type: Optional[str]
                 query_id,  # type: str
                 chart_id,  # type: str
                 chart_name=None,  # type: Optional[str]
                 chart_type=None,  # type: Optional[str]
                 chart_url=None,  # type: Optional[str]
                 product='',  # type: Optional[str]
                 cluster='gold',  # type: str
                 **kwargs
                 ):
        self._dashboard_group_id = dashboard_group_id
        self._dashboard_id = dashboard_id
        self._query_id = query_id
        self._chart_id = chart_id if chart_id else chart_name
        self._chart_name = chart_name
        self._chart_type = chart_type
        self._chart_url = chart_url
        self._product = product
        self._cluster = cluster
        self._node_iterator = self._create_node_iterator()
        self._relation_iterator = self._create_relation_iterator()

    def create_next_node(self):
        # type: () -> Union[Dict[str, Any], None]
        try:
            return next(self._node_iterator)
        except StopIteration:
            return None

    def _create_node_iterator(self):  # noqa: C901
        # type: () -> Iterator[[Dict[str, Any]]]
        node = {
            NODE_LABEL: DashboardChart.DASHBOARD_CHART_LABEL,
            NODE_KEY: self._get_chart_node_key(),
            'id': self._chart_id
        }

        if self._chart_name:
            node['name'] = self._chart_name

        if self._chart_type:
            node['type'] = self._chart_type

        if self._chart_url:
            node['url'] = self._chart_url

        yield node

    def create_next_relation(self):
        # type: () -> Union[Dict[str, Any], None]
        try:
            return next(self._relation_iterator)
        except StopIteration:
            return None

    def _create_relation_iterator(self):
        # type: () -> Iterator[[Dict[str, Any]]]
        yield {
            RELATION_START_LABEL: DashboardQuery.DASHBOARD_QUERY_LABEL,
            RELATION_END_LABEL: DashboardChart.DASHBOARD_CHART_LABEL,
            RELATION_START_KEY: DashboardQuery.DASHBOARD_QUERY_KEY_FORMAT.format(
                product=self._product,
                cluster=self._cluster,
                dashboard_group_id=self._dashboard_group_id,
                dashboard_id=self._dashboard_id,
                query_id=self._query_id
            ),
            RELATION_END_KEY: self._get_chart_node_key(),
            RELATION_TYPE: DashboardChart.CHART_RELATION_TYPE,
            RELATION_REVERSE_TYPE: DashboardChart.CHART_REVERSE_RELATION_TYPE
        }

    def _get_chart_node_key(self):
        return DashboardChart.DASHBOARD_CHART_KEY_FORMAT.format(
            product=self._product,
            cluster=self._cluster,
            dashboard_group_id=self._dashboard_group_id,
            dashboard_id=self._dashboard_id,
            query_id=self._query_id,
            chart_id=self._chart_id
        )

    def __repr__(self):
        return 'DashboardChart({!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r}, {!r})'.format(
            self._dashboard_group_id,
            self._dashboard_id,
            self._query_id,
            self._chart_id,
            self._chart_name,
            self._chart_type,
            self._chart_url,
            self._product,
            self._cluster
        )

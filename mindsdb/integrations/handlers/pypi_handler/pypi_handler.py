from types import ModuleType

import pypistats
from mindsdb_sql import parse_sql

from mindsdb.integrations.handlers.pypi_handler.pypi_tables import (
    PyPIOverallTable,
    PyPIPythonMajorTable,
    PyPIPythonMinorTable,
    PyPIRecentTable,
    PyPISystemTable,
)
from mindsdb.integrations.libs.api_handler import APIHandler
from mindsdb.integrations.libs.response import HandlerStatusResponse as StatusResponse


class PyPIHandler(APIHandler):
    def __init__(self, name: str, **kwargs) -> None:
        """initializer method

        Args:
            name (str): handler's name
        """
        super().__init__(name)

        self.connection = None

        _tables = [
            PyPIOverallTable,
            PyPIPythonMajorTable,
            PyPIPythonMinorTable,
            PyPIRecentTable,
            PyPISystemTable,
        ]

        for Table in _tables:
            self._register_table(Table.name, Table(self))

    def check_connection(self):
        return StatusResponse(True)

    def connect(self) -> ModuleType:
        self.connection = pypistats
        return self.connection

    def native_query(self, query: str) -> StatusResponse:
        """Receive and process a raw query.

        Parameters
        ----------
        query : str
            query in a native format

        Returns
        -------
        StatusResponse
            Request status
        """
        ast = parse_sql(query, dialect="mindsdb")
        return self.query(ast)

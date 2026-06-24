import unittest
from unittest.mock import patch, MagicMock
from database.db_handler import get_saved_location, log_route, get_db_connection

class TestDataBaseHandler(unittest.TestCase)
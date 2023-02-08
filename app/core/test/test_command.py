# Test for the custom management command "wait_for_db"

from unittest.mock import patch
from psycopg2 import OperationalError as PG2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch("core.management.commands.wait_for_db.Command.check")
class Wait_For_Db_Test(SimpleTestCase):

    def wait_for_db_reday(self, patched_check):
        #Test if Db is ready
        patched_check.return_value = True

        call_command('wait_for_db')
        patched_check.assert_called_once_with(datase=['default'])
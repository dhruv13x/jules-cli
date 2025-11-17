# tests/test_db.py


import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import os
from pathlib import Path

from src.jules_cli.db import get_db_path, init_db, add_history_record
from src.jules_cli.commands.history import cmd_history_list, cmd_history_view
from src.jules_cli.state import _state

class TestDB(unittest.TestCase):

    def setUp(self):
        # Use a temporary database for testing
        self.test_db_path = Path('./test_history.db')
        _state["session_id"] = "test_session_id"
        self.db_patcher = patch('src.jules_cli.db.get_db_path', return_value=self.test_db_path)
        self.history_patcher = patch('src.jules_cli.commands.history.get_db_path', return_value=self.test_db_path)
        self.db_patcher.start()
        self.history_patcher.start()

    def tearDown(self):
        self.db_patcher.stop()
        self.history_patcher.stop()
        if self.test_db_path.exists():
            os.remove(self.test_db_path)

    def test_01_init_db(self):
        """Test that the database is initialized correctly."""
        init_db()
        self.assertTrue(self.test_db_path.exists())
        con = sqlite3.connect(self.test_db_path)
        cur = con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='history'")
        self.assertIsNotNone(cur.fetchone())
        con.close()

    def test_02_add_history_record(self):
        """Test that a history record is added correctly."""
        init_db()
        add_history_record(session_id="test_session", prompt="test prompt", status="test_status")
        con = sqlite3.connect(self.test_db_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM history WHERE session_id = 'test_session'")
        row = cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "test_session")
        self.assertEqual(row[2], "test prompt")
        self.assertEqual(row[5], "test_status")
        con.close()

    @patch('src.jules_cli.commands.history.logger')
    def test_03_cmd_history_list(self, mock_logger):
        """Test that the history list command works."""
        init_db()
        add_history_record(session_id="test_session_1", prompt="prompt 1", status="status 1")
        add_history_record(session_id="test_session_2", prompt="prompt 2", status="status 2")
        cmd_history_list()
        self.assertEqual(mock_logger.info.call_count, 2)

        # Check that both sessions are in the output, without relying on order
        logged_sessions = [call.args[1] for call in mock_logger.info.call_args_list]
        self.assertIn("test_session_1", logged_sessions)
        self.assertIn("test_session_2", logged_sessions)

    def test_04_update_history_record(self):
        """Test that a history record is updated correctly."""
        init_db()
        add_history_record(session_id="test_session_update", prompt="original prompt", status="prompted")
        add_history_record(session_id="test_session_update", patch="test patch", status="patched")
        add_history_record(session_id="test_session_update", pr_url="test_pr_url", status="pr_created")

        con = sqlite3.connect(self.test_db_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM history WHERE session_id = 'test_session_update'")
        row = cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "test_session_update")
        self.assertEqual(row[2], "original prompt")
        self.assertEqual(row[3], "test patch")
        self.assertEqual(row[4], "test_pr_url")
        self.assertEqual(row[5], "pr_created")
        con.close()

    def test_05_multiple_tasks(self):
        """Test that multiple tasks in a single session are recorded correctly."""
        init_db()
        # Task 1
        add_history_record(session_id="task_1", prompt="prompt 1", status="prompted")
        add_history_record(session_id="task_1", patch="patch 1", status="patched")

        # Task 2
        add_history_record(session_id="task_2", prompt="prompt 2", status="prompted")
        add_history_record(session_id="task_2", pr_url="pr_url 2", status="pr_created")

        con = sqlite3.connect(self.test_db_path)
        cur = con.cursor()

        # Verify Task 1
        cur.execute("SELECT * FROM history WHERE session_id = 'task_1'")
        row1 = cur.fetchone()
        self.assertIsNotNone(row1)
        self.assertEqual(row1[2], "prompt 1")
        self.assertEqual(row1[3], "patch 1")

        # Verify Task 2
        cur.execute("SELECT * FROM history WHERE session_id = 'task_2'")
        row2 = cur.fetchone()
        self.assertIsNotNone(row2)
        self.assertEqual(row2[2], "prompt 2")
        self.assertEqual(row2[4], "pr_url 2")

        con.close()

    @patch('src.jules_cli.commands.history.logger')
    def test_04_cmd_history_view(self, mock_logger):
        """Test that the history view command works."""
        init_db()
        add_history_record(session_id="test_session_view", prompt="view prompt", status="view_status")
        cmd_history_view("test_session_view")
        self.assertEqual(mock_logger.info.call_count, 6)

        all_logs = " ".join(str(call.args) for call in mock_logger.info.call_args_list)

        # Check that the session ID is in the output
        self.assertIn("test_session_view", all_logs)
        self.assertIn("view prompt", all_logs)
        self.assertIn("view_status", all_logs)


if __name__ == '__main__':
    unittest.main()

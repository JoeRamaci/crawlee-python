import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from crawlee import monitor
from crawlee.monitor import pad_date


class MonitorTests(unittest.TestCase):
    def test_format_date_time(self) -> None:
        date_object = datetime(2023, 12, 25, 14, 30, 5)
        expected = '25/12/2023 14:30:5'
        self.assertEqual(monitor.format_date_time(date_object), expected)
        date_object2 = datetime(2025, 4, 10, 10, 10, 15)
        expected = '10/4/2025 10:10:15'
        self.assertEqual(monitor.format_date_time(date_object2), expected)

    def test_bad_date_time(self) -> None:
        with self.assertRaises(ValueError):
            bad_date = datetime(-2025, 1, 23, 12, 20, 55)
            monitor.format_date_time(bad_date)
        with self.assertRaises(ValueError):
            bad_date2 = datetime(202500000, 40000, 100000, 1, 14, 32)
            monitor.format_date_time(bad_date2)

    def test_pad_date(self) -> None:
        self.assertEqual(pad_date(5, 2), '05')
        self.assertEqual(pad_date(12345, 7), '0012345')

        self.assertEqual(pad_date('5', 4), '0005')
        self.assertEqual(pad_date('Jean', 6), '00Jean')

        self.assertEqual(pad_date(123, 2), '123')
        self.assertEqual(pad_date('12345', 3), '12345')

        # edge cases
        self.assertEqual(pad_date('', 5), '00000')
        self.assertEqual(pad_date(0, 3), '000')

    @patch('crawlee.monitor.psutil.process_iter')
    def test_get_chromium_cpu_usage(self, mock_process_iter: MagicMock) -> None:
        mock_proc1 = MagicMock()
        mock_proc1.info = {'pid': 123, 'name': 'Chromium'}
        mock_proc1.cpu_percent.return_value = 12.5
        mock_proc1.pid = 123

        mock_proc2 = MagicMock()
        mock_proc2.info = {'pid': 456, 'name': 'not_chromium'}
        mock_proc2.cpu_percent.return_value = 25.0
        mock_proc2.pid = 456

        mock_proc3 = MagicMock()
        mock_proc3.info = {'pid': 789, 'name': 'chromium-helper'}
        mock_proc3.cpu_percent.return_value = 0.0
        mock_proc3.pid = 789

        mock_process_iter.return_value = [mock_proc1, mock_proc2, mock_proc3]

        dummy_stats = MagicMock()
        dummy_pool = MagicMock()
        monitor_instance = monitor.Monitor(dummy_stats, dummy_pool, None)

        result = monitor_instance._get_chromium_cpu_usage()

        self.assertIn("PID 123: 12.50% CPU", result)
        self.assertNotIn("PID 456", ''.join(result))  # Not Chromium
        self.assertNotIn("PID 789", ''.join(result))  # 0% CPU


if __name__ == '__main__':
    unittest.main()

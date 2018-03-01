from .context import aptnotes
import unittest
from tempfile import TemporaryFile


class ConnectTestSuite(unittest.TestCase):

    def test_apt_notes(self):
        # --
        reports = aptnotes.AptNotes.get_reports()
        self.assertGreater(len(reports), 10, 'Failed to get reports from gitlab.')
        # --
        test_report = reports[-1]
        self.assertEqual(test_report.__class__.__name__, 'Report', 'Incorrect object returned, expected Report.')
        # --
        self.assertEqual(len(test_report.box_shared_name), 32, 'Invalid length of Box shared name')
        # --
        self.assertEqual(test_report.box_file_id.__class__.__name__, 'int', 'Incorrect BoxId, expected integer.')
        # --
        with TemporaryFile() as tempfile:
            tempfile.write(test_report.get_file_content())
            self.assertEqual(tempfile.__class__.__name__, 'file', 'Incorrect Box download, expected file.')


if __name__ == '__main__':
    unittest.main()

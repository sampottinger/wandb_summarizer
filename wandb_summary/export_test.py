import unittest

import wandb_summary.export


class ExportTests(unittest.TestCase):

    def test_normalize_run_info(self):
        result = wandb_summary.export.normalize_run_info([{'a': 1}, {'b': 2}])
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0]['a'], 1)
        self.assertEquals(result[0]['b'], '')
        self.assertEquals(result[1]['a'], '')
        self.assertEquals(result[1]['b'], 2)

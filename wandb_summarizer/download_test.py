import unittest
import unittest.mock

import wandb_summarizer.download


class DownloadTests(unittest.TestCase):

    def setUp(self):
        self.__test_run = unittest.mock.MagicMock()
        self.__test_run.tags = ['tag1', 'tag2']
        self.__test_run.url = 'test/url'
        self.__test_run.name = 'test project'
        self.__test_run.state = 'finished'
        self.__test_run.created_at = 'creation str'
        self.__test_run.description = 'test description'
        self.__test_run.history = unittest.mock.MagicMock(return_value=[{'a': 1}, {'a': 2}])
        self.__test_run.config = {'config1': 1, 'config2': 2}

        self.__test_api = unittest.mock.MagicMock()
        self.__test_api.runs = unittest.mock.MagicMock(return_value=[self.__test_run])

        self.__test_logger = unittest.mock.MagicMock()
        self.__test_logger.debug = unittest.mock.MagicMock()

    def test_get_results(self):
        results = wandb_summarizer.download.get_results(
            'testuser/testproject',
            api=self.__test_api,
            logger=self.__test_logger
        )

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result['tags'], '["tag1", "tag2"]')
        self.assertEqual(result['url'], 'test/url')
        self.assertEqual(result['name'], 'test project')
        self.assertEqual(result['state'], 'finished')
        self.assertEqual(result['created_at'], 'creation str')
        self.assertEqual(result['description'], 'test description')
        self.assertEqual(result['end_a'], 2)
        self.assertEqual(result['config_config1'], 1)
        self.assertEqual(result['config_config2'], 2)

    def test_serialize_run(self):
        result = wandb_summarizer.download.serialize_run(self.__test_run)
        self.assertEqual(result['tags'], '["tag1", "tag2"]')
        self.assertEqual(result['url'], 'test/url')
        self.assertEqual(result['name'], 'test project')
        self.assertEqual(result['state'], 'finished')
        self.assertEqual(result['created_at'], 'creation str')
        self.assertEqual(result['description'], 'test description')
        self.assertEqual(result['end_a'], 2)
        self.assertEqual(result['config_config1'], 1)
        self.assertEqual(result['config_config2'], 2)

    def test_flatten_dict_and_add(self):
        dict_1 = {'a': 1}
        dict_2 = {'b': 2}
        wandb_summarizer.download.flatten_dict_and_add(dict_1, dict_2, 'prefix')
        self.assertEquals(dict_2['prefix_a'], 1)

    def test_is_empty_value_primitive(self):
        self.assertFalse(wandb_summarizer.download.is_empty_value(1))

    def test_is_empty_value_true_str(self):
        self.assertTrue(wandb_summarizer.download.is_empty_value(
            '{"desc":null,"value":0}'
        ))

    def test_is_empty_value_false_str(self):
        self.assertFalse(wandb_summarizer.download.is_empty_value('test'))

    def test_is_empty_value_true_dict(self):
        self.assertTrue(wandb_summarizer.download.is_empty_value(
            {'desc': None, 'value': 0}
        ))

    def test_is_empty_value_false_dict(self):
        self.assertFalse(wandb_summarizer.download.is_empty_value(
            {'desc': 'other', 'value': 0}
        ))

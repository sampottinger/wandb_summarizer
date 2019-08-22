"""Logic for downloading and serializing run results from wandb.

Logic for downloading and serializing run results from wandb, gathing information from wandb about
a run before converting that information into a flat data structure, removing information about
metrics over time and instead only reporting on the final metrics seen from a run. Released under
the MIT license (see LICENSE.md).
"""

import collections
import json

import wandb


def get_results(project_name, query_param=None, api=None, logger=None):
    """Download run information from a project given optional query parameters.

    Args:
        project_name (str): The name of the project to be downloaded. Should be of form
            username/project.
        query_param (str): The mongo-like selector to be used in filtering runs. If not provided
            or None, will download all runs.
        api (wandb.Api): The api object to use in requesting run information. If None or not
            provided, will create a new API access object using default values.
        logger (logger.Logger): The logger with which to report debug information. If None or not
            provided, no messages will be logged.
    Returns:
        List[Dict]: List of dictionaries where each dict represents a single run.
    """
    if not api:
        api = wandb.Api()

    if not query_param:
        query_param = {}

    def log(msg):
        """Log a message if a logger has been given.

        Args:
            msg (str): The message to be logged.
        """
        if logger:
            logger.debug(msg)

    log('Querying for runs')
    runs = api.runs(project_name, query_param)

    log('Downloading %d runs' % len(runs))
    run_info = list(map(serialize_run, runs))

    return run_info


def serialize_run(run):
    """Convert a run information object from wandb into a plain old dictionary.

    Args:
        run (wandb.Run): The run to be serialized into a dictionary.
    Returns:
        Dict: Serialized version of the given run with run-wide information and data from the final
            sample collected from a run.
    """
    ret_dict = {
        'tags': json.dumps(run.tags),
        'url': run.url,
        'name': run.name,
        'state': run.state,
        'created_at': run.created_at,
        'description': run.description,
    }

    if run.state == 'finished':
        run_history = run.history(pandas=False)
        if len(run_history) > 0:
            last_record = run_history[-1]
            flatten_dict_and_add(last_record, ret_dict, 'end')

    flatten_dict_and_add(run.config, ret_dict, 'config')

    return ret_dict


def flatten_dict_and_add(source_dict, target_dict, prefix):
    """Insert non-empty values from source_dict into target_dict.

    Insert non-empty values from source_dict into target_dict where target_dict is modified
    in-place.

    Args:
        source_dict (Dict): The dictionary from which new keys should be registered.
        target_dict (Dict): The dictionary into which new keys should be registered.
        prefix (str): The prefix to prepend to keys found in source_dict.
    """
    for key in source_dict:
        value = source_dict[key]
        is_empty = is_empty_value(value)
        new_key = prefix + '_' + key
        is_already_present = new_key in target_dict

        if not is_empty:
            if is_already_present:
                raise ValueError('Already saw %s in target dict.' % new_key)
            else:
                target_dict[new_key] = source_dict[key]


def is_empty_value(value):
    """Determine if a value was "empty" within wandb.

    Determine if a value was "empty" within Weights and Biases because it was not reported within a
    run or was not applicable.

    Args:
        value: The value reported by wandb.
    Returns:
        bool: True if the value is "empty" and false otherwise.
    """
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.decoder.JSONDecodeError:
            return False

    if isinstance(value, collections.Mapping):
        if 'desc' in value and 'value' in value:
            return value['desc'] == None and value['value'] == 0
        else:
            return False
    else:
        return False

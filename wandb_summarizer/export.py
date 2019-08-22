"""Simple script to generate a summary CSV across runs within a wandb project.

Build datasets as CSV files of summary information across all or many runs within a Weights and
Biases project. This can be used to summarize inputs and observations across experiments within a
project, supporting iterative model refinement or model selection. To motivate the script consider
that, for model selection, it may be useful to have a table which summarizes the results of all runs
given the parameters for that run. For example, users trying different dropout rates may be logging
those rates within Weights and Biases' config object (wandb.config). To see how that impacted
training and validation error, one would want to get the final errors across all runs versus the
dropout rates attempted.

Released under the MIT license (see LICENSE.md).
"""

import csv
import json
import logging
import sys

import wandb_summarizer.download

USAGE_STR = 'wandb-summarizer-to-csv [username/project name] [output loc] [optional verbose flag] [optional query parameters]'
MIN_NUM_ARGS = 2
MAX_NUM_ARGS = 4
TRUE_VALUES = ['y', 't', 'yes', 'true']


def normalize_run_info(run_info):
    """Normalize all dictionaries describing a run.

    Args:
        run_info (List[Dict]): The list of dictionaries to be normalized.
    Returns:
        List[Dict]: The input run_info but with each dictionary now having all the same keys. Note
            that there will be empty string values when a key was not originally found on a
            dictionary.
    """
    keys = set([])
    for run in run_info:
        keys.update(run.keys())

    def get_run_info_with_blanks(run):
        """Ensure all of the required keys are found on a single run dictionary.

        Args:
            run (Dict): The run's original dictionary.
        Returns:
            Dict: The input run dictionary with all of the required keys. Empty string values will
                be added when a required key is not present.
        """
        return dict(zip(keys, map(lambda x: run.get(x, ''), keys)))

    return list(map(get_run_info_with_blanks, run_info))


def main():
    """Main entry point for this script from the command line."""
    num_arguments_given = len(sys.argv) - 1

    invalid_args = num_arguments_given < MIN_NUM_ARGS
    invalid_args = invalid_args or num_arguments_given > MAX_NUM_ARGS

    if invalid_args:
        print(USAGE_STR)
        return

    project_name = sys.argv[1]
    output_loc = sys.argv[2]

    logger = logging.getLogger(__name__)
    if num_arguments_given > 2:
        logger_value = sys.argv[3].lower()
        use_verbose = logger_value in TRUE_VALUES
    else:
        use_verbose = True

    if use_verbose:
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    if num_arguments_given > 3:
        query_param = json.loads(sys.argv[4])
    else:
        query_param = {}

    run_info = wandb_summarizer.download.get_results(
        project_name,
        query_param=query_param,
        logger=logger
    )

    logger.debug('Normalizing')
    normalized_run_info = normalize_run_info(run_info)

    logger.debug('Saving')
    with open(output_loc, 'w') as f:
        cols = sorted(normalized_run_info[0].keys())
        writer = csv.DictWriter(f, cols)
        writer.writeheader()
        writer.writerows(normalized_run_info)


if __name__ == '__main__':
    main()

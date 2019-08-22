W&B Summary
====================================================================================================
A humble unofficial microlibrary / command line tool for summarizing data within [Weights and Biases](https://app.wandb.ai/) across runs including a tiny tool to download wandb data as a CSV file. This is not endorsed or affiliated with Weights and Biases.

<br>

Installation
----------------------------------------------------------------------------------------------------
This package is available via pip and requires Python 3. Simply run the following (optionally within a virtual environment).

```
$ pip install wandb_summary
```

<br>

Usage
----------------------------------------------------------------------------------------------------
This package is usable via the command line or from another Python script. The command line tool takes the following form:

```
$ wandb-summary-export [username/project name] [output loc] [optional verbose flag] [optional query parameters]
```

Most uses of the microlibrary from another Python script will want to use `wandb_summary.download.get_results` which takes the following parameters:

 - `project_name` (str): The name of the project to be downloaded. Should be of form username/project.
 - `query_param` (str): [The mongo-like selector](https://docs.wandb.com/docs/integrations/api.html#querying-runs) to be used in filtering runs. If not provided or None, will download all runs. Defaults to None.
 - `api` (wandb.Api): The api object to use in requesting run information. If None or not provided, will create a new API access object using default values. Defaults to None.
 - `logger` (logger.Logger): The logger with which to report debug information. If None or not provided, no messages will be logged. Defaults to None.

<br>

Purpose
----------------------------------------------------------------------------------------------------
This microlibrary builds summary datasets across all or many runs within a Weights and Biases project, reporting statistics from the end of each run as opposed to over time (over epochs) within those runs. This can be used to summarize inputs and results as a tabular data artifact across experiments within a project, supporting iterative model refinement or model selection. For example, users trying different dropout rates or L2 penalty inside a neural network for regularization may be logging those rates within Weights and Biases' config object (`wandb.config`). The wandb online interface may show those runs in a table with the final results from each but one may wish to visualize  information from that table by building a bar chart showing the final validation / training set F1 scores at different dropout rates. As there is no "export table to CSV" option within wandb, one would need to write a custom script to download this data via Python. This microlibrary / command line tool makes it easy to download those results into a flat table for that post-hoc analysis, making it easier to generate results like the following:

| L2 Penalty | Final Validation Accuracy | Final Training Accuracy |
|------------|---------------------------|-------------------------|
| 0.001      | 73%                       | 87%                     |
| 0.01       | 73%                       | 75%                     |
| 0.1        | 56%                       | 55%                     |

<br>

Examples
----------------------------------------------------------------------------------------------------
Downloading all runs from [sampottinger/who-wrote-this](https://app.wandb.ai/sampottinger/who-wrote-this) via the command line tool to a CSV file:

```
$ wandb-summary-export sampottinger/who-wrote-this who_wrote_this.csv
```

<br>

Downloading select runs from [sampottinger/who-wrote-this](https://app.wandb.ai/sampottinger/who-wrote-this) via the command line tool to a CSV file with no debug logging:

```
$ wandb-summary-export sampottinger/who-wrote-this who_wrote_this.csv f "{\"config.corpusCol\": \"description\"}"
```

<br>

Downloading run information from [sampottinger/who-wrote-this](https://app.wandb.ai/sampottinger/who-wrote-this) within another Python script:

```
import wandb_summary.download

run_info = wandb_summary.download.get_results('sampottinger/who-wrote-this')
print(run_info[0]['url'])
```

<br>

Development Standards
----------------------------------------------------------------------------------------------------
All top level methods should be unit tested and have [Google style guide conformant docstrings](http://google.github.io/styleguide/pyguide.html). Please conform to the [Google Python Style Guide](http://google.github.io/styleguide/pyguide.html) when possible.

<br>

Open Source Libraries Used
----------------------------------------------------------------------------------------------------
This uses the [wandb client](https://github.com/wandb/client) internally under the [MIT License](https://github.com/wandb/client/blob/master/LICENSE).

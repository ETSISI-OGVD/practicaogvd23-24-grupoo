# OGVD - Assignment 2

## Synapse assignment

We have prepared an EDA notebook using Spark, run on a CSV file stored in Azure.

## ML assignment

### Pipeline explanation

We have created an automatic MLOps pipeline that runs from changes in this Github repository. It has three steps:

* `data-update`. The dataset is automatically updated and cleaned. In our case, we have a static dataset, so we only clean the raw data and prepare it for training. In a real world setting it should grab new data that has been accumulating, so the model is trained on recent data and we prevent any drift.
* `model-train`. Training of a Gradient Boosting Regressor on the clean data.
* `model-deploy`. An endpoint is created or updated and the model is deployed. Although we have prepared two YAML files for these two jobs, we had trouble with a known bug for MLFLOW models. Thus, we ended up running everything from the `deploy.py` script from Github runners.

Each step has a directory, and also a Github workflow to run them. Each step is run automatically after the previous one is finished, or after its directory has been updated in the repository from a Pull Request. Further, the `data-update` action (and consequently the full pipeline) is run each Monday at night, so the model would be up to date with the current data distribution.

### Reproduction details

- Create an Azure service principal objetc and inject the credentials as a secret.
- Create the raw dataset in Azure.
- Run the worflows from Github.

## Cost report
# OGVD - Assignment 2

## Synapse assignment

We have prepared an EDA notebook using Spark, run on a CSV file stored in Azure.

## ML assignment

### Pipeline explanation

We have developed an automated MLOps pipeline that is triggered by changes in this GitHub repository. The pipeline consists of three stages:

1. `data-update`: The dataset is automatically updated and cleaned. In our particular case, we have a static dataset, so we only clean and preprocess the raw data in preparation for training. However, in a real-world setting, this stage should retrieve new data that has been accumulating, enabling the model to be trained on recent data and preventing any potential drift.
2. `model-train`: Training of a Gradient Boosting Regressor on the clean data.
3. `model-deploy`: An endpoint is created or updated, and the model is deployed. Although we have created two YAML files for these two tasks, we encountered an existing bug related to MLFLOW models. Consequently, we executed all steps from the `deploy.py` script using GitHub runners.

Each stage has a corresponding directory and GitHub workflow to execute it. The stages are run automatically after the preceding stage has finished or after its directory has been updated in the repository from a Pull Request. Furthermore, the `data-update` action (and consequently the entire pipeline) is executed every Monday night to ensure that the model remains up-to-date with the current data distribution.

### Reproduction details

- Create an Azure service principal objetc and inject the credentials as a secret.
- Create the raw dataset in Azure.
- Run the worflows from Github.

## Cost report
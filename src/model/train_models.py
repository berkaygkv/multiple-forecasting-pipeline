import papermill as pm
import os
from src import ProjectConstants
import pandas as pd


def single_train(provider: str, hyperparameter_tuning: bool = False) -> None:
    """Runs the budget.ipynb notebook for the given provider and stores the created product notebook under
    the "product/notebooks" directory

        Args:
        provider: Provider name whose modelling procedure will be run.
        hyperparameter_tuning: Boolean option whether the hyperparameter procedure will be started when building model.

        Returns: None
    """
    parameters = {
        "provider": provider,
        "hyperparameter_tuning": hyperparameter_tuning,
        "ROOT_DIR": ProjectConstants.ROOT_DIR,
    }
    pm.execute_notebook(
        "src/notebooks/budget.ipynb",
        f"product/notebooks/budget_{provider}.ipynb",
        parameters=parameters,
        request_save_on_cell_execute=False,
    )
    print("Run finished.")


def bulk_train(
    exclude_present_models: bool = False, hyperparameter_tuning: bool = False
) -> None:
    """Runs the budget.ipynb notebook for all the providers included in the dataset and stores the created product
    notebook under the "product/notebooks" directory

        Args:
        exclude_present_models: Boolean options whether the providers that has a model built under models folder, will be excluded.
        hyperparameter_tuning: Boolean option whether the hyperparameter procedure will be started when building models.

        Returns: None
    """

    # Identify the providers for which a model were built in the models folder
    excluded_list = [
        k.replace(".pkl", "") for k in os.listdir(ProjectConstants.ROOT_DIR + "/models")
    ]

    # Read the source data identify the unique providers
    dataframe = pd.read_csv(ProjectConstants.ROOT_DIR + "/" + "data/provider_data.csv")
    providers_list = dataframe.provider.unique().tolist()

    # Exclude the providers from running
    if exclude_present_models:
        providers_list = [k for k in providers_list if k not in excluded_list]

    # Loop through all the providers to create notebooks and prediction models
    for provider in providers_list:
        print(provider)
        parameters = {
            "provider": provider,
            "hyperparameter_tuning": hyperparameter_tuning,
        }
        pm.execute_notebook(
            "src/notebooks/budget.ipynb",
            f"product/notebooks/budget_{provider}.ipynb",
            parameters=parameters,
            request_save_on_cell_execute=False,
        )
        print(f"{provider} run finished.")

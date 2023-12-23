import papermill as pm
import os
import pandas as pd


cwd = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(__file__).split("/src")[0]
dataframe = pd.read_csv(ROOT_DIR + "/" + "data/provider_data.csv")
providers_list: list = dataframe.provider.unique().tolist()
drop_list = [k.replace(".pkl", "") for k in os.listdir(ROOT_DIR + "/models")]
print(drop_list)
providers_list = [k for k in providers_list if k not in drop_list]

for param in providers_list:
    print(param)
    parameters = {
    "provider": param,
    "hyperparameter_tuning": False
}
    pm.execute_notebook(
        "src/notebooks/budget.ipynb",
        f"product/notebooks/budget_{param}.ipynb",
        parameters=parameters,
        request_save_on_cell_execute=False,
    )
    print(f"{param} run finished.")
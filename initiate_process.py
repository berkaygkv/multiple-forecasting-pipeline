from src import bulk_train
from src import load_sql_data

if __name__ == "__main__":
    providers_list = ['provider_1', 'provider_2', 'provider_3', 'provider_4', 'provider_5', 'provider_6', 'provider_7', 'provider_8']
    _ = load_sql_data(inputted_providers_list=providers_list)
    _ = bulk_train(exclude_present_models=False)
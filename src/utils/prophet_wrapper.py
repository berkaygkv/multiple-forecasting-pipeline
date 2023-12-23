from fbprophet import Prophet
import yaml


class CustomProphetModel:
    """ Customized Facebook Prophet Model that is parameterized by the config file and capable of adding
    customized seasonality defined in the custom_seasonality key in the config file .
    
    Seasonality Example: 
    
    custom_seasonalities:
        seasonality_1:
        name: "weekly"
        period: 7
        fourier_order: 10
    

    Args:
        - provider_name: str = Provider name string that will be used to obtain relevant parameters in the config file.

    Returns: 
        CustomProphetModel object inherited from Prophet class.
    """

    def __new__(cls, provider_name):
        # Read predefined model_config.yaml file
        with open("config/model_config.yaml") as rd:
            conf = yaml.safe_load(rd).get(provider_name, {"custom_seasonalities": None})

        # Extract model only parameters that are accepted by Prophet Class
        model_parameters = conf.copy()
        model_parameters.pop("custom_seasonalities")
        seasonality_parameters = conf.copy()["custom_seasonalities"]
        custom_model = Prophet(**model_parameters)
        if seasonality_parameters:
            for seasonality_dict in seasonality_parameters:
                custom_model.add_seasonality(
                    **seasonality_parameters[seasonality_dict])
        return custom_model


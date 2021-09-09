import pandas as pd
import logging
from authentication import ws
from azureml.train.automl import AutoMLConfig
from azureml.train.automl.run import AutoMLRun
from azureml.automl.core.forecasting_parameters import ForecastingParameters
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig

from azureml.core import Dataset
from azureml.core.experiment import Experiment

# Prep the data
dataset_name = 'energy-train-processed'
label = 'Load'
ds = Dataset.get_by_name(workspace=ws, name=dataset_name)

# Setup the forecasting parameters
forecasting_parameters = ForecastingParameters(
    time_column_name='Date',
    forecast_horizon=4,
    target_rolling_window_size=3,
    feature_lags='auto',
    validate_parameters=True
)

# Featurization
featurization_config = FeaturizationConfig()
featurization_config.drop_columns = ['TZ', 'City', 'Code']
featurization_config.add_transformer_params('Imputer', ['Load'], {"strategy": "ffill"})

# Setup the classifier
automl_settings = {
    "task": 'forecasting',
    "primary_metric":'r2_score',
    "iteration_timeout_minutes": 10,
    "experiment_timeout_hours": 0.3,
    "featurization": featurization_config,
    "compute_target":'newcluster1',
    "max_concurrent_iterations": 4,
    "verbosity": logging.INFO,
    "training_data":ds,
    "label_column_name":label,
    "n_cross_validations": 5,
    #"blocked_models":['Prophet'],
    "enable_voting_ensemble":True,
    "enable_early_stopping": True,
    "model_explainability":True,
    #"enable_dnn":True,
    "forecasting_parameters": forecasting_parameters
        }

automl_classifier = AutoMLConfig(**automl_settings)

# Setup experiment and trigger run
experiment = Experiment(ws, name='forecasting_run_1')
remote_run = experiment.submit(automl_classifier, show_output=True, wait_post_processing=True)
remote_run.wait_for_completion()

# Run details
logging.info(f" Get best child run:\n {remote_run.get_best_child()}")
logging.info(f" Get data guardrails:\n {remote_run.get_guardrails()}")
logging.info(f" Summary of results:\n {remote_run.summary()}")
#best_run, fitted_model = run.get_output()
#logging.info(f" Get best run:\n {best_run}")
#logging.info(f" Fitted model steps:\n {fitted_model.steps}")

## Setup experiment and trigger run
#experiment = ws.experiments['Tutorial-automl']
#run = AutoMLRun(experiment, run_id="AutoML_ced4244b-545d-4200-b4f3-67fa95c7ada3")
#
#best_run = run.get_best_child()
#model_name = best_run.properties['model_name']
#description = 'Best Run to be registered'
#tags = None
#model = run.register_model(
#        model_name = model_name,
#        description= description,
#        tags=tags)
#
#print(f" model registered")

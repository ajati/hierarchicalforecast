# compute base forecast no coherent
from statsforecast.core import StatsForecast
from statsforecast.models import AutoARIMA, Naive
import pandas as pd

# obtain hierarchical reconciliation methods and evaluation
from hierarchicalforecast.core import HierarchicalReconciliation
from hierarchicalforecast.methods import BottomUp, TopDown, MiddleOut, MinTrace
from datasetsforecast.hierarchical import HierarchicalData
import numpy as np


# Load TourismSmall dataset
Y_df, S, tags = HierarchicalData.load("./data", "TourismSmall")
Y_df["ds"] = pd.to_datetime(Y_df["ds"])


# Compute base level predictions
sf = StatsForecast(
    df=Y_df, models=[AutoARIMA(season_length=12), Naive()], freq="M", n_jobs=-1
)

forecasts_df = sf.forecast(h=12)

# Reconcile the base predictions
reconcilers = [
    BottomUp(),
    TopDown(method="forecast_proportions"),
    MiddleOut(
        middle_level="Country/Purpose/State", top_down_method="forecast_proportions"
    ),
    MinTrace(method="ols"),
]

hrec = HierarchicalReconciliation(reconcilers=reconcilers)

reconciled_forecasts = hrec.reconcile(Y_hat_df=forecasts_df, Y_df=Y_df, S=S, tags=tags)


from hierarchicalforecast.core import HierarchicalEvaluation


def mse(y, y_hat):
    return np.mean((y - y_hat) ** 2)


evaluator = HierarchicalEvaluation(evaluators=[mse])
evaluator.evaluate(Y_hat_df=Y_rec_df, Y_test=Y_test_df, tags=tags, benchmark="Naive")

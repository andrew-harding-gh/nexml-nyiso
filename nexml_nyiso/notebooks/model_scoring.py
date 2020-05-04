import utils
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import DatetimeTickFormatter


def eval(df):
    """
    Evaluates model prediction DataFrame

    Parameters
    ----------
    df: DataFrame -> DataFrame with 'prediction', 'nyiso_prediction', and 'target' columns.

    Returns DataFrame and Bokeh plot for notebook use.
    """

    df.sort_index(inplace=True)
    pred_plot = figure(plot_width=1200, plot_height=600, x_axis_label='Date', y_axis_label='Usage')
    pred_plot.circle(x='date', y='target', source=df, size=10, fill_alpha=.5, legend_label='Actual')
    pred_plot.triangle(x='date', y='prediction', source=df, size=10, fill_alpha=.5, legend_label='Prediction', color='green')
    pred_plot.line(x='date', y='prediction', source=df, alpha=.5, legend_label='Prediction', color='green')
    pred_plot.square(x='date', y='nyiso_prediction', source=df, size=10, fill_alpha=.5, legend_label='NYISO Prediction', color='red')
    pred_plot.line(x='date', y='nyiso_prediction', source=df, alpha=.5, legend_label='NYISO Prediction', color='red')
    pred_plot.xaxis.formatter = DatetimeTickFormatter()

    df['prediction_error'] = df['prediction'] - df['target']
    df['nyiso_prediction_error'] = df['nyiso_prediction'] - df['target']
    total_prediction_error = df['prediction_error'].abs().sum().round()
    total_nyiso_error = df['nyiso_prediction_error'].abs().sum().round()
    closest_count = len(df[df['prediction_error'].abs() < df['nyiso_prediction_error'].abs()])
    print('Total prediction error: {e}'.format(e=total_prediction_error))
    print('Total ISOLF prediction error: {e}'.format(e=total_nyiso_error))
    print('Percentage of time the model outperformed the NYISO model: {percent} ({closer}/{total})'.format(
        percent=round(closest_count / len(df) * 100, 2),
        closer=closest_count,
        total=len(df)
    ))
    df.sort_values(by=['prediction_error'], inplace=True)

    return df, pred_plot

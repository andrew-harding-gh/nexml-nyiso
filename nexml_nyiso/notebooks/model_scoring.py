import utils
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.models.tools import HoverTool
from bokeh.io.export import get_screenshot_as_png
from bokeh.io import output_notebook


def de_process(df, mean, std):
    for col in utils.COLUMNS_TO_NORMALIZE:
        df[col] *= std[col]
        df[col] += mean[col]


def eval(model, mean, std):
    """
    Evaluates trained model.

    Parameters
    ----------
    model: Model -> Trained Keras model.
    mean: Series -> Series containing mean of columns.
    std: Series -> Series containing std of columns.

    Returns DataFrame and Bokeh plot for notebook use.
    """
    train, test = utils.load_data()
    utils.preprocess(test, mean, std)
    predictions = model.predict(test.copy().drop(columns=['target']))
    isolf = utils.isolf()
    results = test.join(isolf, how='inner')
    results['prediction'] = predictions
    results['target'] *= std.target
    results['target'] += mean.target
    results['prediction'] *= std.target
    results['prediction'] += mean.target
    results['date'] = results.index

    pred_plot = figure(plot_width=1200, plot_height=600, x_axis_label='Date', y_axis_label='Usage')
    pred_plot.circle(x='date', y='target', source=results, size=10, fill_alpha=.5, legend_label='Actual')
    pred_plot.triangle(x='date', y='prediction', source=results, size=10, fill_alpha=.5, legend_label='Prediction', color='green')
    pred_plot.line(x='date', y='prediction', source=results, alpha=.5, legend_label='Prediction', color='green')
    pred_plot.square(x='date', y='isolf_mean', source=results, size=10, fill_alpha=.5, legend_label='ISO Prediction', color='red')
    pred_plot.line(x='date', y='isolf_mean', source=results, alpha=.5, legend_label='ISO Prediction', color='red')
    pred_plot.xaxis.formatter = DatetimeTickFormatter()

    results['prediction_error'] = results['target'] - results['prediction']
    results['isolf_error'] = results['target'] - results['isolf_mean']
    total_prediction_error = results['prediction_error'].abs().sum().round()
    total_isolf_error = results['isolf_error'].abs().sum().round()
    print('Total prediction error: {e}'.format(e=total_prediction_error))
    print('Total ISOLF prediction error: {e}'.format(e=total_isolf_error))
    results = results[[
        'prediction_error',
        'isolf_error',
        'prediction',
        'isolf_mean',
        'target',
        'date',
        'PRCP',
        'TMIN',
        'TMAX',
    ]]

    return results, pred_plot

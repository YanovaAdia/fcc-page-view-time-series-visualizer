import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import calendar

register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv",
                 parse_dates=['date'], 
                 index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025))
        & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
  # Draw line plot
  fig, ax = plt.subplots(figsize=(20, 5))

  ax.plot(df, color='red')
  ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
  ax.set_xlabel('Date')
  ax.set_ylabel('Page Views')
  # Save image and return fig (don't change this part)
  fig.savefig('line_plot.png')
  return fig


def draw_bar_plot():
  # Copy and modify data for monthly bar plot

  df_bar = df.copy()
  months = list(calendar.month_name[1:])

  df_bar['year'] = df.index.year
  df_bar['month'] = df.index.month_name()

  df_bar = df_bar.groupby(['year', 'month']).value.mean()\
  .unstack(level='month')

  df_bar = df_bar[months]

  fig = df_bar.plot.bar(figsize=(7, 8)).figure

  plt.legend(title='Months')
  plt.ylabel('Average Page Views')
  plt.xlabel('Years')

  # Save image and return fig (don't change this part)
  fig.savefig('bar_plot.png')
  return fig


def draw_box_plot():
  # Prepare data for box plots (this part is done!)
  df_box = df.copy()
  df_box.reset_index(inplace=True)
  df_box['year'] = [d.year for d in df_box.date]
  df_box['month'] = [d.strftime('%b') for d in df_box.date]

  # Draw box plots (using Seaborn)
  months = list(calendar.month_name[1:])
  acr_month = []

  for i in range(0, len(months)):
    acr_month.append(months[i][:3])
  
  fig, axes = plt.subplots(1, 2, figsize=(20, 5))

  sns.boxplot(x='year', y='value', data=df_box,
              ax=axes[0]).set(title='Year-wise Box Plot (Trend)',
                              xlabel='Year',
                              ylabel='Page Views')
  sns.boxplot(x='month', y='value', data=df_box,
              ax=axes[1], order=acr_month).set(title='Month-wise Box Plot (Seasonality)',
                              xlabel='Month',
                              ylabel='Page Views')
  # Save image and return fig (don't change this part)
  fig.savefig('box_plot.png')
  return fig

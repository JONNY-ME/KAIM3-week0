import os
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

# ---------------------------------
# Data Management Functions
# ---------------------------------

def manage_data(data_path):
    """
    Ensure required data files are present. Downloads and extracts data if missing.

    Parameters:
        data_path (str): Path to the data directory.

    Returns:
        None
    """
    # Create the data directory if it doesn't exist
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # List of expected files in the data_path directory
    expected_files = [
        f'{data_path}/benin-malanville.csv',
        f'{data_path}/sierraleone-bumbuna.csv',
        f'{data_path}/togo-dapaong_qc.csv'
    ]

    # Check for missing files
    if not all([os.path.exists(f) for f in expected_files]):
        import gdown
        import zipfile

        # File URL (replace 'FILE_ID' with the actual ID from the link)
        file_url = 'https://drive.google.com/uc?id=1wRxR5CROC95Z9vPYlXwHrSGt79Of_zQU'
        destination = f'{data_path}/data.zip'

        # Download the file from Google Drive
        gdown.download(file_url, destination, quiet=True)

        # Extract the contents of the zip file
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall(data_path)

        # Remove the zip file after extraction
        os.remove(destination)

# ---------------------------------
# Data Cleaning Functions
# ---------------------------------

def clip_outliers(data, columns, valid_range):
    """
    Clip outliers in the specified columns based on the valid range.

    Parameters:
        data (DataFrame): The input dataset.
        columns (list): List of columns to check for outliers.
        valid_range (list): List of tuples specifying valid ranges (min, max) for each column.

    Returns:
        DataFrame: The dataset with outliers clipped.
    """
    for col, (min_val, max_val) in zip(columns, valid_range):
        data[col] = data[col].clip(lower=min_val, upper=max_val)
    return data

# ---------------------------------
# Visualization Functions
# ---------------------------------

def plot_time_series(data, columns, data_name='Data'):
    """
    Plot time series data for specified columns.

    Parameters:
        data (DataFrame): The dataset.
        columns (list): List of column names to plot.
        data_name (str): Name of the dataset for titles.

    Returns:
        None
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    fig.suptitle(f"{data_name} Time Series Data")
    for col in columns:
        data[col].plot(ax=axes[columns.index(col)], title=col, legend=True)

    plt.tight_layout()
    plt.show()

def plot_monthly_trends(data, columns, data_name='Data'):
    """
    Plot monthly trends for specified columns.

    Parameters:
        data (DataFrame): The dataset.
        columns (list): List of column names to plot.
        data_name (str): Name of the dataset for titles.

    Returns:
        None
    """
    data['Month'] = data.Timestamp.dt.month
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    fig.suptitle(f"{data_name} Monthly Trends")
    for col in columns:
        data.groupby('Month')[col].mean().plot(ax=axes[columns.index(col)], title=col, legend=True)

    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap_specific(datasets, columns, titles):
    """
    Plot correlation heatmaps for multiple datasets.

    Parameters:
        datasets (list): List of datasets (DataFrames).
        columns (list): Columns to include in the correlation calculation.
        titles (list): Titles for each heatmap.

    Returns:
        None
    """
    fig, axes = plt.subplots(1, len(datasets), figsize=(18, 6))
    for ax, data, title in zip(axes, datasets, titles):
        corr = data[columns].corr()
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title(title)

    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(data, data_names):
    """
    Plot the correlation heatmap for the given data.

    Parameters:
        data (list): List of dataframes.
        data_names (list): List of names of the dataframes.

    Returns:
        None
    """
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    fig.suptitle("Correlation Heatmap")
    for i, (data, data_name) in enumerate(zip(data, data_names)):
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm', ax=ax[i])
        ax[i].set_title(data_name)

    plt.tight_layout()
    plt.show()

def plot_scatter(data, columns, data_name='Data'):
    """
    Plot scatter plots for all combinations of the specified columns.

    Parameters:
        data (DataFrame): The dataset.
        columns (list): List of columns to plot.
        data_name (str): Name of the dataset for titles.

    Returns:
        None
    """
    combs = list(combinations(columns, 2))
    fig, axes = plt.subplots(1, len(combs), figsize=(15, 4))
    fig.suptitle(f"{data_name} Scatter Plots")
    for comb, ax in zip(combs, axes):
        data.plot.scatter(x=comb[0], y=comb[1], ax=ax)
        ax.set_title(f"{comb[0]} vs {comb[1]}")

    plt.tight_layout()
    plt.show()

def plot_wind_rose_combined(datasets, wind_speed_column, wind_direction_column, names):
    """
    Create combined wind rose plots for multiple datasets.

    Parameters:
        datasets (list): List of datasets (DataFrames).
        wind_speed_column (str): Column name for wind speed.
        wind_direction_column (str): Column name for wind direction.
        names (list): Titles for each dataset.

    Returns:
        None
    """
    fig, axes = plt.subplots(1, len(datasets), subplot_kw={'projection': 'windrose'}, figsize=(18, 6))
    for ax, data, title in zip(axes, datasets, names):
        ax.bar(data[wind_direction_column], data[wind_speed_column], normed=True, opening=0.8, edgecolor='white')
        ax.set_title(title)
        ax.legend(title="Wind Speed (m/s)")

    plt.tight_layout()
    plt.show()

def plot_histograms(datasets, columns, titles):
    """
    Plot histograms for multiple variables across datasets.

    Parameters:
        datasets (list): List of datasets (DataFrames).
        columns (list): Columns to plot histograms for.
        titles (list): Titles for each dataset.

    Returns:
        None
    """
    fig, axes = plt.subplots(len(columns), len(datasets), figsize=(18, 6 * len(columns)))
    for i, column in enumerate(columns):
        for j, (data, title) in enumerate(zip(datasets, titles)):
            ax = axes[i, j] if len(columns) > 1 else axes[j]
            sns.histplot(data[column], kde=True, ax=ax)
            ax.set_title(f"{title} - {column}")
            ax.set_xlabel(column)
            ax.set_ylabel("Frequency")

    plt.tight_layout()
    plt.show()

def calculate_and_plot_z_scores(datasets, columns, titles):
    """
    Calculate Z-scores for specified columns and plot histograms of Z-scores.

    Parameters:
        datasets (list): List of datasets (DataFrames).
        columns (list): Columns to calculate Z-scores for.
        titles (list): Titles for each dataset.

    Returns:
        None
    """
    fig, axes = plt.subplots(len(columns), len(datasets), figsize=(18, 6 * len(columns)))
    for i, column in enumerate(columns):
        for j, (data, title) in enumerate(zip(datasets, titles)):
            # Calculate Z-scores
            data[f"{column}_zscore"] = (data[column] - data[column].mean()) / data[column].std()
            # Plot histogram of Z-scores
            ax = axes[i, j] if len(columns) > 1 else axes[j]
            sns.histplot(data[f"{column}_zscore"], kde=True, ax=ax)
            ax.set_title(f"{title} - {column} Z-scores")
            ax.set_xlabel(f"{column} Z-score")
            ax.set_ylabel("Frequency")

    plt.tight_layout()
    plt.show()

def plot_bubble_charts(datasets, x_column, y_column, size_column, hue_column, titles):
    """
    Create bubble charts for multiple datasets.

    Parameters:
        datasets (list): List of datasets (DataFrames).
        x_column (str): Column for x-axis.
        y_column (str): Column for y-axis.
        size_column (str): Column for bubble size.
        hue_column (str): Column for bubble colour.
        titles (list): Titles for each dataset.

    Returns:
        None
    """
    fig, axes = plt.subplots(1, len(datasets), figsize=(18, 6))
    for ax, data, title in zip(axes, datasets, titles):
        sns.scatterplot(
            x=data[x_column],
            y=data[y_column],
            size=data[size_column],
            hue=data[hue_column],
            sizes=(20, 200),
            alpha=0.7,
            ax=ax
        )
        ax.set_title(title)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.legend(title=hue_column, loc='upper right', bbox_to_anchor=(1.2, 1))

    plt.tight_layout()
    plt.show()

def plot_temperature_vs_humidity(datasets, temperature_column, humidity_column, titles):
    """
    Create scatter plots of temperature vs relative humidity.

    Parameters:
        datasets (list): List of datasets (DataFrames).
        temperature_column (str): Column name for temperature.
        humidity_column (str): Column name for humidity.
        titles (list): Titles for each dataset.

    Returns:
        None
    """
    fig, axes = plt.subplots(1, len(datasets), figsize=(18, 6))
    for ax, data, title in zip(axes, datasets, titles):
        sns.scatterplot(
            x=data[humidity_column],
            y=data[temperature_column],
            ax=ax,
            alpha=0.7
        )
        ax.set_title(title)
        ax.set_xlabel("Relative Humidity (%)")
        ax.set_ylabel("Ambient Temperature (°C)")

    plt.tight_layout()
    plt.show()

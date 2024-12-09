import os
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations

def manage_data(data_path):
    '''
    This function checks if the data files are present in the data_path' directory. If the files are not present, 
    it downloads the files from Google Drive and extracts the contents of the zip file.

    Parameters:
    data_path (str): The path to the data directory.

    Returns:
    None
    
    '''

    # Create the data directory if it doesn't exist
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # List of expected files in the data_path' directory
    expected_files = [f'{data_path}/benin-malanville.csv', f'{data_path}/sierraleone-bumbuna.csv', f'{data_path}/togo-dapaong_qc.csv']

    # Check if the data_path' directory is empty or if any of the expected files are missing
    if not all([os.path.exists(f) for f in expected_files]):
        import gdown
        import zipfile

        # Correct file URL format (replace 'FILE_ID' with the actual ID from the link)
        file_url = 'https://drive.google.com/uc?id=1wRxR5CROC95Z9vPYlXwHrSGt79Of_zQU'
        destination = f'{data_path}/data.zip'
        
        # Download the file from Google Drive using gdown
        gdown.download(file_url, destination, quiet=True)

        # Extract the contents of the zip file
        with zipfile.ZipFile(destination, 'r') as zip_ref:
            zip_ref.extractall()
            
        # Remove the zip file after extracting
        os.remove(destination)

def clip_outliers(data, columns, valid_range):
    '''
    Clip the outliers in the data based on the valid range

    Args:
    data: DataFrame
    columns: List of columns to check for outliers
    valid_range: List of tuples containing the valid range for each column

    Returns:
    DataFrame: DataFrame with outliers clipped
    '''
    for col, (min_val, max_val) in zip(columns, valid_range):
        data[col] = data[col].clip(lower=min_val, upper=max_val)
    return data


def plot_time_series(data, columns, data_name='Data'):
    '''
    Plot time series data

    Args:
    data: DataFrame
    columns: list of str
    data_name: str

    Returns:
    None
    '''
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    fig.suptitle(f"{data_name} Time Series Data")
    for col in columns:
        data[col].plot(ax=axes[columns.index(col)], title=col, legend=True)

    plt.tight_layout()
    plt.show()

def plot_monthly_trends(data, columns, data_name='Data'):
    '''
    Plot monthly trends for the given columns

    Parameters:
    data (pd.DataFrame): The data to plot
    columns (list): The columns to plot
    data_name (str): The name of the data

    Returns:
    None
    '''
    data['Month'] = data.Timestamp.dt.month
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    fig.suptitle(f"{data_name} Monthly Trends")
    for col in columns:
        data.groupby('Month')[col].mean().plot(ax=axes[columns.index(col)], title=col, legend=True)

    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(data, data_names):
    '''
    Plot the correlation heatmap for the given data

    Parameters:
    data (list): List of dataframes
    data_names (list): List of names of the dataframes

    Returns:
    None
    '''
    fig, ax = plt.subplots(1, 3, figsize=(12, 4))
    fig.suptitle("Correlation Heatmap")
    for i, (data, data_name) in enumerate(zip(data, data_names)):
        sns.heatmap(data.corr(), annot=True, cmap='coolwarm', ax=ax[i])
        ax[i].set_title(data_name)

    plt.tight_layout()
    plt.show()


def plot_scatter(data, columns, data_name='Data'):
    '''
    Plot scatter plots for the given columns in the data

    Parameters:
    data (pd.DataFrame): The data to plot
    columns (list): The columns to plot
    data_name (str): The name of the data

    Returns:
    None
    '''
    combs = list(combinations(columns, 2))
    fig, axes = plt.subplots(1, len(combs), figsize=(15, 4))
    fig.suptitle(f"{data_name} Wind Conditions Scatter Plots")
    for comb, ax in zip(combs, axes):
        data.plot.scatter(x=comb[0], y=comb[1], ax=ax)
        ax.set_title(f"{comb[0]} vs {comb[1]}")
    
    plt.tight_layout()
    plt.show()
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import numpy as np

# Title of the App
st.title("Solar and Meteorological Data Analysis")

# File Upload
st.header("Upload Data Files")
uploaded_files = st.file_uploader(
    "Upload CSV files for analysis (e.g., Benin Malanville, Sierra Leone Bumbuna, Togo Dapaong)",
    accept_multiple_files=True,
    type=["csv"],
)

# Display Uploaded Files
if uploaded_files:
    datasets = {}
    for uploaded_file in uploaded_files:
        try:
            data = pd.read_csv(uploaded_file)
            datasets[uploaded_file.name] = data
            st.success(f"Successfully loaded {uploaded_file.name}")
        except Exception as e:
            st.error(f"Error loading {uploaded_file.name}: {e}")

    # Dataset Selection
    selected_dataset_name = st.selectbox(
        "Select a dataset to explore", list(datasets.keys())
    )

    if selected_dataset_name:
        selected_dataset = datasets[selected_dataset_name]

        # Data Preview
        st.subheader("Data Preview")
        st.write(selected_dataset.head())

        # Data Information
        st.subheader("Data Information")
        st.write(f"Shape: {selected_dataset.shape}")
        st.write("Summary Statistics:")
        st.write(selected_dataset.describe())

        # Missing Values
        st.subheader("Missing Values")
        st.write(selected_dataset.isnull().sum())

        # Outlier Detection
        st.subheader("Outlier Detection")
        numerical_columns = selected_dataset.select_dtypes(include=["number"]).columns
        selected_column = st.selectbox("Select a column for outlier analysis", numerical_columns)

        if selected_column:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.boxplot(data=selected_dataset, x=selected_column, ax=ax)
            st.pyplot(fig)

            # Outlier Clipping
            st.subheader("Outlier Removal")
            min_val = st.number_input(f"Enter minimum value for {selected_column}")
            max_val = st.number_input(f"Enter maximum value for {selected_column}")

            if st.button("Clip Outliers"):
                selected_dataset[selected_column] = selected_dataset[selected_column].clip(lower=min_val, upper=max_val)
                st.success(f"Outliers clipped for {selected_column}")
                st.write(selected_dataset.describe())

        # Visualization Options
        st.header("Visualizations")

        # Time Series Plot
        st.subheader("Time Series Plot")
        time_series_column = st.selectbox("Select a column for time series analysis", numerical_columns)
        timestamp_column = st.selectbox("Select the timestamp column", selected_dataset.columns)

        if time_series_column and timestamp_column:
            selected_dataset[timestamp_column] = pd.to_datetime(selected_dataset[timestamp_column])
            fig, ax = plt.subplots(figsize=(15, 5))
            selected_dataset.set_index(timestamp_column)[time_series_column].plot(ax=ax, title=f"Time Series: {time_series_column}")
            st.pyplot(fig)

        # Correlation Heatmap
        st.subheader("Correlation Heatmap")
        correlation_columns = st.multiselect("Select columns for correlation heatmap", numerical_columns)

        if correlation_columns:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(selected_dataset[correlation_columns].corr(), annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)

        # Wind Analysis
        st.subheader("Wind Analysis: Windrose Plot")
        wind_speed_column = st.selectbox("Select wind speed column", numerical_columns)
        wind_direction_column = st.selectbox("Select wind direction column", numerical_columns)

        if wind_speed_column and wind_direction_column:
            fig = plt.figure(figsize=(8, 8))
            ax = WindroseAxes.from_ax(fig=fig)
            ax.bar(selected_dataset[wind_direction_column], selected_dataset[wind_speed_column], normed=True, opening=0.8, edgecolor="white")
            ax.set_title("Windrose Plot")
            st.pyplot(fig)

        # Histograms
        st.subheader("Histogram")
        histogram_column = st.selectbox("Select a column for histogram", numerical_columns)

        if histogram_column:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(data=selected_dataset, x=histogram_column, kde=True, ax=ax)
            st.pyplot(fig)

        # Temperature vs Humidity Analysis
        st.subheader("Temperature vs Humidity Analysis")
        temp_column = st.selectbox("Select the temperature column", numerical_columns)
        humidity_column = st.selectbox("Select the humidity column", numerical_columns)

        if temp_column and humidity_column:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.scatterplot(x=selected_dataset[humidity_column], y=selected_dataset[temp_column], alpha=0.7, ax=ax)
            ax.set_title(f"{temp_column} vs {humidity_column}")
            ax.set_xlabel("Humidity (%)")
            ax.set_ylabel("Temperature (°C)")
            st.pyplot(fig)

        # Z-Score Analysis
        st.subheader("Z-Score Analysis")
        z_score_column = st.selectbox("Select a column for Z-score analysis", numerical_columns)

        if z_score_column:
            z_scores = (selected_dataset[z_score_column] - selected_dataset[z_score_column].mean()) / selected_dataset[z_score_column].std()
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(z_scores, kde=True, ax=ax)
            ax.set_title(f"Z-Scores for {z_score_column}")
            ax.set_xlabel("Z-Score")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        # Bubble Chart
        st.subheader("Bubble Chart")
        x_column = st.selectbox("Select the X-axis column", numerical_columns)
        y_column = st.selectbox("Select the Y-axis column", numerical_columns)
        size_column = st.selectbox("Select the size column", numerical_columns)
        hue_column = st.selectbox("Select the hue column", numerical_columns)

        if x_column and y_column and size_column and hue_column:
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.scatterplot(
                x=selected_dataset[x_column],
                y=selected_dataset[y_column],
                size=selected_dataset[size_column],
                hue=selected_dataset[hue_column],
                sizes=(20, 200),
                alpha=0.7,
                ax=ax
            )
            ax.set_title(f"Bubble Chart: {x_column} vs {y_column}")
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            st.pyplot(fig)

else:
    st.info("Please upload at least one CSV file to proceed.")

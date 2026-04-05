"""Core Skills Drill — Descriptive Analytics

Compute summary statistics, plot distributions, and create a correlation
heatmap for the sample sales dataset.

Usage:
    python drill_eda.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def compute_summary(df):
    """Compute summary statistics for all numeric columns.

    Args:
        df: pandas DataFrame with at least some numeric columns

    Returns:
        DataFrame containing count, mean, median, std, min, max
        for each numeric column. Save the result to output/summary.csv.
    """
    # TODO: Compute descriptive statistics (count, mean, median, std, min, max)
    #       for all numeric columns and save to output/summary.csv
    
    numeric_df = df.select_dtypes(include=['number'])
    summary = numeric_df.describe().loc[['count', 'mean', '50%', 'std', 'min', 'max']]
    summary = summary.rename(index={'50%': 'median'})
    summary.to_csv('output/summary.csv')
    print("Summary statistics saved to output/summary.csv")
    return summary


def plot_distributions(df, columns, output_path):
    """Create a 2x2 subplot figure with histograms for the specified columns.

    Args:
        df: pandas DataFrame
        columns: list of 4 column names to plot (use numeric columns)
        output_path: file path to save the figure (e.g., 'output/distributions.png')

    Returns:
        None — saves the figure to output_path
    """
    # TODO: Create a 2x2 figure with sns.histplot (KDE overlay) for each column
    #       Add titles, labels, and tight layout before saving
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    for i, col in enumerate(columns):
        if i < len(axes):   # Safety check
            sns.histplot(data=df, x=col, kde=True, ax=axes[i], color='skyblue')
            axes[i].set_title(f'Distribution of {col}', fontsize=14)
            axes[i].set_xlabel(col)
            axes[i].set_ylabel('Frequency')

    # If we have fewer than 4 columns, hide the empty subplots
    for j in range(len(columns), 4):
        axes[j].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f" Distributions plot saved to {output_path}")

def plot_correlation(df, output_path):
    """Compute Pearson correlation matrix and visualize as a heatmap.

    Args:
        df: pandas DataFrame with numeric columns
        output_path: file path to save the figure (e.g., 'output/correlation.png')

    Returns:
        None — saves the figure to output_path
    """
    # TODO: Compute the correlation matrix for numeric columns and
    #       visualize it as an annotated Seaborn heatmap
    
    numeric_df = df.select_dtypes(include=['number'])
    corr_matrix = numeric_df.corr(method='pearson')
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, 
                annot=True,           # Show correlation values
                cmap='coolwarm',      # Red = positive, Blue = negative
                vmin=-1, vmax=1,      # Correlation range
                center=0,
                fmt='.2f',            # 2 decimal places
                linewidths=0.5)
    plt.title('Correlation Heatmap of Numeric Features', fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f" Correlation heatmap saved to {output_path}")


def main():
    """Load data, compute summary, and generate all plots."""
    os.makedirs("output", exist_ok=True)

    # TODO: Load the CSV from data/sample_sales.csv
    # TODO: Call compute_summary and save the result
    # TODO: Choose 4 numeric-friendly columns and call plot_distributions
    # TODO: Call plot_correlation
    
    df = pd.read_csv('data/sample_sales.csv')
    print(f" Data loaded successfully! Shape: {df.shape}")

    # Task 1: Summary Statistics
    compute_summary(df)

    # Task 2: Distribution Plots - Use only existing numeric columns (max 4)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    plot_columns = numeric_cols[:4]   # Take up to 4 numeric columns

    print(f"Plotting distributions for: {plot_columns}")
    plot_distributions(df, plot_columns, 'output/distributions.png')

    # Task 3: Correlation Heatmap
    plot_correlation(df, 'output/correlation.png')

    print("\n All tasks completed! Check the 'output/' folder.")
if __name__ == "__main__":
    main()

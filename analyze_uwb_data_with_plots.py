import os
import uwb_dataset
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create the figure directory if it doesn't exist
figure_dir = "figures"
os.makedirs(figure_dir, exist_ok=True)

# Import raw data using uwb_dataset.py
data = uwb_dataset.import_from_files()

# Convert the dataset to a pandas DataFrame
columns = [
    "NLOS", "Measured_Range", "FP_IDX", "FP_AMP1", "FP_AMP2", "FP_AMP3",
    "STDEV_NOISE", "CIR_PWR", "MAX_NOISE", "RXPACC", "CH", "FRAME_LEN",
    "PREAM_LEN", "BITRATE", "PRFR", *[f"CIR_{i}" for i in range(1016)]
]
df = pd.DataFrame(data, columns=columns)

# Key columns for statistics and visualization
key_columns = [
    "NLOS", "Measured_Range", "FP_IDX", "FP_AMP1", "FP_AMP2", "FP_AMP3",
    "STDEV_NOISE", "CIR_PWR", "MAX_NOISE", "RXPACC", "CH", "FRAME_LEN",
    "PREAM_LEN", "BITRATE", "PRFR"
]

# Calculate basic statistics
statistics_summary = {
    "mean": df[key_columns].mean(),
    "median": df[key_columns].median(),
    "std_dev": df[key_columns].std(),
    "min": df[key_columns].min(),
    "max": df[key_columns].max(),
}

# Print the calculated statistics
for stat_name, values in statistics_summary.items():
    print(f"\n{stat_name.title()} Statistics:")
    print(values)

# Save the statistics to a CSV file
output_path = "statistics_summary.csv"
statistics_df = pd.DataFrame(statistics_summary)
statistics_df.to_csv(output_path, index=True)
print(f"\nStatistics summary saved to {output_path}")

# Plot distributions for key columns
for column in key_columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column], kde=True, bins=30, color="blue")
    plt.title(f"Distribution of {column}", fontsize=16)
    plt.xlabel(column, fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(alpha=0.5)
    
    # Save the plot
    plot_path = os.path.join(figure_dir, f"{column}_distribution.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Saved distribution plot for {column} to {plot_path}")

# Pairplot for relationships (optional, for selected columns)
selected_columns = ["Measured_Range", "FP_IDX", "FP_AMP1", "FP_AMP2", "FP_AMP3"]
sns.pairplot(df[selected_columns], kind="scatter", diag_kind="kde")
pairplot_path = os.path.join(figure_dir, "pairplot_selected_columns.png")
plt.savefig(pairplot_path)
plt.close()
print(f"Saved pairplot for selected columns to {pairplot_path}")
import os
import pandas as pd
import matplotlib.pyplot as plt

class GFRnevReader:
    """
    A class for reading data from GFRnev files.
    """

    def __init__(self, file_name):
        self.file_name = file_name

    def read_data(self):
        """
        Reads data from the GFRnev file and returns a list of lists
        containing the run name, attribute, topic, metric, value,
        and cutoff for each line in the file.
        """
        # extract the run name and attribute from the file name
        base_name = os.path.basename(self.file_name)
        run_name, attribute, _ = base_name.split(".")

        # define a list to hold the data
        data = []

        # read the lines from the text file
        with open(self.file_name) as file:
            lines = file.readlines()[1:]  # skip the first line

        # loop through the lines and extract the data
        for line in lines:
            parts = line.split()

            topic = parts[0]
            metric_suffix = parts[1].rstrip("=")
            metric = metric_suffix.split("@")[0]
            value = float(parts[2])

            if "@" in metric_suffix:
                cutoff = int(metric_suffix.split("@")[1])
            else:
                cutoff = 0

            # append the run name, attribute, topic, metric, value,
            # and cutoff to the data list
            data.append([run_name, attribute, topic, metric, value, cutoff])

        return data


class GFRnevDataFrame:
    """
    A class for creating a Pandas DataFrame from GFRnev data.
    """

    def __init__(self, data):
        self.data = data

    def create_dataframe(self):
        """
        Creates a Pandas DataFrame from the GFRnev data.
        """
        # create a DataFrame from the data
        df = pd.DataFrame(
            self.data,
            columns=["Run Name", "Attribute", "Topic", "Metric", "Value", "Cutoff"],
        )

        return df

        
class Visualizer:

    def __init__(self, df):
        self.df = df

    def compare_aggregated_runs(self, cutoff_value):

        # Filter the dataframe based on the cutoff value
        df_filtered = self.df[self.df['Cutoff'] == cutoff_value]

        # Group by 'Run Name' and 'Metric', and take the mean of the 'Value' column
        df_grouped = df_filtered.groupby(['Run Name', 'Metric']).mean().reset_index()

        # Pivot the dataframe to group by metric and run name
        df_pivot = df_grouped.pivot(index='Metric', columns='Run Name', values='Value')

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        df_pivot.plot(kind='bar', ax=ax, rot=0, width=0.8)

        # Set the axis labels and title
        ax.set_xlabel('Metric')
        ax.set_ylabel('Value')
        ax.set_title(f'NTCIR Fairweb\'23 Systems (Cutoff = {cutoff_value}) - Aggregated')

        # Add a legend
        ax.legend(title='Run Name')

        # Adjust the plot to prevent labels from being cut off
        fig.tight_layout()

        # Show the plot
        plt.savefig('./results/Systemwise_Comparison.pdf', dpi=330)


CUTOFF = 100
# create an empty list to hold the data
all_data = []

# get a list of all files in the folder with the extension .GFRnev
folder_path = "."
extension = ".GFRnev"
file_names = [f for f in os.listdir(folder_path) if f.endswith(extension)]

# loop through the files and read the data
for file_name in file_names:
    print(f"File: {file_name}")
    reader = GFRnevReader(file_name)
    data = reader.read_data()

    # add the data to the all_data list
    all_data.extend(data)

# create a GFRnevDataFrame object and create the DataFrame
gfrnev_df = GFRnevDataFrame(all_data)
df = gfrnev_df.create_dataframe()

# Save the DataFrame
df.to_csv('./results/Results.csv', index=False)

viz = Visualizer(df)
viz.compare_aggregated_runs(CUTOFF)

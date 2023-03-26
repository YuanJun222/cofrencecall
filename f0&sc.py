import os
import librosa
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt

# Set the parent folder paths
parent_folder_paths = ['/Users/wonjun/PycharmProjects/cc/data/Deacrease low', '/Users/wonjun/PycharmProjects/cc/data/decrease high ', '/Users/wonjun/PycharmProjects/cc/data/increase']

for parent_folder_path in parent_folder_paths:
    # Loop through all the subdirectories in the parent folder
    for subfolder_name in os.listdir(parent_folder_path):
        subfolder_path = os.path.join(parent_folder_path, subfolder_name)
        if os.path.isdir(subfolder_path):
            f0_range_list = []  # create a new list to store f0 range values
            file_names = []  # create a new list to store file names
            spectral_centroid_avg_list = []  # create a new list to store spectral centroid avg values
            spectral_centroid_maxmin_list = []  # create a new list to store spectral centroid max - min values
            amplitude_mean_list = []  # create a new list to store amplitude mean values
            amplitude_maxmin_list = []  # create a new list to store amplitude max - min values

            # Loop through each MP3 file in the subdirectory
            for file_name in tqdm(os.listdir(subfolder_path)):
                # Check if the file is an MP3 file
                if file_name.endswith('.mp3'):
                    # Load the audio file
                    file_path = os.path.join(subfolder_path, file_name)
                    y, sr = librosa.load(file_path)

                    # Calculate the F0 values
                    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C1'), fmax=librosa.note_to_hz('C7'),
                                                                 hop_length=512)
                    f0_filtered = [f0[i] for i in range(len(f0)) if 64 <= f0[i] <= 200]  # filter the F0 values

                    # Calculate the F0 range value and append to the list
                    f0_mean = np.mean(f0_filtered)
                    f0_range = np.max(f0_filtered) - np.min(f0_filtered)
                    f0_range_list.append(f0_range)

                    # Calculate the spectral centroid
                    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr, fmin=64, fmax=200)
                    spectral_centroid_avg = np.nanmean(spectral_centroids)
                    spectral_centroid_maxmin = np.nanmax(spectral_centroids) - np.nanmin(spectral_centroids)
                    spectral_centroid_avg_list.append(spectral_centroid_avg)
                    spectral_centroid_maxmin_list.append(spectral_centroid_maxmin)

                    # Calculate the amplitude mean value and append to the list
                    amplitude_mean = np.mean(np.abs(y))
                    amplitude_mean_list.append(amplitude_mean)

                    # Calculate the amplitude max-min value and append to the list
                    amplitude_maxmin = np.max(y) - np.min(y)
                    amplitude_maxmin_list.append(amplitude_maxmin)

                    file_names.append(file_name)

            # Create a Pandas DataFrame from the lists of file names and F0 range values
            df = pd.DataFrame({'File Name': file_names, 'F0 Range': f0_range_list, 'Spectral Centroid Avg': spectral_centroid_avg_list,
                               'Spectral Centroid Max-Min': spectral_centroid_maxmin_list})

            # Set the Excel file name to the subdirectory name
            excel_file_name = subfolder_name + '_merged.xlsx'
            excel_file_path = os.path.join(parent_folder_paths, excel_file_name)

            # Export the DataFrame to an Excel file
            df.to_excel(excel_file_path)

            # Plot and save F0 and spectral centroid graph
            fig, ax = plt.subplots()
            ax.plot(times_filtered, f0_filtered, label='f0', color='cyan', linewidth=3)
            ax.plot(times, spectral_centroids[0], label='Spectral centroid', color='red', linewidth=3)
            ax.text(0.5, 0.95, f'Amplitude mean: {amplitude_mean:.2f}', ha='center', va='center',
                    transform=ax.transAxes, fontsize=12)
            ax.text(0.5, 0.9, f'Amplitude max-min: {amplitude_maxmin:.2f}', ha='center', va='center',
                    transform=ax.transAxes, fontsize=12)
            ax.set(title='F0 & Spectral Centroid', xlabel='Time (s)', ylabel='Frequency (Hz)')
            ax.legend(loc='upper right')
            graph_file_name = file_name.split('.')[0] + 'merged.png'
            graph_file_path = os.path.join(subfolder_path, graph_file_name)
            plt.savefig(graph_file_path)
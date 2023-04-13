# MECH-463-Capstone
A place for all our pre and post-processing code for IMU data


This README contains a brief overview of the code we generated in Winter 2023. The repository comprises 4 subfolders.

*Data*
This section contains the useful selection of the data we collected over the semester. It uses this (not very good) naming convention:

SubjectFirstName_Trial#_autolabeled

Trial# shows the trial speed and condition:
1 -> 3.5 km/h
2 -> 5 km/h
3 -> 6.5 km/h
4 -> 2 km/h
5 -> 3 km/h
6 -> 2 km/h (simulated foot drop)
7 -> 3 km/h (simulated foot drop)

These were labeled using the automatic labeling script



*ML algorithms*
This folder contains both SVM and LSTM algorithms, configured to use k-fold validation. Ensure the plotted results match the actual data that is used - this must be done manually.
SVM is implemented using scikit-learn, LSTM is implemented using TensorFlow.



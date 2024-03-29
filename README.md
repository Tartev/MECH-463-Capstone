# MECH-463-Capstone

This README contains a brief overview of the code we generated in Winter 2023. The repository comprises 4 subfolders.

Authors:

- Griffin Burd, griffin.burd@mail.mcgill.ca       } contact if needed

- Vincent.Tarte, vincent.tarte@mail.mcgill.ca

- Mario Daccache, mario.daccache@mail.mcgill.ca

- Bennett Evans, bennett.evans@mail.mcgill.ca

**Requirements**

Install all necessary packages. Alternatively, run the code in Google colab.


**Data**

*Collection*

This folder contains the useful selection of the data we collected over the semester. This data was collected by mounting the Shimmer 3 IMU on our mediolateral shanks, and subequently walking on a treadmill at certain speeds. In some of our trials, we tried to emulate the gait of someone suffering from foot drop.

*Naming*

Our data uses the following naming convention:

*SubjectFirstName_Trial#*

*Trial# indicates the trial speed and condition:*
- *1 -> 3.5 km/h*
- *2 -> 5 km/h*
- *3 -> 6.5 km/h*
- *3B -> 7.5 km/h*
- 
- *4 -> 2 km/h*
- *5 -> 3 km/h*
- *6 -> 2 km/h (simulated foot drop)*
- *7 -> 3 km/h (simulated foot drop)*

Some of these data is unlabeled, while others are labeled using the automatic labeling script. In the labeled data, the last column represents the labels of each datapoint (0=stance, 1=swing).

Some of these datasets were processed to eliminate non-walking at the start and end of the trial. In these cases, time will not start at 0.

If you choose to change the naming convention, be sure to update the algorithms where necessary so that they reference the correct file names.

Note that trials 1-3B and 4-7 were collected during different DAQ sessions. The IMU was mounted on different legs (left/right) for these sessions, so using data across both requires flipping the sign on certain signals. This is performed somewhat clunkily within the ML algorithms. Both SVM and LSTM perform best when trained and tested on data acquired from an individual DAQ session (i.e., only trials 1-3B or 4-7).



**ML algorithms**

*Structure*

This folder contains both SVM and LSTM algorithms. SVM is implemented using scikit-learn, while LSTM is implemented using TensorFlow. However, the code for both is structured very similarly.

At the top, data is imported - make sure these data are located in your working folder. K-fold validation will be performed on these data using leave-one-out training.

Depending on the amount of data used, the algorithms will usually take about 5-15 minutes to run.

Error results are plotted. Ensure that the labels on these plots actually match the data that is used - this must be done manually.



**Labeling**

This folder contains the automatic labeling script. This will take an unlabeled .csv (Shimmer output), and add a labeled column. It will also plot the predicted labels so you can tell if it makes a big mistake.

The script is a bit clunky: input the name of the unlabeled data in several places, and choose the name for the output file. It will save the output .csv in your working folder.


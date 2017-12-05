#********************************************************
# FILE: my_first_script.py
# AUTHOR: Melinda Pullman
# EMAIL: mkp0015@uah.edu
# MODIFIED BY: n/a
# ORGANIZATION: UAH/ATS Dept.
# CREATION DATE: 02/16/2017
# LAST MOD DATE: n/a
# PURPOSE: This script reads ASCII data into NumPy arrays before
#          creating two functions that will find elements in the
#          data above certain thresholds and plotting the results
# DEPENDENCIES: numpy, time, matplotlib
#********************************************************

#import dependencies (packages)
import numpy as np
import matplotlib.pyplot as plt
import time 

#read in Huntsville ascii file
infile = r'\\uahdata\rhome\ESS508\huntsville.asc'
with open(infile, 'r') as f:
    lines = f.readlines()

#redeclare lines variable to just include data and not header
lines = lines[6:]

#get dimensions of data 
x_dim = len(lines[7].split(' ')[:-1])
y_dim = len(lines)

#create blank array to hold data
img = np.zeros([y_dim, x_dim])

#read data into blank array by row then column
for i in range(img.shape[0]):
    row = lines[i].split(' ')[:-1]
    for j in range(img.shape[1]):
        img[i,j] = row[j]

#plot huntsville ascii data
plt.imshow(img, cmap='gray')
plt.title('Huntsville ISERV Data')
plt.show()



#define function for finding elements greater than or equal to a threshold
def threshold_function(data, threshold):
    """
    FUNCTION:  img_thres_func = threshold_function(data, threshold)
    ARGUMENTS: data - the input 2-dimensional array that will be examined
               threshold - the threshold at which to examine the array
    KEYWORDS:  N/A
    RETURNS:   img_thres - the 2-dimensional array with boolean values
    NOTES:     Takes 2-dimensional array, identifies if each element is
               greater than or equal to a threshold by using for loops and
               iterations, and returns a boolean numpy array with the same
               dimensions of the original array.     
    """
    
    img_thres = np.zeros([data.shape[0],data.shape[1]])
        
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            img_thres[i,j] = (data[i,j] >= threshold)

    return img_thres

#define numpy function for finding elements greater than a threshold
def np_threshold_function(data, threshold):
    """
    FUNCTION:  img_np_thres_func = np_threshold_function(data, threshold)
    ARGUMENTS: data - the input 2-dimensional array that will be examined
               threshold - the threshold at which to examine the array
    KEYWORDS:  N/A
    RETURNS:   img_thres - the 2-dimensional array with boolean values
    NOTES:     Takes a 2-dimensional array, uses numpy functionality to
               identify if each element is greater than or equal to a
               threshold, then returns a boolean numpy arary with the
               same dimensions of the original array.
    """

    img_thres = data >= threshold
    return img_thres



#start time to perform function 1
start_time1 = time.time()

#run the threshold_function for img data
img_thres_func = threshold_function(img, 100)

#return end time to perform function 1
time_diff1 = time.time() - start_time1 
print 'threshold_function took', time_diff1, ' seconds to run'

#start time to perform function 2
start_time2 = time.time()

#run the np_threshold_function for img data
img_np_thres_func = np_threshold_function(img, 150)

#return end time to perform function 2
time_diff2 = time.time() - start_time2
print 'np_threshold_function took', time_diff2, ' seconds to run'

#time difference between the two functions
print 'The time difference between the two functions was equal to', time_diff1 - time_diff2, 'seconds'

#plot threshold_function for img data
plt.imshow(img_thres_func, cmap='gray')
plt.title('Huntsville ISERV Data With Threshold of 100')
plt.show()

#plot np_threshold_function for img data
plt.imshow(img_np_thres_func, cmap='gray')
plt.title('Huntsville ISERV Data With Threshold of 150')
plt.show()

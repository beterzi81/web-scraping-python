import numpy as np             # importing numpy library as np                     
pre_two_array = np.array([[10, 30, 50, 70, 90], [10, 30, 50, 70, 90], [10, 30, 50, 70, 90], [10, 30, 50, 70, 90], [10, 30, 50, 70, 90]])    # defining a 2D array having 5 rows and 5 columns
print(pre_two_array)                       # printing the array
norm = np.linalg.norm(pre_two_array)       # To find the norm of the array
print(norm)                                # Printing the value of the norm
normalized_array = pre_two_array/norm  # Formula used to perform array normalization
print(normalized_array)                # printing the normalized array
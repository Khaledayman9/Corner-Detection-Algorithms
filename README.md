# Corner-Detection-Algorithms
Analyze the interaction between various scoring functions and automatic threshold detection. In more specific terms, scoring functions (corner detections) are to be applied to the image, then the resulting gradient magnitudes are to be subjected to automatic threshold detection.

# Steps
In more specific terms, scoring functions (corner detections) are to be applied to the image, then the resulting gradient magnitudes are to be subjected to automatic threshold detection. As per that, the following components are to be implemented:
- Corner detection:
  - Harris.
  - SUSAN.
- Automatic threshold detection:
  - Calculate convex hull.


# Implementation
## Harris and Susan corner detection
In this part, we implement two functions as follows:
### 1. Harris:
- Input:
  - The input image (2D array or the original image)
  - Tunable parameter k (for simplicity equate it to 0.04 for testing purposes).
- Output:
  - 2D array representing the matrix (the resulting image) after corner detection.
  - Min which represents the min value of the resulted values after applying harris on the input image.
  - Max which represents the max value of the resulted values after applying harris on the input image.
- Description:
  - Implements the Harris corner detection technique using a **3 x 3** window around each pixel and use the following kernels to compute the derivative in the x and y directions.
  - Derivative in the x direction:
    
  ![DX](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/f81af90f-cb35-45dd-be61-0e46a2f763d2)
  
  - Derivative in the y direction:
    
  ![dy](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/3f633857-773d-42bc-b908-7311ed4b6ccc)
- Example for the output:
  - First Example:
      - Min = -4756062904.36
      - Max = 19205376969.44
        
   ![o1](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/791827de-6fb0-47c0-9412-0fd32bd8f44d)
  - Second Example:
      - Min = -4678122250.24
      - Max = 25481986947.04
        
    ![o2](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/aa72bd77-317d-4942-99e6-b258661ea6be)

### 2. Susan:
- Input:
  - The Original Image (It is advisable to not turn the image to 2D array to give more accurate results)
  - Tunable Parameter t (which will differ from one image to the other)
- Output:
  - 2D array representing the resulting image.
- Description:
  - Implement the Susan corner detection using the equation and a kernel size which is equal to 3x3.
- Example for the output:
  - First Example with t = 50:
    
     ![o3](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/fbb2e467-17e3-43b4-b468-bdf3f244cd25)

  
  - Second Example with t = 2:
    
    ![o4](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/c11cdd26-dbc7-4993-87ee-6f436a5c3299)

    
## Getting Data Ready for Convex Hull:
In order to get the data ready for the convex hull, we need to get the histogram of the resulting images. Susan is fine to get a histogram while Harris is not !!. Why is this? Because the resulted values vary from the negative to positive values. Hence, we get the max and min value resulted in Harris. So we need to handle it first by performing contrast stretching on the image before getting the histogram so that the values are mapped between [0-255].

### 1. Contrast Stretching:
- Input:
  - 2D array representing the image (the output of harris).
  - a,b,c,d (the variables required for contrast stretching).
- Output:
  - 2D array representing the output after applying contrast stretching.
- Example for the output:
  - On the camera man image:
    
   ![o5](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/23b16e91-2b2c-42ac-864d-30cb206ee26f)

  - On the second example:
    
  ![o6](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/88897641-6102-4bee-a7fc-dc3d3524ab56)

  
### 2. Calculate Histogram for Susan:
- Input:
  - 2D array representing the image (resulted from susan).
- Output:
  -  an array representing the histogram of the image.
- Example for the output:
  - For first image:
    
    ![o7](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/ed023d4c-8f61-492d-9691-8c49dba09746)

  - For second image:

    ![o8](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/819502da-403d-48ce-b993-02030186859f)

### 3. Calculate Histogram for harris:
- Input:
  - 2D array representing the image (resulted from harris after doing the necessary modification).
- Output:
  -   an array representing the histogram of the image.
- Example for the output:
  - For first image:
    
  ![o11](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/33425d45-e04c-44a6-984c-4b49e4af51ba)

  - For second image:

   ![o12](https://github.com/Khaledayman9/Corner-Detection-Algorithms/assets/105018459/41b28f38-c188-4ebf-9fad-d9f8c97a91fa)


## Getting Data Ready for Convex Hull:
As gradient magnitudes are calculated out of edges and corners detectors, a threshold is traditionally used in order to allow only strong features to be returned as a result. Instead of assigning static thresholds, an automated approach is to be followed, which is the  convex hull. Hence, in this part we implement the following functions:
### 1. GetHull:
- Input:
  - 1D array representing the histogram.
- Output:
  - 1D array of tuples representing the start point and the end of each region in the convex hull.
- Description:
  - We start the convex hull by getting the maximum slope that will represent each region and hence we want to know the start point of the region (x,y) and the end point of it (x,y).
- Example for the output:
  - For Susan:
    - For the first image: [(0, 1020), (8, 54633), (9, 1423)]
    - For the Second Image: [(0, 2336), (9, 265732)]
 - For Harris:
    - For the first image: [(0, 1), (50, 57206), (255, 0)]
    - For the Second Image: [(0, 504), (39, 309797), (255, 0)]

### 2. GetHullValues:
- Input:
  - 1D array of tuples representing the convex hull points.
- Output:
  - 1D array representing the hull values for each color.
- Description:
  - Here we get the hull values according to the equation of region which you can get using the equation of the straight line: y=mx+c.
  - Get the hull value of each intensity by substituting in the line equation to get the y value (representing the hull value).
- Example for the output:
  - For Susan:
    - For the first image: [1020.0, 7721.625, 14423.25, 21124.875, 27826.5,34528.125, 41229.75, 47931.375, 54633.0, 1423.0]
    - For the Second Image: [2336.0, 31602.222222222223, 60868.444444444445,90134.66666666667, 119400.88888888889,148667.11111111112, 177933.33333333334,207199.55555555556, 236465.77777777778, 265732.0]

### 3. GetThreshold:
- Input:
  - 1D array representing the histogram.
  - 1D array representing the hull values.
- Output:
  - The threshold according to the convex hull criteria
- Description:
  - Here you take the hull values and the histogram values and apply the last step in convex hull algorithm to get the threshold.
- Example for the output:
  - For Susan:
    - For the first image: 7
    - For the Second Image: 8
 - For Harris:
    - For the first image: 52
    - For the Second Image: 40


### 4. ApplyThresh:
- Input:
  - 1D array representing the histogram.
  - The Threshold value that we already got.
- Output:
  - Two 1D arrays representing the histogram after splitting it below and above the threshold.
- Description:
  - The main aim of this function is to split the histogram into two arrays representing the histogram of values below threshold and histogram of values above threshold so that we can re-apply the thresholding once again on the resulted histograms.
- Example for the output:
  - For Susan:
    - For the first image:
      - [1020, 107, 324, 641, 890, 2261, 1881]
      - [2356, 54633, 1423]
    - For the Second Image: 8
      - [2336, 2020, 2147, 17732, 6258, 9327, 6458, 7387]
      - [22603, 265732]
     


## Plotting Results:

### 1. drawImages:
- Input:
  - First Threshold representing the lower threshold.
  - Second Threshold representing the higher threshold.
  - Image the image resulted from the corner detectors.
- Output:
  -  3 images representing the original image after splitting it into three regions which are:
    - **lower region** which is the image below the threshold.
    - **mid region** which is the image between the 2 thresholds.
    - **higher region** which is the image above the higher threshold.
- Description:
  - The main purpose of this image is to split the image into 3 images after getting all the work done and getting 2 thresholds from the resulted image of the corner detection so that we can divide the image into corners, detectors and flat regions.once again on the resulted histograms.



# Final Goal
The final goal is to apply Harris and Susan corner detection to the image, afterwards you apply Convex hull to the result so that you can get a specific value corresponding to the threshold. Based on this threshold, you will split the histogram of the resulting image into 2  parts and then take the first part and apply on it the Convex Hull thresholding again resulting in 2 thresholds so that we can divide the image based on them.


# Technologies
- Python
- Google Colab

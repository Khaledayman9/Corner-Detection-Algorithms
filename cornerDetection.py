# -*- coding: utf-8 -*-
"""CV Assignment2_5lyha ala Allah.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1d5PhYDaagacMCDwy-iAILwBs-Z6BclOI
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

!wget -O ex_image_1.jpg https://www.math.hkust.edu.hk/~masyleung/Teaching/CAS/MATLAB/image/images/cameraman.jpg # t = 50
!wget -O ex_image_2.jpg https://indiantechwarrior.com/wp-content/uploads/2021/10/Harris-Corner-600x570.jpg # t = 2
!wget -O test_image_1.jpg https://files.123freevectors.com/wp-content/original/171185-20-black-square-pattern-vector-pack-02.jpg # t = 103
!wget -O test_image_2.jpg https://docs.nvidia.com/vpi/kodim08_grayscale.png  # t = 75
!wget -O test_image_3.jpg https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTGjNtoiUIHvLUMM5nLp_N4o3La-F8FKboqGnZ0X6faL7WpEjZK # t = 35
!wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1WvA9cKxkkVe9JpzVljbq0pR73Vo_wy52' -O test_image_4.jpg # t = 65

ex_im1 = Image.open("ex_image_1.jpg").convert('L')
ex_im2 = Image.open("ex_image_2.jpg").convert('L')
test_im1 = Image.open("test_image_1.jpg").convert('L')
test_im2 = Image.open("test_image_2.jpg").convert('L')
test_im3 = Image.open("test_image_3.jpg").convert('L')
test_im4 = Image.open("test_image_4.jpg").convert('L')

ex_im1_arr = np.array(ex_im1)
ex_im2_arr = np.array(ex_im2)
test_im1_arr = np.array(test_im1)
test_im2_arr = np.array(test_im2)
test_im3_arr = np.array(test_im3)
test_im4_arr = np.array(test_im4)

"""# **Harris:**


*   **Input:**
  1. **The input image** (2D array or the original image)
  2. **Tunable parameter k** (for simplicity equate it to 0.04 for testing purposes).
*   **Output:**
  1. **2D array** representing the matrix (the resulting image) after corner detection.
  2. **Min** which represents the min value of the resulted values after applying harris on the input image
  3. **Max** which represents the max value of the resulted values after applying harris on the input image
*   **Description:**
  * Implements the Harris corner detection technique as discussed in the tutorial using **a 3 x 3 window** around each pixel and use the given kernels in the assignment description to compute the derivative in the **x** and **y** directions.
"""

def Harris(image, ka):
    image = np.array(image, dtype=np.float64)
    kernel_dx = np.array([[-1, 0, 1]])
    kernel_dy = np.array([[-1], [0], [1]])
    Ix = conv_op_2d(image, kernel_dx)
    Iy = conv_op_2d(image, kernel_dy)
    IxIx = Ix * Ix
    IyIy = Iy * Iy
    IxIy = Ix * Iy
    Axx = conv_op_2d(IxIx, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))
    Ayy = conv_op_2d(IyIy, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))
    Axy = conv_op_2d(IxIy, np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]))
    det_M = Axx * Ayy - Axy**2
    trace_M = Axx + Ayy
    res = det_M - ka * trace_M**2
    min = res[0, 0]
    max = res[0, 0]
    for i in range(res.shape[0]):
        for j in range(res.shape[1]):
            if res[i, j] < min:
                min = res[i, j]
            if res[i, j] > max:
                max = res[i, j]
    return res, min, max

def conv_op_2d(image, kernel):
    img_array = np.array(image, dtype=np.float64)
    rows, cols = img_array.shape
    k_rows, k_cols = kernel.shape
    res = np.array([[0.0] * cols for _ in range(rows)], dtype=float)
    for i in range(2, rows - 2):
        for j in range(2, cols - 2):
            neighborhood = img_array[i - k_rows//2:i + k_rows//2 + 1, j - k_cols//2:j + k_cols//2 + 1]
            result = 0.0
            for m in range(neighborhood.shape[0]):
                for n in range(neighborhood.shape[1]):
                    result += neighborhood[m, n] * kernel[m, n]
            res[i, j] = result
    return res

"""# **Susan:**


*   **Input:**
  1. **The Original Image** (It is advisable to not turn the image to 2D array to give more accurate results)

  2. **Tunable Parameter t**.

*   **Output:**
  1. **2D array** representing the resulting image.
  
*   **Description:**
  * Implement the Susan corner detection using the equation discussed in the tutorial and a kernel size which is equal to **3x3**.
"""

def Susan(image, t):
    img_array = np.array(image, dtype=np.float64)
    rows, cols = img_array.shape
    res = np.array([[0.0] * cols for _ in range(rows)], dtype=float)
    kernel = np.array([[255.0, 255.0, 255.0],
                       [255.0, 255.0, 255.0],
                       [255.0, 255.0, 255.0]])
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            neighborhood = img_array[i - 1:i + 2, j - 1:j + 2]
            brightness_diff = np.exp(-((neighborhood - img_array[i, j]) / t) ** 6)
            corner_response = 0.0
            for ni in range(3):
                for nj in range(3):
                    corner_response += brightness_diff[ni, nj]
            res[i, j] = corner_response
    return res

"""# **Getting Data Ready for Convex Hull**
In order to get the data ready for the convex hull, we need to get the histogram of the resulting
images. Susan is fine to get a histogram while Harris is not !!. Why is this? Because the
resulted values vary from the negative to positive values. Hence, we get the max and min value
resulted in Harris. So we need to handle it first by performing contrast stretching on the image
before getting the histogram so that the values are mapped between [0-255].

## **Contrast Stretching:**

*   **Input:**
  1. **2D array representing the image** (the output of harris)

  2. **a,b,c,d** (the variables required for contrast stretching).

*   **Output:**
  1. **2D array representing the output after applying contrast stretching.**
"""

def contrastStretch(im, a,b,c,d):
  res = im.copy()
  scl = (b-a)/(d-c)
  for i in range (0,len(im)):
    for j in range (0,len(im[0])):
      res[i][j] = int((int(im[i][j])-c)*scl+a)
  return res

"""## **Calculate Histogram for Susan:**


*   **Input:**
  1. **2D array representing the image** (resulted from susan)

*   **Output:**
  1. **an array representing the histogram of the image**
  
"""

def CalcHistSusan(image, size):
  res = [0 for x in range((3**2)+1)]
  for i in range(len(image)):
    for j in range(len(image[0])):
      res[int(image[i][j])]+=1
  return res

"""## **Calculate Histogram for Harris:**


*   **Input:**
  1. **2D array representing the image** (resulted from harris after doing the *necessary modification*)

*   **Output:**
  1. **an array representing the histogram of the image**
  
"""

def CalcHistHarris(image):
  res = [0 for x in range(256)]
  for i in range(len(image)):
    for j in range(len(image[0])):
      res[int(image[i][j])]+=1
  return res

"""# **Convex Hull:**
As gradient magnitudes are calculated out of edges and corners
detectors, a threshold is traditionally used in order to allow only strong
features to be returned as a result. Instead of assigning static
thresholds, an automated approach is to be followed, which is the convex hull. Hence, in this part you are asked to implement the
following functions:

## **GetHull:**

*   **Input:**
  1. **1D array** representing the histogram.

*   **Output:**
  1. **1D array of tuples** representing the start point *(x,y)* and the end point *(x,y)* of each region in the convex hull.
  
*   **Description:**
  * As discussed in the tutorial, we start the convex hull by getting the
maximum slope that will represent each region and hence we want to
know the start point of the region *(x,y)* and the end point of it *(x,y)*.
"""

def getHull(hist):
    res = []
    i = 0
    while i < len(hist) - 1:
        max_slope = float('-inf')
        end_index = i + 1
        for j in range(i + 1, len(hist)):
            slope = (hist[j] - hist[i]) / (j - i)
            if slope > max_slope:
                max_slope = slope
                end_index = j
        res.append((i, hist[i]))
        i = end_index
    res.append(((len(hist) - 1), hist[(len(hist) - 1)]))
    return res

"""## **GetHullValues:**

*   **Input:**
  1. **1D array of tuples** representing the convex hull points.

*   **Output:**
  1. **1D array** representing the hull values for each color.
  
*   **Description:**
  * Here we get the hull values according to the equation of region which you
can get using the equation of the straight line: *y=mx+c*.
  * Get the *hull value* of each intensity by substituting in the line equation to get the *y* value (*representing the hull value*)
"""

def getHullValues(convexH):
  res = []
  size = convexH[len(convexH)-1][0] + 1
  for i in range(size):
    for j in range(len(convexH) - 1):
      x1, y1 = convexH[j]
      x2, y2 = convexH[j + 1]
      m = (y2 - y1)/(x2 - x1)
      c = y2 - (m * x2)
      if i >= x1 and i <= x2:
        res.append(m *  i + c)
        break
  return res

"""## **GetThreshold:**

*   **Input:**
  1. **1D array** representing the histogram.
  2. **1D array** representing the hull values.

*   **Output:**
  1. **The threshold** according to the convex hull criteria.
  
*   **Description:**
  * Here you take the hull values and the histogram values and apply the last
step in convex hull algorithm to get the threshold
"""

def getThreshold(hist, hullV):
  threshold = 0
  max = hullV[0] - hist[0]
  for i in range(len(hist)):
    if max < (hullV[i] - hist[i]):
      threshold = i
      max = hullV[i] - hist[i]
  return threshold

"""## **ApplyThresh:**

*   **Input:**
  1. **1D array** representing the histogram.
  2. **The Threshold** value.

*   **Output:**
  1. **2 1D arrays**  representing the histogram after splitting it below and above the threshold
  
*   **Description:**
  * The main aim of this function is to split the histogram into two arrays
representing the histogram of values below threshold and histogram of
values above threshold so that we can re-apply the thresholding once
again on the resulted histograms
"""

def applyThres(hist, thres):
  res1 = []
  res2 = []
  for i in range(len(hist)):
    if i < thres:
      res1.append(hist[i])
    else:
      res2.append(hist[i])
  return res1,res2

"""# Getting the Resulted Images:

## **drawImages:**

*   **Input:**
  1. **First Threshold** representing the lower threshold.
  2. **Second Threshold** representing the higher threshold.
  3. **Image** the image resulted from the corner detectors

*   **Output:**
  1. **3 images**  representing the original image after splitting it into three regions which are:
      * **lower region** which is the image below the threshold.
      * **mid region** which is the image between the 2 thresholds.
      * **higher region** which is the image above the higher threshold.
  
*   **Description:**
  * The main purpose of this image is to split the image into 3 images after getting all the work done and getting 2 thresholds from the resulted image of the corner detection so that we can divide the image into corners, detectors and flat regions.
"""

def drawImages(thresh1,thresh2,image):
  res1 = [[0 for x in range(len(image[0]))] for y in range(len(image))]
  res2 = [[0 for x in range(len(image[0]))] for y in range(len(image))]
  res3 = [[0 for x in range(len(image[0]))] for y in range(len(image))]
  for i in range(1,len(image)-1):
    for j in range(1,len(image[0])-1):
      if(image[i][j]<thresh1):
        res1[i][j] = image[i][j]

        res1[i-1][j-1] = 255
        res1[i-1][j] = 255
        res1[i-1][j-1] = 255
        res1[i][j-1] = 255
        res1[i][j+1] = 255
        res1[i+1][j-1] = 255
        res1[i+1][j] = 255
        res1[i+1][j+1] = 255
      elif image[i][j] >= thresh1 and image[i][j] <thresh2:
        res2[i][j] = image[i][j]
      elif image[i][j] >=thresh2:
        res3[i][j] = image[i][j]
  return res1,res2,res3

"""# Testing Scenarios:

## Example Images

### First Example Image:


*   **t = 50**
"""

# Call your Functions Below and keep the same format for showing the output:
# Save your resulted images in variables im1, im2, and im3 so that you don't change the parameters
resS = Susan(ex_im1_arr, 50)
histResS = CalcHistSusan(resS, resS.shape)
second_Thres = getThreshold(histResS, getHullValues(getHull(histResS)))
histResS1, _ = applyThres(histResS, second_Thres)
first_Thres = getThreshold(histResS1, getHullValues(getHull(histResS1)))
im1_S, im2_S, im3_S = drawImages(first_Thres, second_Thres, resS)


con, min, max = Harris(ex_im1_arr, 0.04)
con = contrastStretch(con, 0, 255, min, max)
histH = CalcHistHarris(con)
second_ThresH = getThreshold(histH, getHullValues(getHull(histH)))
histResH1, _ = applyThres(histH, second_ThresH)
first_ThresH = getThreshold(histResH1, getHullValues(getHull(histResH1)))
im1, im2, im3 = drawImages(first_ThresH, second_ThresH, con)

print("Susan's Thresholds: ",first_Thres,second_Thres)
plt.plot(histResS)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(resS, cmap='gray')
s = 'Original Susan Image '
plt.title(s)

plt.subplot(1, 4, 2)
plt.imshow(im1_S, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2_S, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3_S, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)
plt.show()

# ================================================================================================

print("Harris's Thresholds: ",first_ThresH,second_ThresH)
print("Min = ",min,"Max = ",max)
plt.plot(histH)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(con, cmap='gray')
plt.title('Original Harris Image')

plt.subplot(1, 4, 2)
plt.imshow(im1, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)

"""### Second Example Image:

* **t = 2**
"""

# Call your Functions Below and keep the same format for showing the output:
# Save your resulted images in variables im1, im2, and im3 so that you don't change the parameters
resS = Susan(ex_im2_arr, 2)
histResS = CalcHistSusan(resS, resS.shape)
second_Thres = getThreshold(histResS, getHullValues(getHull(histResS)))
histResS1, _ = applyThres(histResS, second_Thres)
first_Thres = getThreshold(histResS1, getHullValues(getHull(histResS1)))
im1_S, im2_S, im3_S = drawImages(first_Thres, second_Thres, resS)


con, min, max = Harris(ex_im2_arr, 0.04)
con = contrastStretch(con, 0, 255, min, max)
histH = CalcHistHarris(con)
second_ThresH = getThreshold(histH, getHullValues(getHull(histH)))
histResH1, _ = applyThres(histH, second_ThresH)
first_ThresH = getThreshold(histResH1, getHullValues(getHull(histResH1)))
im1, im2, im3 = drawImages(first_ThresH, second_ThresH, con)

print("Susan's Thresholds: ",first_Thres,second_Thres)
plt.plot(histResS)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(resS, cmap='gray')
s = 'Original Susan Image '
plt.title(s)

plt.subplot(1, 4, 2)
plt.imshow(im1_S, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2_S, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3_S, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)
plt.show()

# ================================================================================================

print("Harris's Thresholds: ",first_ThresH,second_ThresH)
print("Min = ",min,"Max = ",max)
plt.plot(histH)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(con, cmap='gray')
plt.title('Original Harris Image')

plt.subplot(1, 4, 2)
plt.imshow(im1, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)

"""## **Test Images**

### First Test Image:


*   **t = 102**
"""

# Call your Functions Below and keep the same format for showing the output:
# Save your resulted images in variables im1, im2, and im3 so that you don't change the parameters
resS = Susan(test_im1_arr, 102)
histResS = CalcHistSusan(resS, resS.shape)
second_Thres = getThreshold(histResS, getHullValues(getHull(histResS)))
histResS1, _ = applyThres(histResS, second_Thres)
first_Thres = getThreshold(histResS1, getHullValues(getHull(histResS1)))
im1_S, im2_S, im3_S = drawImages(first_Thres, second_Thres, resS)


con, min, max = Harris(test_im1_arr, 0.04)
con = contrastStretch(con, 0, 255, min, max)
histH = CalcHistHarris(con)
second_ThresH = getThreshold(histH, getHullValues(getHull(histH)))
histResH1, _ = applyThres(histH, second_ThresH)
first_ThresH = getThreshold(histResH1, getHullValues(getHull(histResH1)))
im1, im2, im3 = drawImages(first_ThresH, second_ThresH, con)

print("Susan's Thresholds: ",first_Thres,second_Thres)
plt.plot(histResS)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(resS, cmap='gray')
s = 'Original Susan Image '
plt.title(s)

plt.subplot(1, 4, 2)
plt.imshow(im1_S, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2_S, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3_S, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)
plt.show()

# ================================================================================================

print("Harris's Thresholds: ",first_ThresH,second_ThresH)
print("Min = ",min,"Max = ",max)
plt.plot(histH)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(con, cmap='gray')
plt.title('Original Harris Image')

plt.subplot(1, 4, 2)
plt.imshow(im1, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)

"""### Second Test Image:


*   **t = 75**


"""

# Call your Functions Below and keep the same format for showing the output:
# Save your resulted images in variables im1, im2, and im3 so that you don't change the parameters
resS = Susan(test_im2_arr, 75)
histResS = CalcHistSusan(resS, resS.shape)
second_Thres = getThreshold(histResS, getHullValues(getHull(histResS)))
histResS1, _ = applyThres(histResS, second_Thres)
first_Thres = getThreshold(histResS1, getHullValues(getHull(histResS1)))
im1_S, im2_S, im3_S = drawImages(first_Thres, second_Thres, resS)


con, min, max = Harris(test_im2_arr, 0.04)
con = contrastStretch(con, 0, 255, min, max)
histH = CalcHistHarris(con)
second_ThresH = getThreshold(histH, getHullValues(getHull(histH)))
histResH1, _ = applyThres(histH, second_ThresH)
first_ThresH = getThreshold(histResH1, getHullValues(getHull(histResH1)))
im1, im2, im3 = drawImages(first_ThresH, second_ThresH, con)

print("Susan's Thresholds: ",first_Thres,second_Thres)
plt.plot(histResS)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(resS, cmap='gray')
s = 'Original Susan Image '
plt.title(s)

plt.subplot(1, 4, 2)
plt.imshow(im1_S, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2_S, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3_S, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)
plt.show()

# ================================================================================================

print("Harris's Thresholds: ",first_ThresH,second_ThresH)
print("Min = ",min,"Max = ",max)
plt.plot(histH)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(con, cmap='gray')
plt.title('Original Harris Image')

plt.subplot(1, 4, 2)
plt.imshow(im1, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)

"""### Third Test Image:


*   **t = 35**


"""

# Call your Functions Below and keep the same format for showing the output:
# Save your resulted images in variables im1, im2, and im3 so that you don't change the parameters
resS = Susan(test_im3_arr, 35)
histResS = CalcHistSusan(resS, resS.shape)
second_Thres = getThreshold(histResS, getHullValues(getHull(histResS)))
histResS1, _ = applyThres(histResS, second_Thres)
first_Thres = getThreshold(histResS1, getHullValues(getHull(histResS1)))
im1_S, im2_S, im3_S = drawImages(first_Thres, second_Thres, resS)


con, min, max = Harris(test_im3_arr, 0.04)
con = contrastStretch(con, 0, 255, min, max)
histH = CalcHistHarris(con)
second_ThresH = getThreshold(histH, getHullValues(getHull(histH)))
histResH1, _ = applyThres(histH, second_ThresH)
first_ThresH = getThreshold(histResH1, getHullValues(getHull(histResH1)))
im1, im2, im3 = drawImages(first_ThresH, second_ThresH, con)

print("Susan's Thresholds: ",first_Thres,second_Thres)
plt.plot(histResS)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(resS, cmap='gray')
s = 'Original Susan Image '
plt.title(s)

plt.subplot(1, 4, 2)
plt.imshow(im1_S, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2_S, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3_S, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)
plt.show()

# ================================================================================================

print("Harris's Thresholds: ",first_ThresH,second_ThresH)
print("Min = ",min,"Max = ",max)
plt.plot(histH)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(con, cmap='gray')
plt.title('Original Harris Image')

plt.subplot(1, 4, 2)
plt.imshow(im1, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)

"""### Forth Test Image:


*   **t = 65**


"""

# Call your Functions Below and keep the same format for showing the output:
# Save your resulted images in variables im1, im2, and im3 so that you don't change the parameters
resS = Susan(test_im4_arr, 65)
histResS = CalcHistSusan(resS, resS.shape)
second_Thres = getThreshold(histResS, getHullValues(getHull(histResS)))
histResS1, _ = applyThres(histResS, second_Thres)
first_Thres = getThreshold(histResS1, getHullValues(getHull(histResS1)))
im1_S, im2_S, im3_S = drawImages(first_Thres, second_Thres, resS)


con, min, max = Harris(test_im4_arr, 0.04)
con = contrastStretch(con, 0, 255, min, max)
histH = CalcHistHarris(con)
second_ThresH = getThreshold(histH, getHullValues(getHull(histH)))
histResH1, _ = applyThres(histH, second_ThresH)
first_ThresH = getThreshold(histResH1, getHullValues(getHull(histResH1)))
im1, im2, im3 = drawImages(first_ThresH, second_ThresH, con)

print("Susan's Thresholds: ",first_Thres,second_Thres)
plt.plot(histResS)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(resS, cmap='gray')
s = 'Original Susan Image '
plt.title(s)

plt.subplot(1, 4, 2)
plt.imshow(im1_S, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2_S, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3_S, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)
plt.show()

# ================================================================================================

print("Harris's Thresholds: ",first_ThresH,second_ThresH)
print("Min = ",min,"Max = ",max)
plt.plot(histH)

plt.figure(figsize=(20, 5))

plt.subplot(1, 4, 1)
plt.imshow(con, cmap='gray')
plt.title('Original Harris Image')

plt.subplot(1, 4, 2)
plt.imshow(im1, cmap='gray')
plt.title('below lower threshold')
plt.subplot(1, 4, 3)
plt.imshow(im2, cmap='gray')
plt.title('between the 2 thresholds')

plt.subplot(1, 4, 4)
plt.imshow(im3, cmap='gray')
plt.title('above higher threshold')

plt.subplots_adjust(wspace=0.5)
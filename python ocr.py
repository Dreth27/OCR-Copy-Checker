import cv2
from PIL import Image
import pytesseract
import numpy as np
from PIL import Image
import os
import threading
import time


with open("D:\Downloads\Python_OCR\input\path.txt", 'r', encoding='utf-8') as f:
    file_contents = f.read()


im_file = file_contents



im = Image.open(im_file)
im.save("D:\Downloads\Python_OCR\output\page_01.png")

import matplotlib
from matplotlib import pyplot as plt
image_path = im_file

img = cv2.imread(image_path)


def display(im_path):
  dpi = 80
  im_data = plt.imread(im_path)

  height, width = im_data.shape[:2]

  figsize = width / float(dpi), height / float(dpi)

  fig = plt.subplots(figsize=figsize)
  ax = fig.add_subplot(111)

  ax.axis('off')

  ax.imshow(im_data, cmap='gray')

  plt.show()






inverted_image = cv2.bitwise_not(img)
cv2.imwrite("D:\Downloads\Python_OCR\output\inverted.png", inverted_image)



##Binarization

def grayscale(image):
  return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


gray_image = grayscale(img)
cv2.imwrite("D:\Downloads\Python_OCR\output\gray.png", gray_image)




## Thresholding

thresh, bwimage = cv2.threshold(gray_image, 210, 230, cv2.THRESH_BINARY)
cv2.imwrite("D:\\Downloads\\Python_OCR\\output\\black_image.png", bwimage)




## Noise removal

def noise_removal(image):
  kernel = np.ones((1, 1), np.uint8)
  image = cv2.dilate(image, kernel, iterations=1)
  kernel = np.ones((1, 1), np.uint8)
  image = cv2.erode(image, kernel, iterations=1)
  image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
  image = cv2.medianBlur(image, 3)
  return (image)
no_noise = noise_removal(bwimage)
cv2.imwrite("D:\\Downloads\\Python_OCR\\output\\no_noise.png", no_noise)




## Errosion

def thin_font(image):
  image = cv2.bitwise_not(image)
  kernel = np.ones((2,2),np.uint8)
  image = cv2.erode(image, kernel, iterations=1)
  image = cv2.bitwise_not(image)
  return (image)


eroded_image = thin_font(no_noise)
cv2.imwrite("D:\\Downloads\\Python_OCR\\output\\eroded_image.png", eroded_image)


## Dilation 

def thick_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((2,2),np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return (image)


dilated_image = thick_font(no_noise)
cv2.imwrite("D:\\Downloads\\Python_OCR\output\\dilated_image.png", dilated_image)


## Deskewing

new = cv2.imread(file_contents)

def getSkewAngle(cvImage) -> float:
    newImage = cvImage.copy()
    gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

   
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=2)

    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    for c in contours:
        rect = cv2.boundingRect(c)
        x,y,w,h = rect
        cv2.rectangle(newImage,(x,y),(x+w,y+h),(0,255,0),2)

    largestContour = contours[0]
    print (len(contours))
    minAreaRect = cv2.minAreaRect(largestContour)
    cv2.imwrite("D:\\Downloads\\Python_OCR\\output\\boxes.png", newImage)
    angle = minAreaRect[-1]
    if angle < -45:
        angle = 90 + angle
    return -1.0 * angle

def rotateImage(cvImage, angle: float):
    newImage = cvImage.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage



def deskew(cvImage):
    angle = getSkewAngle(cvImage)
    return rotateImage(cvImage, -1.0 * angle)


fixed = deskew(new)
cv2.imwrite("D:\\Downloads\\Python_OCR\\output\\rotated_fixed.png", fixed)


## Removing borders 

def remove_borders(image):
    contours, heiarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntsSorted = sorted(contours, key=lambda x:cv2.contourArea(x))
    cnt = cntsSorted[-1]
    x, y, w, h = cv2.boundingRect(cnt)
    crop = image[y:y+h, x:x+w]
    return (crop)
no_borders = remove_borders(no_noise)
cv2.imwrite("D:\\Downloads\\Python_OCR\\output\\no_borders.png", no_borders)


## Adding border

color = [255, 255, 255]
top, bottom, left, right = [150]*4
image_with_border = cv2.copyMakeBorder(no_borders, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
cv2.imwrite("D:\\Downloads\\Python_OCR\\output\\image_with_border.png", image_with_border)


##output 

import pytesseract
from PIL import Image

img_file = im_file
no_noise = "D:\\Downloads\\Python_OCR\\output\\no_noise.png"


# Perform OCR and get confidence data
data = pytesseract.image_to_data(Image.open(img_file), output_type=pytesseract.Output.DICT)

# Initialize variables for overall confidence calculation
total_confidence = 0
word_count = 0

# Iterate through the data to calculate the overall confidence
for i in range(len(data['text'])):
    # Skip empty words
    if data['text'][i].strip():
        total_confidence += int(data['conf'][i])
        word_count += 1

# Calculate the overall confidence
if word_count > 0:
    overall_confidence = total_confidence / word_count
else:
    overall_confidence = 0

# Print the overall confidence in percentage
print(f"Overall Confidence: {overall_confidence:.2f}%")

# Save the OCR output and confidence level to a text file




ocr_result = pytesseract.image_to_string(img)

print (ocr_result)

# Save the OCR output to a text file
output_file = open('D:\\Downloads\\Python_OCR\\output.txt', 'w')
ocr_result = pytesseract.image_to_string(Image.open(img_file))
output_file.write(f"OCR Result:\n{ocr_result}\n\nOverall Confidence: {overall_confidence:.2f}%")
output_file.close()

## delete after output
output_folder_path = os.path.join('D:', 'Downloads', 'Python_OCR', 'output')

# Wait for 15 seconds
#time.sleep(15)

# Delete all files and folders in the output folder
for root, dirs, files in os.walk(output_folder_path):
    for file in files:
        os.remove(os.path.join(root, file))
    for dir in dirs:
        os.rmdir(os.path.join(root, dir))



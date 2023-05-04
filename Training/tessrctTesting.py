import cv2
import numpy as np
import pytesseract

MIN_CONTOUR_AREA = 400
RESIZED_IMAGE_WIDTH = 20
RESIZED_IMAGE_HEIGHT = 30

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load the input image
import os
dirname = os.path.dirname(__file__)
img = cv2.imread(os.path.join(dirname, "two.png"))

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to binarize the image
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Find contours in the image
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate over the contours and find the bounding box of each contour
for contour in contours:
    area = cv2.contourArea(contour)
    if area > MIN_CONTOUR_AREA:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Crop the image to the bounding box
        number_plate_img = gray[y:y+h, x:x+w]

        # Resize the image to a fixed size
        resized_img = cv2.resize(number_plate_img, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

        # Threshold the image to make it binary
        ret, thresh_img = cv2.threshold(resized_img, 127, 255, cv2.THRESH_BINARY)

        # Find contours in the image
        contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate over the contours and recognize the text using Tesseract
        classifications = []
        flattened_images = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 10 and h > 10:
                # Extract the letter from the image
                letter_img = thresh_img[y:y+h, x:x+w]

                # Resize the letter to a fixed size
                letter_img = cv2.resize(letter_img, (RESIZED_IMAGE_WIDTH, RESIZED_IMAGE_HEIGHT))

                # Flatten the image into a 1D array
                flattened_image = letter_img.reshape((1, RESIZED_IMAGE_WIDTH * RESIZED_IMAGE_HEIGHT)).astype(np.float32)

                # Recognize the letter using Tesseract
                letter = pytesseract.image_to_string(letter_img, config='--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

                # Print the recognized letter and add it to the classifications and flattened_images arrays
                print('Recognized letter:', letter)
                classifications.append(ord(letter))
                flattened_images.append(flattened_image)

        # Save the classifications and flattened images to files
        np.savetxt('nclassifications.txt', classifications, fmt='%d')
        np.savetxt('nflattened_images.txt', flattened_images, fmt='%d')

        # Show the output image with the bounding boxes and recognized letters
        cv2.imshow('Output', img)
        cv2.waitKey(0)

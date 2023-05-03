import os
from Display import results
# Load test set of images and ground truth labels
test_images = ['honda.jpg','redcar.jpg', 'skoda.jpg', 'scooter.jpg']
test_labels = ['AAB0205','BAA4777', 'BAB9128', 'AAA4253']
dirname = os.path.dirname(__file__)
# img_path = os.path.join("LPD-KNN-PYTHON", "LicPlateImages", "Testing", "10.png")
# print(img_path)


# Initialize variables to keep track of correct and total predictions
correct_preds = 0
total_preds = 0
# Loop through each image in the test set
for i in range(len(test_images)):
    # Detect license plate in image
    img_path = os.path.join(dirname, "LicPlateImages", "Testing",test_images[i])
    if(os.path.exists(img_path)):
        detected_plate = results(img_path)
        print("detected" , detected_plate)
        # Compare detected plate with ground truth label
        if detected_plate == test_labels[i]:
            correct_preds += 1
        
        total_preds += 1

# Compute accuracy
accuracy = (correct_preds / total_preds) * 100
print('Accuracy:', accuracy, '%')

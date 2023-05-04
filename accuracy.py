import os
from Display import results
# Load test set of images and ground truth labels
imageLabels = {
    'honda.jpg': 'AAB0205',
    'redcar.jpg' : 'BAA4777',
    'skoda.jpg' : 'BAB9128',
    'scooter.jpg' : 'AAA4253',
}

dirname = os.path.dirname(__file__)
# img_path = os.path.join("LPD-KNN-PYTHON", "LicPlateImages", "Testing", "10.png")
# print(img_path)


# Initialize variables to keep track of correct and total predictions
correct_preds = 0
total_preds = 0
# Loop through each image in the test set
for img, label in imageLabels.items():
    # Detect license plate in image
    img_path = os.path.join(dirname, "LicPlateImages", "Testing", img)
    if(os.path.exists(img_path)):
        detected_plate = results(img_path)
        print("detected" , detected_plate)
        # Compare detected plate with ground truth label
        if detected_plate == label:
            correct_preds += 1
        total_preds += 1


# Compute accuracy
accuracy = (correct_preds / total_preds) * 100
print('Accuracy:', accuracy, '%')

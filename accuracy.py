import os
from Display import results
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load test set of images and ground truth labels
imageLabels = {
    'honda.jpg': 'AAB0205',
    'redcar.jpg' : 'BAA4777', #right one is 777
    'skoda.jpg' : 'BAB9128',
    'scooter.jpg' : 'AAA4253',
}

dirname = os.path.dirname(__file__)

# Initialize variables to keep track of correct and total predictions
correct_preds = 0
total_preds = 0

# Initialize variables for true positives (TP), false positives (FP), and false negatives (FN)
TP = 0
FP = 0
FN = 0

# Initialize lists for true labels and predicted labels
y_true = []
y_pred = []

# Loop through each image in the test set
for img, label in imageLabels.items():
    # Detect license plate in image
    img_path = os.path.join(dirname, "LicPlateImages", "Testing", img)
    if(os.path.exists(img_path)):
        detected_plate = results(img_path)
        print("detected" , detected_plate)
        
        # Add the true label and predicted label to the respective lists
        y_true.append(label)
        y_pred.append(detected_plate)

        # Compare detected plate with ground truth label
        if detected_plate == label:
            TP += 1
        else:
            FP += 1
        total_preds += 1

# Compute false negatives (assuming all other plates in the dataset are ground truth negatives)
FN = len(imageLabels) - TP

# Compute accuracy, precision, recall, and F1 score
accuracy = (TP / total_preds) * 100
precision = TP / (TP + FP)
recall = TP / (TP + FN)
f1_score = 2 * ((precision * recall) / (precision + recall))

print('--------------------------------------')
print('Accuracy:', accuracy, '%')
print('Precision:', precision)
print('Recall:', recall)
print('F1 score:', f1_score)

# Confusion matrix
cm = confusion_matrix(y_true, y_pred, labels=list(imageLabels.values()))

# Print confusion matrix as text
print('Confusion Matrix:')
print('Predicted: ', ' '.join(imageLabels.values()))
for i, row_label in enumerate(imageLabels.values()):
    print('True', row_label, ': ', ' '.join(str(x) for x in cm[i]))

# Plotting
plt.figure(figsize=(10,7))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=list(imageLabels.values()), yticklabels=list(imageLabels.values()))
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

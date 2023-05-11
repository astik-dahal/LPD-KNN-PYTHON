import os
import imgaug.augmenters as iaa
import cv2
from Display import results
import matplotlib.pyplot as plt

# Load test set of images and ground truth labels
imageLabels = {
    'honda.jpg': 'AAB0205',
    'redcar.jpg' : 'BAA4770',
    'skoda.jpg' : 'BAB9128',
    'scooter.jpg' : 'AAA4253',
}

# Split dataset into training and test sets (change the proportions as needed)
train_imageLabels = {k: v for i, (k, v) in enumerate(imageLabels.items()) if i % 2 == 0}
test_imageLabels = {k: v for i, (k, v) in enumerate(imageLabels.items()) if i % 2 == 1}

# Data augmentation
seq = iaa.Sequential([
    iaa.Fliplr(0.5),
    iaa.Affine(rotate=(-10, 10), scale=(0.9, 1.1))
])

dirname = os.path.dirname(__file__)
augmented_train_imageLabels = {}

# Display the original and augmented images side by side
for original_img, label in train_imageLabels.items():
    original_img_path = os.path.join(dirname, "LicPlateImages", "Training", original_img)
    original_image = cv2.imread(original_img_path)

    for i in range(5):
        augmented_img_name = f"{original_img.split('.')[0]}_aug_{i}.jpg"
        augmented_img_path = os.path.join(dirname, "LicPlateImages", "Training", augmented_img_name)
        augmented_image = cv2.imread(augmented_img_path)

        # Convert the images from BGR to RGB (used by Matplotlib)
        original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        augmented_image_rgb = cv2.cvtColor(augmented_image, cv2.COLOR_BGR2RGB)

        # Display the images
        fig, axes = plt.subplots(1, 2)
        axes[0].imshow(original_image_rgb)
        axes[0].set_title('Original Image')
        axes[1].imshow(augmented_image_rgb)
        axes[1].set_title(f'Augmented Image {i+1}')

        plt.show()

train_imageLabels.update(augmented_train_imageLabels)
print(train_imageLabels)
print(test_imageLabels)
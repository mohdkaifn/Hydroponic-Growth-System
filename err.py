import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
import serial

# Load the trained model
model = tf.keras.models.load_model(r"C:\datas\projects\final_yr_project\spinach\spinach\model_v1.h5")

def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        # Display the uploaded image
        image = Image.open(file_path)
        image = image.resize((300, 300))  # Resize the image if needed
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
        
        # Perform prediction and send status to Arduino
        prediction(file_path)

def prediction(img_path):
    class_names = ['Early_blight', 'Healthy', 'Late_blight']

    # Load and preprocess the image
    my_image = load_img(img_path, target_size=(128, 128))
    my_image = img_to_array(my_image)
    my_image = np.expand_dims(my_image, 0)

    # Perform prediction using the loaded model
    out = np.round(model.predict(my_image)[0], 2)

    # Convert prediction result to 0 or 1 based on disease detection
    # if out[1] == max(out):
    #     disease_status = 0
    #     print("Healthy")
    # else:
    #     disease_status = 1
    #     print("Disease Detected")

    # Send disease status to Arduino
    # ser.write(str(disease_status).encode())
    # print(f"Disease status sent to Arduino: {disease_status}")

    # Plot the prediction (optional)
    # plot_prediction(out)

def plot_prediction(out):
    class_names = ['Early_blight', 'Healthy', 'Late_blight']
    fig = plt.figure(figsize=(7, 4))
    plt.barh(class_names, out, color='lightgray', edgecolor='red', linewidth=1, height=0.5)

    for index, value in enumerate(out):
        plt.text(value / 2 + 0.1, index, f"{100 * value:.2f}%", fontweight='bold')

    plt.xticks([])
    plt.yticks([0, 1, 2], labels=class_names, fontweight='bold', fontsize=14)
    plt.tight_layout()
    plt.show()

# Create Tkinter window
root = tk.Tk()
root.title('Image Uploader')

# Create button to upload image
upload_button = tk.Button(root, text="Upload Image", command=upload_image)
upload_button.pack(pady=10)

# Create label to display uploaded image
label = tk.Label(root)
label.pack()

# Initialize Serial Communication
# ser = serial.Serial('COM3', 9600)  # Change 'COM10' to your Arduino port

root.mainloop()

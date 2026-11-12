import math
import cv2
import subprocess
import numpy as np
import os 

def compute_brightness(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray_image)
    return brightness

def adjust_contrast_exposure(image, brightness_threshold=105):
    brightness = compute_brightness(image)
    print(brightness)
    exposure_adjustment = -31  # Decrease exposure by reducing brightness
    contrast_adjustment = 1.5  # Increase contrast

    if brightness < brightness_threshold:
        print('Pass')
        adjusted_image = cv2.convertScaleAbs(image, alpha=1, beta=exposure_adjustment)
        # adjusted_image = cv2.addWeighted(adjusted_image, contrast_adjustment, adjusted_image, 0, 0)
        return adjusted_image
    else:
        print('Not Pass')
        return image

def handle_img(inp_image_path,output_image_path):
    image = cv2.imread(inp_image_path)
    if image is None:
        print(f"Unable to load image from {inp_image_path}")
    else:
        adjusted_image = adjust_contrast_exposure(image)
        cv2.imwrite(output_image_path, adjusted_image)

def calculate_mean_values(image_path, min_luminance, min_rgb, max_rgb):
    # Read the conjunctiva image
    conjunctiva_image = cv2.imread(image_path)
    
    # Split the image into its RGB channels
    b, g, r = cv2.split(conjunctiva_image)
    
    # Calculate mean values of R, G, and B components
    mean_r = np.mean(r)
    mean_g = np.mean(g)
    mean_b = np.mean(b)
    
    return mean_r, mean_g, mean_b


def detect_anemia():
    inp_image_path = 'input_img/input_img.jpg'
    output_image_path = 'edit_img/edit_img.jpg'
    handle_img(inp_image_path, output_image_path)

    yolo_script_path = 'yolov5/detect.py'

    command = f"python {yolo_script_path} --source {inp_image_path} --weights yolov5/runs/train/exp/weights/best.pt --conf 0.25" 
    os.system(command) 
    
    image_path = 'output_img/output.jpg' 

    min_luminance = 0
    min_rgb = 0
    max_rgb = 255

    mean_r, mean_g, mean_b = calculate_mean_values(image_path, min_luminance, min_rgb, max_rgb)
    val1 = (-1.922 + 0.206 * mean_r - 0.241 * mean_g + 0.012 * mean_b)
    Num = math.exp(val1)
    Den = 1 + math.exp(val1)
    L = Num / Den
    add_value = 3
    if (L * 10 + add_value) < 6:
        Hgb_val = 10
    else:
        Hgb_val = (L * 10 + add_value)
    print("\n Hgb = ", round(Hgb_val, 2), "g/dl")
    temp = round(Hgb_val, 2)
    print(temp)
    return temp
    """ if Hgb_val < 12:  # A Threshold value I have used on the basis of data available to me
        print("\nAnemic")
    else:
        print("\nNon-Anemic") """

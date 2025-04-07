# Author        : CHAN Cheuk Hei
# Student Name  : CHAN Cheuk Hei
# Student ID    : 57270778
# Usage         : Testing   - Check Duplicate Image base on Color Histogram

import cv2
import numpy as np
import os

def calculate_histogram(image):
    # Convert the image to the HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Calculate the histogram for each channel
    hist_h = cv2.calcHist([hsv_image], [0], None, [256], [0, 256])
    hist_s = cv2.calcHist([hsv_image], [1], None, [256], [0, 256])
    hist_v = cv2.calcHist([hsv_image], [2], None, [256], [0, 256])
    
    # Normalize the histograms
    hist_h = cv2.normalize(hist_h, hist_h)
    hist_s = cv2.normalize(hist_s, hist_s)
    hist_v = cv2.normalize(hist_v, hist_v)
    
    return hist_h, hist_s, hist_v

def compare_histograms(hist1, hist2):
    score = 0
    for h1, h2 in zip(hist1, hist2):
        score += cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)
    return score / len(hist1)

def find_duplicate_images(directory, threshold=0.95, output_file="similarity_scores.txt"):
    image_files = [f for f in os.listdir(directory) if f.endswith(".jpg")]
    histograms = {}
    duplicates = []
    checked_pairs = set()

    for i, filename in enumerate(image_files):
        filepath = os.path.join(directory, filename)
        try:
            image = cv2.imread(filepath)
            histograms[filename] = calculate_histogram(image)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

    with open(output_file, "w") as file:
        for i, filename1 in enumerate(image_files):
            for j, filename2 in enumerate(image_files):
                if i >= j:
                    continue
                pair = tuple(sorted([filename1, filename2]))
                if pair in checked_pairs:
                    continue
                checked_pairs.add(pair)

                similarity_score = compare_histograms(histograms[filename1], histograms[filename2])
                if similarity_score >= threshold:
                    duplicates.append((filename1, filename2, similarity_score))
                    file.write(f"{filename1} is similar to {filename2} with similarity score {similarity_score * 100:.2f}%\n")

    return duplicates

if __name__ == "__main__":
    directory = "E:\FYP\dataset\disease_v2\leaf_yellowing"
    duplicates = find_duplicate_images(directory)

    if duplicates:
        print("Duplicate images found and saved to similarity_scores.txt")
    else:
        print("No duplicate images found.")

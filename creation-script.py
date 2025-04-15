#!/usr/bin/env python3
"""
Challenge Creation Script for "Hidden Depths" CTF

This script automates the creation of the image-based CTF challenge by:
1. Creating the necessary text files for clues and flags
2. Encoding ASCII values in the red channel
3. Adding EXIF metadata
4. Embedding hidden messages using steganography

Requirements:
- PIL/Pillow
- NumPy
- ExifTool installed on your system
- Steghide installed on your system
"""

import os
import subprocess
import sys
from PIL import Image
import numpy as np

def create_text_files():
    """Create the necessary text files for the challenge"""
    print("Creating text files...")
    
    with open("clue1.txt", "w") as f:
        f.write("The surface reveals nothing. Look deeper at layer 42, 42, 42 - RGB holds the key. But first, check what the camera saw.")
    
    with open("flag.txt", "w") as f:
        f.write("Congratulations! You've reached the deepest point. Your flag is: FLAG{D33P_S34_S3CR3TS_R3V34L3D}")
    
    print("Text files created successfully.")

def prepare_image(input_image):
    """Prepare the image for the challenge"""
    print(f"Preparing image from {input_image}...")
    
    # Open the input image
    img = Image.open(input_image)
    
    # Convert to RGB if not already
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    # Save as PNG to avoid compression issues
    output_image = "challenge.png"
    img.save(output_image)
    
    print(f"Image prepared and saved as {output_image}")
    return output_image

def encode_neptune(image_path):
    """Encode 'NEPTUNE' in the red channel at position (42,42)"""
    print("Encoding 'NEPTUNE' in the red channel...")
    
    # Open the image
    img = Image.open(image_path)
    img_array = np.array(img)
    
    # ASCII values for "NEPTUNE"
    neptune_ascii = [78, 69, 80, 84, 85, 78, 69]
    
    # Starting position
    x, y = 42, 42
    
    # Make sure the coordinates are valid
    height, width, _ = img_array.shape
    if y >= height or x+6 >= width:
        print(f"Warning: Image is too small! Dimensions are {width}x{height}")
        print(f"Using coordinates (0,0) instead of ({x},{y})")
        x, y = 0, 0
    
    # Modify only the red channel at specific pixels
    for i, ascii_value in enumerate(neptune_ascii):
        # Get current pixel
        current_pixel = img_array[y, x + i].copy()
        
        # Only modify the red channel (index 0)
        current_pixel[0] = ascii_value
        
        # Set the modified pixel back
        img_array[y, x + i] = current_pixel
        
        # Print for verification
        print(f"Modified pixel at ({x + i}, {y}): R={ascii_value}, ASCII = {chr(ascii_value)}")
    
    # Convert back to an image and save
    modified_img = Image.fromarray(img_array)
    modified_img.save(image_path)
    
    print("Red channel encoding completed successfully.")

def add_exif_metadata(image_path):
    """Add EXIF metadata with the hex clue"""
    print("Adding EXIF metadata...")
    
    # The hex code spells "RED CHANNEL"
    hex_code = "52 45 44 20 43 48 41 4E 4E 45 4C"
    
    # Run exiftool to add metadata
    command = ["exiftool", f"-Comment=Coordinates of interest: {hex_code}", image_path]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("EXIF metadata added successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error adding EXIF metadata: {e}")
        print(f"Error output: {e.stderr}")
        return False

def embed_steghide(image_path, text_file, password, output_path=None):
    """Embed a text file using steghide"""
    if output_path is None:
        output_path = image_path
        
    print(f"Embedding {text_file} with password '{password}'...")
    
    # Run steghide to embed the file
    command = ["steghide", "embed", "-cf", image_path, "-ef", text_file, 
               "-sf", output_path, "-p", password, "-f"]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Successfully embedded {text_file}.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error embedding file: {e}")
        print(f"Error output: {e.stderr}")
        return False

def verify_challenge(image_path):
    """Verify that the challenge works as expected"""
    print("\nVerifying challenge...")
    
    # Check EXIF metadata
    print("\nChecking EXIF metadata...")
    try:
        result = subprocess.run(["exiftool", image_path], capture_output=True, text=True, check=True)
        if "Comment" in result.stdout and "52 45 44 20 43 48 41 4E 4E 45 4C" in result.stdout:
            print("✓ EXIF metadata verification passed.")
        else:
            print("✗ EXIF metadata verification failed.")
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error checking EXIF metadata: {e}")
    
    # Check red channel encoding
    print("\nChecking red channel encoding...")
    img = Image.open(image_path)
    img_array = np.array(img)
    message = ""
    for i in range(7):
        try:
            r_value = img_array[42, 42+i][0]
            message += chr(r_value)
            print(f"Pixel {i+1}: Red value = {r_value}, ASCII = {chr(r_value)}")
        except:
            print(f"Error reading pixel {i+1}")
    
    if message == "NEPTUNE":
        print(f"✓ Red channel verification passed. Message: {message}")
    else:
        print(f"✗ Red channel verification failed. Message: {message}")
    
    # Try extracting with steghide
    print("\nChecking steghide extraction with password 'dive'...")
    try:
        subprocess.run(["steghide", "extract", "-sf", image_path, "-p", "dive", "-xf", "clue1_test.txt", "-f"], 
                      capture_output=True, check=True)
        print("✓ First steghide layer extraction successful.")
    except subprocess.CalledProcessError as e:
        print(f"✗ First steghide layer extraction failed: {e}")
    
    print("\nChecking steghide extraction with password 'NEPTUNE'...")
    try:
        subprocess.run(["steghide", "extract", "-sf", image_path, "-p", "NEPTUNE", "-xf", "flag_test.txt", "-f"], 
                      capture_output=True, check=True)
        print("✓ Second steghide layer extraction successful.")
    except subprocess.CalledProcessError as e:
        print(f"✗ Second steghide layer extraction failed: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_challenge.py <input_image>")
        print("Example: python create_challenge.py base.jpg")
        sys.exit(1)
    
    input_image = sys.argv[1]
    
    if not os.path.exists(input_image):
        print(f"Error: Image file {input_image} not found.")
        sys.exit(1)
    
    # Create text files
    create_text_files()
    
    # Prepare the image
    challenge_image = prepare_image(input_image)
    
    # Encode NEPTUNE in the red channel
    encode_neptune(challenge_image)
    
    # Add EXIF metadata
    add_exif_metadata(challenge_image)
    
    # Embed first layer with steghide
    embed_steghide(challenge_image, "clue1.txt", "dive")
    
    # Embed final layer with steghide
    embed_steghide(challenge_image, "flag.txt", "NEPTUNE")
    
    # Verify the challenge
    verify_challenge(challenge_image)
    
    print("\nChallenge creation completed successfully!")
    print(f"Final challenge file: {challenge_image}")
    print("Remember to include only the challenge file in your distribution, not the source files.")

if __name__ == "__main__":
    main()

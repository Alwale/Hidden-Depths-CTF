#!/usr/bin/env python3
"""
Solution script for the "Hidden Depths" CTF challenge.
This script extracts values from the red channel at specified coordinates
and converts them to ASCII characters.
"""

from PIL import Image
import numpy as np
import argparse

def extract_message(image_path, x_start, y_start, length=7):
    """
    Extract a message from the red channel of an image starting at specific coordinates.
    
    Args:
        image_path (str): Path to the image file
        x_start (int): Starting x-coordinate
        y_start (int): Starting y-coordinate
        length (int): Number of pixels to read
        
    Returns:
        str: The decoded message
    """
    try:
        # Open the image
        img = Image.open(image_path)
        img_array = np.array(img)
        
        # Get image dimensions
        height, width = img_array.shape[:2]
        
        # Check if coordinates are valid
        if y_start >= height or x_start + length > width:
            print(f"Warning: Coordinates may be out of bounds!")
            print(f"Image dimensions: {width}x{height}")
            print(f"Requested coordinates: ({x_start},{y_start}) to ({x_start+length-1},{y_start})")
        
        # Extract red channel values
        red_values = []
        ascii_chars = []
        
        for i in range(length):
            try:
                # Get red channel value (index 0 in RGB)
                r_value = img_array[y_start, x_start + i][0]
                red_values.append(r_value)
                
                # Convert to ASCII character if in printable range
                if 32 <= r_value <= 126:  # Printable ASCII range
                    ascii_chars.append(chr(r_value))
                else:
                    ascii_chars.append('?')
            except IndexError:
                print(f"Error: Could not read pixel at ({x_start+i}, {y_start})")
                red_values.append(None)
                ascii_chars.append('?')
        
        # Create the message
        message = ''.join(ascii_chars)
        
        return red_values, message
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return [], ""

def main():
    parser = argparse.ArgumentParser(description='Extract hidden message from an image\'s red channel')
    parser.add_argument('image', help='Path to the image file')
    parser.add_argument('-x', '--x-start', type=int, default=42, help='Starting x-coordinate (default: 42)')
    parser.add_argument('-y', '--y-start', type=int, default=42, help='Starting y-coordinate (default: 42)')
    parser.add_argument('-l', '--length', type=int, default=7, help='Number of pixels to read (default: 7)')
    args = parser.parse_args()
    
    red_values, message = extract_message(args.image, args.x_start, args.y_start, args.length)
    
    print("\n=== Red Channel Analysis ===")
    print(f"Starting position: ({args.x_start}, {args.y_start})")
    print(f"Length: {args.length} pixels\n")
    
    if red_values:
        print("Pixel values:")
        for i, val in enumerate(red_values):
            if val is not None:
                print(f"Pixel {i+1}: Red value = {val}, ASCII = {chr(val) if 32 <= val <= 126 else '?'}")
        
        print("\nComplete message:", message)
    
if __name__ == "__main__":
    main()

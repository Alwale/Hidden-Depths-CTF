# "Hidden Depths" CTF Challenge - Solution Guide

This document provides the complete step-by-step solution for the "Hidden Depths" CTF challenge.

## Step 1: Extract First Hidden Message

Based on the underwater theme of the challenge, try using "dive" as the password for Steghide:

```bash
steghide extract -sf challenge.png -p "dive"
```

This extracts a file named "clue1.txt" containing:
```
The surface reveals nothing. Look deeper at layer 42, 42, 42 - RGB holds the key. Check the RED CHANNEL for what lies beneath.
```

This clue points to:
1. Pixel coordinates (42, 42)
2. Looking at the RED CHANNEL values

## Step 2: Analyze Red Channel Values

There are multiple ways to analyze the red channel values at coordinates (42,42):

### Option 1: Using a Python Script

```bash
python3 extract_red_channel.py challenge.png -x 42 -y 42 -l 7
```

### Option 2: Using GIMP

1. Open the image in GIMP
2. Zoom in to coordinates (42,42)
3. Use the Color Picker tool on each pixel
4. Note the R value for each pixel

### Option 3: Using ImageMagick

```bash
for i in {0..6}; do
  x=$((42+i))
  identify -format "Pixel ($x,42): %[pixel:p{$x,42}]\n" challenge.png
done
```

All methods will reveal these red channel values:

| Pixel | Red Value | ASCII Character |
|-------|-----------|-----------------|
| 1     | 78        | N               |
| 2     | 69        | E               |
| 3     | 80        | P               |
| 4     | 84        | T               |
| 5     | 85        | U               |
| 6     | 78        | N               |
| 7     | 69        | E               |

The complete message is: `NEPTUNE`

## Step 3: Extract Final Flag

Use the discovered word "NEPTUNE" as the password for another Steghide extraction:

```bash
steghide extract -sf challenge.png -p "NEPTUNE"
```

This extracts a file named "flag.txt" containing the final flag:
```
Congratulations! You've reached the deepest point. Your flag is: FLAG{D33P_S34_S3CR3TS_R3V34L3D}
```

## Summary of Tools Used

1. **Steghide** - For extracting hidden messages from the image
2. **Image Analysis Tools** - Any of the following:
   - Python with PIL/NumPy
   - GIMP
   - Photoshop
   - ImageMagick
   - Stegsolve

## Conceptual Overview

This challenge incorporates multiple layers of steganography and forensic techniques:

1. **Basic Steganography** - Using Steghide with a thematic password ("dive")
2. **Pixel Manipulation** - Examining specific pixel values to extract hidden data
3. **ASCII Encoding** - Converting numeric values to text to reveal a password
4. **Multi-layer Security** - Using the output from one layer as the key to unlock the next

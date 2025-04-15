# "Hidden Depths" CTF Challenge - Solution Guide

This document provides the complete step-by-step solution for the "Hidden Depths" CTF challenge.

## Step 1: Analyze Image Metadata

The first step is to examine the image metadata using ExifTool:

```bash
exiftool challenge.png
```

In the output, look for the "Comment" field, which contains the following hex code:
```
52 45 44 20 43 48 41 4E 4E 45 4C
```

Convert this hex to ASCII:
```bash
echo "52 45 44 20 43 48 41 4E 4E 45 4C" | xxd -r -p
```

This reveals the message: `RED CHANNEL`

## Step 2: Extract First Hidden Message

Based on the underwater theme of the challenge, try using "dive" as the password for Steghide:

```bash
steghide extract -sf challenge.png -p "dive"
```

This extracts a file named "clue1.txt" containing:
```
The surface reveals nothing. Look deeper at layer 42, 42, 42 - RGB holds the key. But first, check what the camera saw.
```

This clue points to:
1. Pixel coordinates (42, 42)
2. Looking at the RGB values (with emphasis on R - Red channel from the hex message)

## Step 3: Analyze Red Channel Values

Using the provided Python script or writing your own:

```bash
python3 extract_red_channel.py challenge.png -x 42 -y 42 -l 7
```

This script extracts the red channel values at the specified coordinates and converts them to ASCII characters:

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

## Step 4: Extract Final Flag

Use the discovered word "NEPTUNE" as the password for another Steghide extraction:

```bash
steghide extract -sf challenge.png -p "NEPTUNE"
```

This extracts a file named "flag.txt" containing the final flag:
```
Congratulations! You've reached the deepest point. Your flag is: FLAG{D33P_S34_S3CR3TS_R3V34L3D}
```

## Summary of Tools Used

1. **ExifTool** - For examining image metadata
2. **Hex Decoder** - For converting hex to ASCII
3. **Steghide** - For extracting hidden messages from the image
4. **Python with PIL/NumPy** - For analyzing specific pixel values

## Conceptual Overview

This challenge incorporates multiple layers of steganography and forensic techniques:

1. **EXIF Metadata Analysis** - Finding hidden information in the image's metadata
2. **Basic Steganography** - Using common steganography tools with a thematic password
3. **Pixel Manipulation** - Examining specific pixel values to extract hidden data
4. **ASCII Encoding** - Converting numeric values to text to reveal a password
5. **Multi-layer Security** - Using the output from one layer as the key to unlock the next

The challenge demonstrates how information can be hidden within digital images in ways that aren't visible to the naked eye or basic analysis tools.

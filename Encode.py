from PIL import Image
import zlib
from collections import Counter, defaultdict


def image_to_ultra_compressed_text(input_image_path, output_text_path):
    """
    Converts an image into a highly compressed text file with common colors stored at the top of the file
    along with image dimensions. Uses run-length encoding for row compression and zlib for compression.
    """
    try:
        # Open the image
        img = Image.open(input_image_path)
        img = img.convert("RGB")  
        width, height = img.size

        color_count = Counter()

        # Process the image row by row
        for y in range(height):
            row = img.crop((0, y, width, y + 1)).getdata()
            color_count.update(row)

        # Sort the colors by frequency
        sorted_colors = [color for color, _ in color_count.most_common()]

        color_index = {color: index for index, color in enumerate(sorted_colors)}

        compressed_data = []

        compressed_data.append(f"{height} {width} {len(sorted_colors)}")

        for color in sorted_colors:
            compressed_data.append(to_hex(color))

        # Process each row and compress it using RLE
        for y in range(height):
            row = img.crop((0, y, width, y + 1)).getdata()
            indexed_row = [color_index[color] for color in row]
            compressed_row = compress_row(indexed_row)
            compressed_data.append(compressed_row)

        # Join the data into a single string and compress it using zlib
        data_string = "\n".join(compressed_data)
        compressed_string = zlib.compress(data_string.encode('ascii'), level=9)

        # Save to file
        with open(output_text_path, 'wb') as f:
            f.write(compressed_string)

        print(f"Image successfully processed to ultra-compressed text: {output_text_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def to_hex(color):
    """Converts (R, G, B) to RRGGBB format."""
    return f"{color[0]:02X}{color[1]:02X}{color[2]:02X}"

def compress_row(row):
    """
    Compresses a single row using run-length encoding (RLE).
    Format: run_length|color_index| for each run.
    """
    compressed_row = []
    count = 1
    prev_pixel = row[0]
    
    for i in range(1, len(row)):
        if row[i] == prev_pixel:
            count += 1
        else:
            compressed_row.append(f"{count}|{prev_pixel}|")
            prev_pixel = row[i]
            count = 1

    compressed_row.append(f"{count}|{prev_pixel}|")

    return "".join(compressed_row)

if __name__ == "__main__":
    input_image_path = "your_image.png"  # Replace with your image path
    output_text_path = "ultra_compressed_output_pixels.txt"
    image_to_ultra_compressed_text(input_image_path, output_text_path)

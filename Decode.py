from PIL import Image
import zlib

def ultra_compressed_text_to_image(input_text_path, output_image_path):
    """
    Decodes the ultra-compressed text file back into an image.
    """
    try:
        # Read the compressed file
        with open(input_text_path, 'rb') as f:
            compressed_data = f.read()

        # Decompress the data
        decompressed_string = zlib.decompress(compressed_data).decode('ascii')

        # Parse the decompressed data
        lines = decompressed_string.split("\n")
        height, width, num_colors = map(int, lines[0].split())
        
        # Extract the color palette
        sorted_colors = [hex_to_rgb(lines[i + 1]) for i in range(num_colors)]

        # Reconstruct the image row by row
        reconstructed_pixels = []
        for line in lines[1 + num_colors:]:
            if line.strip():  # Skip empty lines
                row = decompress_row(line, sorted_colors)
                reconstructed_pixels.extend(row)

        # Create the image
        img = Image.new("RGB", (width, height))
        img.putdata(reconstructed_pixels)
        img.save(output_image_path)

        print(f"Image successfully reconstructed: {output_image_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def hex_to_rgb(hex_color):
    """Converts RRGGBB format to (R, G, B)."""
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def decompress_row(compressed_row, palette):
    """
    Decompresses a single row using the run-length encoding (RLE) scheme.
    Format: run_length|color_index|.
    """
    row = []
    elements = compressed_row.split("|")  # Split by delimiter
    
    if len(elements) % 2 != 1:
        raise ValueError(f"Malformed RLE row: {compressed_row}")

    for i in range(0, len(elements) - 1, 2):
        run_length = int(elements[i])
        color_index = int(elements[i + 1])
        if 0 <= color_index < len(palette):
            row.extend([palette[color_index]] * run_length)
        else:
            raise ValueError(f"Invalid color index {color_index} in row: {compressed_row}")
    return row





# Example usage
if __name__ == "__main__":
    input_text_path = "compressed_output.txt"
    output_image_path = "reconstructed_image.png"  # Replace with desired output path
    ultra_compressed_text_to_image(input_text_path, output_image_path)

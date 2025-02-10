import os
from PIL import Image

def resize_and_crop_images(input_folder, output_folder, target_width, target_height):
    """
    Resize and crop all images in the input folder to the specified resolution, maintaining aspect ratio.
    Saves the processed images to the output folder.
    
    :param input_folder: Path to the input folder containing images.
    :param output_folder: Path to save the processed images.
    :param target_width: Target width for the output images.
    :param target_height: Target height for the output images.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each image in the input folder
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)

        # Skip non-image files
        if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            print(f"Skipping non-image file: {file_name}")
            continue

        try:
            with Image.open(input_path) as img:
                # Check aspect ratios
                input_aspect = img.width / img.height
                target_aspect = target_width / target_height

                # Resize image based on the target aspect ratio
                if input_aspect > target_aspect:
                    # Input image is wider; resize by height
                    new_height = target_height
                    new_width = int(new_height * input_aspect)
                else:
                    # Input image is taller or equal; resize by width
                    new_width = target_width
                    new_height = int(new_width / input_aspect)

                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Calculate crop box
                left = (new_width - target_width) // 2
                top = (new_height - target_height) // 2
                right = left + target_width
                bottom = top + target_height

                # Crop the image to the target resolution
                img_cropped = img_resized.crop((left, top, right, bottom))

                # Save the output image
                output_path = os.path.join(output_folder, file_name)
                img_cropped.save(output_path)
                print(f"Processed and saved: {output_path}")
        except Exception as e:
            print(f"Failed to process {file_name}: {e}")

# Example usage
if __name__ == "__main__":
    input_folder = "input"  # Replace with the path to your input folder
    output_folder = "output"  # Replace with the path to your output folder
    target_width = 2200  # Replace with your target width
    target_height = 2200  # Replace with your target height

    resize_and_crop_images(input_folder, output_folder, target_width, target_height)

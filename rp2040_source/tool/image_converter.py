import cv2
import numpy as np
def rotate_image_90(image):
    # Rotate the image 90 degrees clockwise
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # Display the original and rotated images (optional)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return rotated_image
def padding_cv2(img, expected_size):
    desired_size = expected_size
    delta_width = desired_size[0] - img.shape[1]
    delta_height = desired_size[1] - img.shape[0]
    pad_width = delta_width // 2
    pad_height = delta_height // 2

    padding = ((pad_width, delta_width - pad_width), (pad_height, delta_height - pad_height), (0, 0))

    padded_img = cv2.copyMakeBorder(img, pad_height, delta_height - pad_height, pad_width, delta_width - pad_width, cv2.BORDER_CONSTANT, value=0)

    return padded_img

def resize_with_padding_cv2(img, expected_size):
    # Resize the image while maintaining the aspect ratio
    aspect_ratio = img.shape[1] / img.shape[0]
    if aspect_ratio < 1:
        new_width = expected_size[0]
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = expected_size[1]
        new_width = int(new_height * aspect_ratio)

    resized_img = cv2.resize(img, (new_width, new_height))

    print("Resized Image Dimensions:", resized_img.shape)

    # Calculate padding
    delta_width = expected_size[0] - resized_img.shape[1]
    delta_height = expected_size[1] - resized_img.shape[0]
    pad_width = delta_width // 2
    pad_height = delta_height // 2

    print("Padding:", pad_width, pad_height)

    # Add padding
    padded_img = cv2.copyMakeBorder(resized_img, pad_height, delta_height - pad_height, pad_width, delta_width - pad_width, cv2.BORDER_CONSTANT, value=0)

    print("Padded Image Dimensions:", padded_img.shape)

    return padded_img
def resize_with_crop_and_perspective(original_image, new_size=(200, 200)):
    # Get the original image's height and width
    resized_image = resize_with_padding_cv2(original_image,new_size)
    return resized_image

def bits_to_bytes(bit_array):
    # Check if the length of the bit array is a multiple of 8
    bit_array = [bool(x) for x in bit_array]
    if len(bit_array) % 8 != 0:
        raise ValueError("The length of the bit array must be a multiple of 8.")

    # Initialize an empty byte array
    byte_array = bytearray()

    # Iterate through the bit array, converting 8 bits at a time to a byte
    for i in range(0, len(bit_array), 8):
        byte = 0
        # Convert 8 bits to a byte
        for j in range(8):
            byte = (byte << 1) | bit_array[i + j]
        
        # Append the byte to the byte array
        byte_array.append(byte)

    return byte_array
def resize_and_convert_to_binary_grayscale(input_image_path, new_size=(64, 64)):
    # Read the input image
    original_image = cv2.imread(input_image_path)
    original_image = resize_with_crop_and_perspective(original_image, new_size=(296,128))
    grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)  
    # Resize the image
    resized_image = cv2.resize(grayscale_image, new_size)

    # Convert to 2-level binary grayscale
    _, binary_image = cv2.threshold(resized_image, np.average(resized_image), 255, cv2.THRESH_BINARY)
    # Display the binary image using OpenCV's imshow
    
    
    binary_image = rotate_image_90(binary_image)
    binary_image = cv2.bitwise_not(binary_image)
    cv2.imshow('Binary Image', binary_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Flatten the 2D array to a 1D array
    flattened_image = binary_image.flatten()

    # Convert the 1D array to a byte string
    data = bits_to_bytes(flattened_image)
    return data


# # Example usage
# input_image_path = 'image.png'
# output_text_file = 'output_byte_text.txt'
# # Write the byte text to a file
# data = resize_and_convert_to_binary_grayscale(input_image_path,new_size=(296,128))
# byte_text = ''
# for i in range(len(data)-1):
#     if i % 16 == 0:
#         byte_text +='\n'
#     byte_text +=hex(data[i])
#     byte_text +=', '
# with open(output_text_file, 'w') as file:
#     file.write(byte_text)

# print(f"Image resized and converted to binary grayscale. Byte text saved to {output_text_file}")


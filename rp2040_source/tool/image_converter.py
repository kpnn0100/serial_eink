import cv2
import numpy as np
def resize_with_crop_and_perspective(original_image, new_size=(200, 200)):
    # Get the original image's height and width
    height, width = original_image.shape[:2]

    # Define the source and destination points for the perspective transformation
    src_points = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    dst_points = np.float32([[0, 0], [new_size[0], 0], [new_size[0], new_size[1]], [0, new_size[1]]])

    # Compute the perspective transformation matrix
    perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        # Apply the perspective transformation
    resized_image = cv2.warpPerspective(original_image, perspective_matrix, new_size)
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
def resize_and_convert_to_binary_grayscale(input_image_path, output_text_file, new_size=(64, 64)):
    # Read the input image
    original_image = cv2.imread(input_image_path)
    original_image = resize_with_crop_and_perspective(original_image, new_size=(128,296))
    print(original_image)
    grayscale_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)  
    # Resize the image
    resized_image = cv2.resize(grayscale_image, new_size)

    # Convert to 2-level binary grayscale
    _, binary_image = cv2.threshold(resized_image, np.average(resized_image), 255, cv2.THRESH_BINARY)
    # Display the binary image using OpenCV's imshow
    cv2.imshow('Binary Image', binary_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Flatten the 2D array to a 1D array
    flattened_image = binary_image.flatten()
    # Convert the 1D array to a byte string
    data = bits_to_bytes(flattened_image)
    print(data)
    byte_text = ''
    for i in range(len(data)-1):
        if i % 16 == 0:
            byte_text +='\n'
        byte_text +=hex(data[i])
        byte_text +=', '

    # Write the byte text to a file
    with open(output_text_file, 'w') as file:
        file.write(byte_text)

    print(f"Image resized and converted to binary grayscale. Byte text saved to {output_text_file}")

# Example usage
input_image_path = 'image.png'
output_text_file = 'output_byte_text.txt'
resize_and_convert_to_binary_grayscale(input_image_path, output_text_file,new_size=(296,128))

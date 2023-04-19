import cv2
import argparse
import numpy as np
import matplotlib.pyplot as plt
from apriltag import apriltag

def annotate_detections(img, detections, thickness=2):
    '''
    Add annotations of the AprilTag detection results on the input image.

    Args:
        img (numpy.ndarray): The image on which detection results will be annotated.
        detections (tuple): The tuple containing dictionaries of AprilTag detection results after running detector.detect().
        thickness (int): Thickness of annotation boxes and texts.

    Returns:
        None

    Example Usage:
        annotate_detections(img, detections)
    '''

    # Loop through each detection in the input detection list
    for detection in detections:

        # Define the pixel coordinates of the four corners of the quadrilateral
        corners = detection['lb-rb-rt-lt'].astype(np.int32)

        # Reshape the corners to a 2D array of shape (4, 1, 2)
        corners = corners.reshape((-1, 1, 2))

        # Draw a box around the quadrilateral on the input image
        cv2.polylines(img, [corners], True, (255, 0, 0), thickness)

        # Define the text to be displayed
        text = f"id: {detection['id']}"

        # Define the pixel coordinates of the text on the image
        loc = detection['center'].astype(np.int32)

        # Draw the text on the input image at the specified location
        cv2.putText(img, text, loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), thickness)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A script to detect Apriltag families in a given image',
        epilog='Example: "python image_demo.py --img ../img/non_nested_TLOF.png --tagtype tag36h11"'
    )
    parser.add_argument(
        '--img', type=str, 
        help='The path to the image for Apriltag detection being loaded'
    )
    parser.add_argument(
        '--tagtype', type=str, 
        help='The name of the type of Apriltag being detected. E.g., tag36h11 (the non-nested layout), tagCustom52h12 (the nested layout)'
    )
    parser.add_argument(
        '--stroke', type=int, required=False, default='2', dest="stroke", 
        help='The stoke thickness of annotations for Apriltag detection results'
    )

    args = parser.parse_args()

    # Load an image
    im = cv2.imread(args.img, cv2.IMREAD_COLOR)

    # Create an Apriltag detector
    detector = apriltag(args.tagtype)
    
    # Detect Apriltags (Beware: input image data should be in grayscale)
    detections = detector.detect(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY))
    
    # Print all the detections
    for detection in detections:
        print('-----')
        for k, v in detection.items():
            print(k, v)

    # Plot detection results
    annotate_detections(im, detections, thickness=args.stroke)

    # Display the image
    plt.imshow(im)
    plt.axis('off')
    plt.show()
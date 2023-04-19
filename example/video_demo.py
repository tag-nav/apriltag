import cv2
import argparse
import numpy as np
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
        cv2.polylines(img, [corners], True, (0, 0, 255), thickness)     # BGR

        # Define the text to be displayed
        text = f"id: {detection['id']}"

        # Define the pixel coordinates of the text on the image
        loc = detection['center'].astype(np.int32)

        # Draw the text on the input image at the specified location
        cv2.putText(img, text, loc, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness)    # BGR

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A script to detect Apriltag families from livestreamed video',
        epilog='Example: "python video_demo.py --video 0 --tagtype tag36h11"'
    )
    parser.add_argument(
        '--video', type=int, 
        help='The ID of video being captured. Check out ls /dev/video* to see whether there exist any available video device you have.'
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

    # Create a VideoCapture object to capture video from the default camera (index 0)
    cap = cv2.VideoCapture(args.video)

    # Check if camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera")
        exit()

    # Create an Apriltag detector
    detector = apriltag(args.tagtype)

    # Loop to capture and display video frames
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if frame was captured successfully
        if not ret:
            print("Error: Could not capture frame")
            break

        # Detect Apriltags (Beware: input image data should be in grayscale)
        detections = detector.detect(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
        
        # Plot detection results
        annotate_detections(frame, detections)

        # Display the frame
        cv2.imshow("Camera", frame)

        # Exit loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
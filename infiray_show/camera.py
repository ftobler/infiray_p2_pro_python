import cv2
import numpy as np


def infiray_camera_source():
    """
    A generator function that yields temperature data in degrees C from the InfiRay P2 Pro camera.
    """

    try:
        # Initialize the webcam
        camera = cv2.VideoCapture(0)  # 0 is the default webcam index

        # Check if the camera opened successfully
        if not camera.isOpened():
            print("Error opening camera!")
            exit()

        # disable automatic YUY2->RGB conversion of OpenCV
        camera.set(cv2.CAP_PROP_CONVERT_RGB, 0)

        print("Press 'q' or 'ESC' to quit, 'ENTER' to save a screenshot")

        while True:
            # Capture frame-by-frame
            _ret, frame = camera.read()
            # np.save("frame_raw.npy", frame)

            # the np array has no correct shape without CAP_PROP_CONVERT_RGB
            frame = frame[0]

            # split video frame (top is pseudo color, bottom is temperature data)
            frame_mid_pos = int(len(frame) / 2)
            # picture_data = frame[0:frame_mid_pos]
            thermal_data = frame[frame_mid_pos:]

            # that is the camera pixel resolution anyway. force reshape into this shape.
            image_size = (192, 256)
            thermal_picture_16 = np.frombuffer(thermal_data, dtype=np.uint16).reshape(image_size)

            # convert degree Celsius temperature image
            temperatures = thermal_picture_16 / 64.0 - 273.15

            yield temperatures

    finally:

        # Release resources
        camera.release()

import cv2
import numpy as np
import datetime

# Initialize the webcam
camera = cv2.VideoCapture(0)  # 0 is the default webcam index

# Check if the camera opened successfully
if not camera.isOpened():
    print("Error opening camera!")
    exit()

# disable automatic YUY2->RGB conversion of OpenCV
camera.set(cv2.CAP_PROP_CONVERT_RGB, 0)


def to_temperature(int16_value):
    return int16_value / 64 - 273.15


print("Press 'q' or 'ESC' to quit, 'ENTER' to save a screenshot")


while True:
    # Capture frame-by-frame
    ret, frame = camera.read()
    # np.save("frame_raw.npy", frame)

    # the np array has no correct shape without CAP_PROP_CONVERT_RGB
    frame = frame[0]

    # split video frame (top is pseudo color, bottom is temperature data)
    frame_mid_pos = int(len(frame) / 2)
    picture_data = frame[0:frame_mid_pos]
    thermal_data = frame[frame_mid_pos:]

    # that is the camera pixel resolution anyway. force reshape into this shape.
    image_size = (192, 256)
    thermal_picture_16 = np.frombuffer(thermal_data, dtype=np.uint16).reshape(image_size)

    # normalize the temperature data to 0..1 for display on screen
    min = np.min(thermal_picture_16)
    max = np.max(thermal_picture_16)
    normalized_image = (thermal_picture_16 - min) / (max - min)  # 0..1 float

    # make image bigger for better visibility on screen
    display_scale_factor = 4
    height = int(normalized_image.shape[0] * display_scale_factor)
    width = int(normalized_image.shape[1] * display_scale_factor)
    show_image = cv2.resize(normalized_image, (width, height), interpolation=cv2.INTER_CUBIC)
    show_image = (show_image * 255).astype(np.uint8)  # Convert to uint8
    show_image = cv2.applyColorMap(show_image, cv2.COLORMAP_MAGMA)  # apply colormap

    # draw temperature measurement point at the image center
    x = image_size[1] // 2
    y = image_size[0] // 2
    center_temp = to_temperature(thermal_picture_16[y, x])
    black = (0,0,0)
    white = (255,255,255)
    cv2.drawMarker(show_image, (x*4, y*4), black, cv2.MARKER_CROSS, 20, 3)
    cv2.drawMarker(show_image, (x*4, y*4), white, cv2.MARKER_CROSS, 20, 1)
    cv2.putText(show_image, "%.1f C" % center_temp, (x*4+20, y*4), cv2.FONT_HERSHEY_SIMPLEX, 1, black, 3)
    cv2.putText(show_image, "%.1f C" % center_temp, (x*4+20, y*4), cv2.FONT_HERSHEY_SIMPLEX, 1, white, 1)

    # Display the resulting frame
    cv2.imshow('InfiRay', show_image)

    # Break the loop if 'q' is pressed
    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:  # 27 is the ESC key
        break
    if key == 13:  # 13 is the ENTER key
        date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        cv2.imwrite("%s.png" % date, show_image)

# Release resources
camera.release()
cv2.destroyAllWindows()


import cv2
import numpy as np
import datetime
from infiray_show.camera import infiray_camera_source
from infiray_show.marker import draw_temperature_marker, LPF2D

def main():

    filter_max_pos = LPF2D(0.3)
    filter_min_pos = LPF2D(0.3)

    for temperatures in infiray_camera_source():
        y, x = temperatures.shape

        # normalize the temperature data to 0..1 for display on screen (auto-gain)
        normalized_image = cv2.normalize(temperatures, None, 0, 1, cv2.NORM_MINMAX)

        # make image bigger for better visibility on screen
        scale = 4
        height = y * scale
        width  = x * scale
        show_image = cv2.resize(normalized_image, (width, height), interpolation=cv2.INTER_CUBIC)
        show_image = (show_image * 255).astype(np.uint8)
        show_image = cv2.applyColorMap(show_image, cv2.COLORMAP_MAGMA)  # apply colormap

        # draw temperature measurement point at the image center
        draw_temperature_marker(show_image, x // 2, y // 2, temperatures, scale)

        # find the brightest and dimmest pixel in temperatures and mark them too
        _min_val, _max_val, min_loc, max_loc = cv2.minMaxLoc(temperatures)
        min_loc = filter_min_pos.update(min_loc)
        max_loc = filter_max_pos.update(max_loc)
        draw_temperature_marker(show_image, max_loc[0], max_loc[1], temperatures, scale)
        draw_temperature_marker(show_image, min_loc[0], min_loc[1], temperatures, scale)

        # Display the resulting frame using OpenCV builtin view window
        cv2.imshow('InfiRay', show_image)

        # Break the loop if 'q' is pressed
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:  # 27 is the ESC key
            break
        if key == 13:  # 13 is the ENTER key
            date = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite("%s.png" % date, show_image)


def infiray_show():
    main()


if __name__ == "__main__":
    main()
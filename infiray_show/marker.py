
import cv2


def draw_temperature_marker(show_image, x, y, temperature, scale):
    sx = x * scale
    sy = y * scale
    center_temp = temperature[y, x]
    black = (0,0,0)
    white = (255,255,255)
    cv2.drawMarker(show_image, (sx, sy), black, cv2.MARKER_CROSS, 20, 3)
    cv2.drawMarker(show_image, (sx, sy), white, cv2.MARKER_CROSS, 20, 1)
    shift = 20
    if sx > show_image.shape[1] - 130:
        shift = -130
    cv2.putText(show_image, "%.1f C" % center_temp, (sx+shift, sy), cv2.FONT_HERSHEY_SIMPLEX, 1, black, 3)
    cv2.putText(show_image, "%.1f C" % center_temp, (sx+shift, sy), cv2.FONT_HERSHEY_SIMPLEX, 1, white, 1)

import cv2


class LPF:
    def __init__(self, alpha):
        self.alpha = alpha
        self.value = 0

    def update(self, new_value):
        self.value = self.alpha * new_value + (1 - self.alpha) * self.value
        return self.value


class LPF2D:
    def __init__(self, alpha):
        self.filter_x = LPF(alpha)
        self.filter_y = LPF(alpha)

    def update(self, loc):
        x, y = loc
        return self.filter_x.update(x), self.filter_y.update(y)


def draw_temperature_marker(show_image, x, y, temperature, scale):
    x = int(x)
    y = int(y)
    sx = x * scale
    sy = y * scale
    center_temp = temperature[y, x]
    black = (0, 0, 0)
    white = (255, 255, 255)
    cv2.drawMarker(show_image, (sx, sy), black, cv2.MARKER_CROSS, 20, 3)
    cv2.drawMarker(show_image, (sx, sy), white, cv2.MARKER_CROSS, 20, 1)
    shift = 20
    if sx > show_image.shape[1] - 130:
        shift = -130
    cv2.putText(show_image, "%.1f C" % center_temp, (sx + shift, sy), cv2.FONT_HERSHEY_SIMPLEX, 1, black, 3)
    cv2.putText(show_image, "%.1f C" % center_temp, (sx + shift, sy), cv2.FONT_HERSHEY_SIMPLEX, 1, white, 1)

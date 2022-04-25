import cv2
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class MPLVideoMaker:
    def __init__(self):
        self.init = False
        self.h, self.w = 0, 0
        self.fps = float(0)
        self.size = (self.w, self.h)
        self.fourcc = None
        self.video = None

    def add_frame(self, fig, duration=None):
        """
        Add a frame from a fig matplotlib object
        :param fig: matplotplib fig object
        :param duration: duration of the frame in s
        :return:
        """

        canvas = FigureCanvas(fig)
        canvas.draw()
        image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        if duration is None:
            self.video.write(image)
        else:
            for i in range(self.fps * duration):
                self.video.write(image)

    def init_video(self, name, fig, fps=24):
        """
        Initialize the video
        :param fig: a matplotlib figure obj
        :param fps: frame per second
        :param name: name of the .mp4 file
        :return: None
        """
        canvas = FigureCanvas(fig)
        canvas.draw()
        img = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        (self.h, self.w) = img.shape[:2]
        self.size = (self.w, self.h)
        self.fps = fps
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.video = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.w, self.h), isColor=True)
        self.init = True

    def write_video(self):
        """
        Write the video
        :return:
        """
        self.video.release()

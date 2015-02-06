import cv2
import numpy as np

class RichImage(np.ndarray):

  # ndarrays are funky creatures...
  def __new__(cls, input_array, attrs=None):
    obj = np.asarray(input_array).view(cls)
    obj.windows = set()
    obj.height, obj.width = obj.shape[:2]
    obj.fan = obj[60:-80, 100:-50]
    return obj[::]

  def __array_finalize__(self, obj):
    self.windows = getattr(obj, 'windows', None)
    self.height = getattr(obj, 'height', None)
    self.width = getattr(obj, 'width', None)
    self.fan = getattr(obj, 'fan', None)

  def __str__(self):
    return "{0} of dimensions {1} x {2}".format(self.__class__.__name__, self.w, self.h)

  def rotate(self, angle, image=None):
    if image is None:
        image = self[::]

    (rows, cols, _) = image.shape
    rotation_matrix = cv2.getRotationMatrix2D((cols/2,rows/2), angle, 1)
    return cv2.warpAffine(image, rotation_matrix, (cols,rows))

  def fan_only(self):
      return RichImage(self.fan)

  def rotate_fan(self, angle):
      fan = RichImage(self.fan)
      rotated_fan = self.rotate(angle, fan)
      new_img = self.copy()
      new_img[60:-80, 100:-50] = rotated_fan
      return RichImage(new_img)

  def show(self, window_name="default"):
    self.windows.add(window_name)
    try:
        self.destroy_window(window_name)
    except:
        print "No window named {0}".format(window_name)
    cv2.imshow(window_name, self)

  def destroy_window(self, window_name="default"):
    try:
      self.windows.remove(window_name)
      cv2.destroyWindow(window_name)
    except:
      print "No window named {0}".format(window_name)

  def side_by_side(self, other):
      vis = np.concatenate((self.copy(), other.copy()), axis=1)
      return RichImage(vis)


if __name__ == "__main__":
    import sys
    from platform import system
    import os


    # make sure we're not dealing with windows...
    if system() != 'Windows':
        try:
            print "using readline tools..."
            import readline
            readline.set_pre_input_hook(readline.redisplay())
        except:
            pass


    class Displayer(object):

        def __init__(self, img):
            self.exit_cmds = ["q", "exit"]
            self.help_cmds = ["?", "help"]
            self.save_cmds = ["s", "save"]

            self.help_msg = """\nEnter an angle (positive or negative)

            COMMANDS:
            \t{0} => quit
            \t{1} => help
            \t{2} => save\n""".format(" OR ".join(self.exit_cmds),
                                      " OR ".join(self.help_cmds),
                                      " OR ".join(self.save_cmds))

            self.current_img = img
            self.current_deg = None


        def display_image(self, somedeg):
            deg = 0
            try:
                deg = int(somedeg)
            except:
                pass

            cv2.destroyAllWindows()
            self.current_img = rich_img.side_by_side(rich_img.rotate_fan(deg))
            self.current_deg = deg
            self.current_img.show("rotated {} degrees".format(self.current_deg))

        def save(self):
            img_name = "{0}-deg.jpg".format(self.current_deg)
            cv2.imwrite(img_name, self.current_img)
            print("\n{0} saved to {1}\n".format(img_name, os.getcwd()))


    rich_img = RichImage(cv2.imread("test.jpg"))
    displayer = Displayer(rich_img)

    print(displayer.help_msg)
    displayer.display_image(sys.argv[-1])

    while True:
        key = raw_input("  ?> ")

        if key in displayer.exit_cmds or not key:
            sys.exit(1)
        elif key in displayer.help_cmds:
            print help_msg
        elif key in displayer.save_cmds:
            try:
                displayer.save()
            except:
                pass
        else:
            displayer.display_image(key)


# rich_img = RichImage(cv2.imread('test.jpg'))
# imgray = cv2.cvtColor(rich_img, cv2.COLOR_BGR2GRAY)
# ret,thresh = cv2.threshold(imgray,127,255,0)
# contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#
# cv2.drawContours(rich_img, contours, -1, (0,255,0), 3)
#
#
# gray = cv2.cvtColor(rich_img,cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray,50,150,apertureSize = 3)
#
# lines = cv2.HoughLines(edges,1,np.pi/180,200)
# for rho,theta in lines[0]:
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a*rho
#     y0 = b*rho
#     x1 = int(x0 + 1000*(-b))
#     y1 = int(y0 + 1000*(a))
#     x2 = int(x0 - 1000*(-b))
#     y2 = int(y0 - 1000*(a))
#
#     cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
#
# rich_img.show()

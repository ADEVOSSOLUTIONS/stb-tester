"""
Compatibility so stb-tester will work with both OpenCV 2 and 3.
"""

from distutils.version import LooseVersion

import cv2

_version = LooseVersion(cv2.__version__)

if _version >= LooseVersion('3.2.0'):
    def find_contour_boxes(image, mode, method):
        contours = cv2.findContours(image=image, mode=mode, method=method)[1]
        return [cv2.boundingRect(x) for x in contours]
else:
    def _fix_pre_3_2_rects(r):
        # In OpenCV 3.2 the behaviour of findContours changed.  It seems more
        # sensible now but we need to still support the old behaviour.
        # See 56c133d459248d17165d77eb902a8049680bf896 in OpenCV:
        # https://github.com/opencv/opencv/commit/56c133d459248d17165d77eb902a8049680bf896
        x, y, w, h = r
        return (x - 1, y - 1, w + 2, h + 2)

    def find_contour_boxes(image, mode, method):
        # In v3.0.0 cv2.findContours started returing (img, contours, hierarchy)
        # rather than (contours, heirarchy).  Index -2 selects contours on both
        # versions:
        contours = cv2.findContours(image=image, mode=mode, method=method)[-2]
        return [_fix_pre_3_2_rects(cv2.boundingRect(x)) for x in contours]

# We prefer the v3 names here rather than the v2.4 names:
if _version >= LooseVersion('3.0.0'):
    FILLED = cv2.FILLED  # pylint: disable=c-extension-no-member
    LINE_AA = cv2.LINE_AA  # pylint: disable=c-extension-no-member
else:
    FILLED = cv2.cv.CV_FILLED  # pylint: disable=c-extension-no-member,no-member
    LINE_AA = cv2.CV_AA  # pylint: disable=c-extension-no-member

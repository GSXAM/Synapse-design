import cv2

img = cv2.imread(r".\Photos-001\IMG_20230909_074016_755.jpg", cv2.IMREAD_GRAYSCALE)

h, w = img.shape[:2]

width = 900
height = int(width * h / w)

thresh, img = cv2.threshold(img, 0, 255, cv2.THRESH_TRIANGLE)
print(thresh)
img = cv2.resize(img, (width, height))

cv2.imshow("CCCD", img)
cv2.waitKey()
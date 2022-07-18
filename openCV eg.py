import cv2

img = cv2.imread('/Users/leehoseop/Desktop/이미지파일.png')
x_pos, y_pos, width, height = cv2.selectROI("location", img, False)
print("x_position, y_position:  ", x_pos, y_pos)
print("width, height:  ", width, height)

cv2.destroyAllWindows()



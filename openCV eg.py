import cv2
import sys

src = cv2.imread("/Users/leehoseop/Desktop/SVS_background.png") # src.shape=(320, 480)

if src is None:
    print('Image load failed!')
    sys.exit()

dst1 = cv2.resize(src, (1200, 675), fx=4, fy=4, interpolation=cv2.INTER_NEAREST) # 스케일 팩터 이용
# dst2 = cv2.resize(src, (1920, 1280))  # cv2.INTER_LINEAR, 픽셀 크기 지정
# dst3 = cv2.resize(src, (1920, 1280), interpolation=cv2.INTER_CUBIC) # 픽셀 크기 지정
# dst4 = cv2.resize(src, (1920, 1280), interpolation=cv2.INTER_LANCZOS4) # 픽셀 크기 지정

cv2.imshow('dst1', dst1)
cv2.imwrite('/Users/leehoseop/Desktop/SVS_background2.png', dst1)
# cv2.imshow('dst1', dst1[500:900, 400:800]) # 영상 크기가 너무 커서 일정 부분만 출력
# cv2.imshow('dst2', dst2[500:900, 400:800])
# cv2.imshow('dst3', dst3[500:900, 400:800])
# cv2.imshow('dst4', dst4[500:900, 400:800])
cv2.waitKey()
cv2.destroyAllWindows()

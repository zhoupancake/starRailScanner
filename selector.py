import numpy as np
import cv2 as cv
import random

# 设置putText函数字体
font = cv.FONT_HERSHEY_SIMPLEX


# 计算两边夹角的cos值
def angle_cos(p0, p1, p2):
    d1, d2 = (p0 - p1).astype('float'), (p2 - p1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1) * np.dot(d2, d2)))


def find_squares(img):
    squares = []
    img = cv.GaussianBlur(img, (3, 3), 0)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    bin = cv.Canny(gray, 30, 100, apertureSize=3)
    contours, _hierarchy = cv.findContours(bin, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # print("轮廓数量：%d" % len(contours))
    index = 0

    result = []
    # 轮廓遍历
    for cnt in contours:
        cnt_len = cv.arcLength(cnt, True)  # 计算轮廓周长
        cnt = cv.approxPolyDP(cnt, 0.02 * cnt_len, True)  # 多边形逼近
        # 条件判断逼近边的数量是否为4,轮廓面积是否大于1000,检测轮廓是否为凸的
        if len(cnt) == 4 and cv.contourArea(cnt) > 10000 and cv.isContourConvex(cnt):
            M = cv.moments(cnt)  # 计算轮廓的矩
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])  # 轮廓重心

            cnt = cnt.reshape(-1, 2)
            # max_cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in range(4)])
            # 只检测矩形(cos90° = 0)
            # if max_cos < 0.1:
            # 检测四边形(不限定角度范围)
            # if (cnt[1][0] - cnt[0][0]) > 2 * (cnt[2][1] - cnt[1][1]):
            index = index + 1
            # cv.putText(img,("#%d"%index),(cx,cy),font,0.7,(255,0,255),2)
            squares.append(cnt)
            x, y, w, h = cv.boundingRect(cnt)
            result.append(img[y:y + h, x:x + w])
                # random_integer = random.randint(0, 10000000)
                # save = cv.imwrite(f"./sc/rectangle_{random_integer}.jpg", img[y:y+h, x:x+w])
                # cv.drawContours(img, squares, -1, (0, 0, 255), 2)
                # save = cv.imwrite(f"./sc/rectangle_{random_integer}.jpg", img)
                # print("Save ", save, index)
                # if index < 5:
                #     random_integer = random.randint(0, 10000000)
                #     save = cv.imwrite(f"./sc/rectangle_{random_integer}.jpg", img)
    return squares, result


def select(path):
    img = cv.imread(path)
    # print("read the path", path)
    # cv.waitKey(0)
    squares, img = find_squares(img)
    # cv.drawContours( img, squares, -1, (0, 0, 255), 2 )
    return img


if __name__ == '__main__':
    img = select("./imgs/Trailblazer/29.jpg")

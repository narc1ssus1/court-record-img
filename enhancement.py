import cv2
import numpy as np
import requests

threadshold = 160
ocr_address = "http://127.0.0.1:5000"


def enhancement(img_path):
    # 读取输入图像
    input_image = cv2.imread(img_path)

    # 转换图像为灰度
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # 使用阈值分割将白色纸张变成黑色
    _, thresholded_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY)

    # 找到轮廓
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # 找到最大的轮廓（即白纸）
        largest_contour = max(contours, key=cv2.contourArea)

        # 获取最大轮廓的近似多边形
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)

        # 提取白纸的四个顶点坐标
        points = np.squeeze(approx)

        # 打印顶点坐标
        print("Paper Corner Coordinates:")
        for point in points:
            print(tuple(point))
    else:
        print("No paper found in the image.")

    # 定义输出图像的宽度和高度
    width = 2000
    height = 2828

    # 获取四个顶点坐标
    pts = np.float32(tuple(points))
    dst_pts = np.float32([[0, 0], [width, 0], [width, height], [0, height]])

    ##透视变换进行梯形校正
    M = cv2.getPerspectiveTransform(pts, dst_pts)
    dst = cv2.warpPerspective(input_image, M, (width, height))
    binary = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    # 二值化叠加增强图像
    binary[binary > threadshold] = 255
    binary[binary <= threadshold] = 0
    binary = cv2.merge([binary, binary, binary])
    dst = np.maximum(dst, binary)
    cv2.imwrite(img_path, dst, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
    files = {'jpg':('file.jpg', open(img_path, 'rb'), 'application/octet-stream')}
    try:
        response = requests.post(ocr_address+"/slope-detect",data={}, files=files)
        f = open(img_path, 'wb')
        f.write(response.content)
    except:
        pass
    return img_path

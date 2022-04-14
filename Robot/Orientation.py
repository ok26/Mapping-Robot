import cv2
import numpy as np
from Robot import cap

def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)


def automatic_brightness_and_contrast(image, clip_hist_percent=1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)
    
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))
    
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0
    
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1
    
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1
    
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result, alpha, beta)

def find_markers(type):
    cx, cy = [], []
    _, frame = cap.read()
    frame = adjust_gamma(frame, 1.1)
    #frame, _, _ = automatic_brightness_and_contrast(frame)
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    mask = cv2.inRange(hsv_frame, type[0], type[1])
    _, thresh = cv2.threshold(mask,127,255,0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        M = cv2.moments(c)
        if M["m00"] > 300:   
            cx.append(int(M["m10"] / M["m00"]))    
            cy.append(int(M["m01"] / M["m00"]))
            for i in range(len(cx)):
                cv2.circle(mask, (cx[i], cy[i]), 10, (160, 80, 123), -1)

    cv2.imshow(str(type[0][0]), mask)
    if str(type[0][0]) == "100":
        cv2.imshow("lol", frame)
    key = cv2.waitKey(1)
    return cx, cy


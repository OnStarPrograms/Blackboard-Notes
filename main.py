import cv2 as cv
import platform
import numpy as np
from PIL import Image
import os
import time

frameWidth = 640
frameHeight = 480
cap = cv.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)
count = 0


def notify(title, text):
    if (platform.system() != "Darwin"):
        print("no support for notifications on this system rn")
        return
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))



while True:
    success, img = cap.read()
    if success is not True:
        pass

    # turn image grayscale
    gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # image algorithms to get enrgy of lines then clean up image
    th1  = cv.adaptiveThreshold(gray_img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,11,2)
    blur = cv.GaussianBlur(th1,(5,5),0)
    ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    cv.imshow("Result", th3)

    # Save the snapshot of the image
    if cv.waitKey(1) & 0xFF == ord('s'):
        cv.imwrite('./out/image'+str(count)+'.png',th3)
        count+=1
        notify("Snapshot", "Snapshot taken")
        time.sleep(1)

    # pull all screen shots then turn into pdf
    if cv.waitKey(1) & 0xFF == ord('q'):
        notify("Cleaning Up", "Translating images to pdf")
        images = []

        for f in range(count):
            images.append(Image.open("./out/image" + str(f) + ".png"))

        pdf_path = "./out/lecture_notes.pdf"
        images[0].save(
            pdf_path, "PDF" ,resolution=70.0, save_all=True, append_images=images[1:]
        )
        for f in range(count):
            os.remove('./out/image'+str(f)+'.png')
        break


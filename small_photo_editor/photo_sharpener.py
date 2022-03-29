import numpy as np
import cv2


class SharpenerBlur:
    def __init__(self):
        return

    @staticmethod
    async def sharpen_ig(kernel_size, magnitude):
        # rn need to find a way to save the img to before_edit_img

        # kernel size changes the sharping with less magnitude - for finner tunning rather than alpha scales
        # Sharpened = Original + \alpha * "Details" = Original + \alpha * (Original - Smoothed)

        kernel_sz = kernel_size
        alpha = magnitude

        img_display = cv2.imread("small_photo_editor/before_edit_img.png")
        kernel_box = np.ones((kernel_sz, kernel_sz), dtype=np.float32)
        kernel_box = kernel_box / kernel_box.sum()
        kernel_identity = np.zeros((kernel_sz, kernel_sz), dtype=np.float32)
        kernel_identity[kernel_sz // 2, kernel_sz // 2] = 1.0
        kernel_sharpening = kernel_identity + alpha * (kernel_identity - kernel_box)
        img_sharpened = cv2.filter2D(src=img_display, ddepth=-1, kernel=kernel_sharpening)

        cv2.imwrite("small_photo_editor/after_edit_img.png", img_sharpened)

        # cv2.imshow('sample.jpeg',img)

    @staticmethod
    async def blur_ig(kernel_size):
        kernel_sz = kernel_size

        img_display = cv2.imread("small_photo_editor/before_edit_img.png")
        kernel_box = np.ones((kernel_sz, kernel_sz), dtype=np.float32)
        kernel_box = kernel_box / kernel_box.sum()
        kernel_blurring = kernel_box
        img_sharpened = cv2.filter2D(src=img_display, ddepth=-1, kernel=kernel_blurring)

        cv2.imwrite("small_photo_editor/after_edit_img.png", img_sharpened)






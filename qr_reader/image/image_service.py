import cv2
from pyzbar import pyzbar
import numpy as np

# from ..db import ScanDocument

class IMAGE_PR:
    def __init__(self, filename=None, byte_string=None):
        if filename:
            self.img = cv2.imread(filename)
        elif byte_string:
            nparr = np.frombuffer(byte_string, np.uint8)
            self.img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        else:
            self.img = None

        (self.h, self.w, self.d) = self.img.shape


    @staticmethod
    def decode_barcodes(_img):
        barcodes = pyzbar.decode(_img)

        if barcodes:
            barcode = barcodes[0]
            barcodeData = barcode.data.decode("utf-8")
            return barcodeData
        else:
            return None


    def return_image_corner(self):
        return self.img[0:int(self.h * 0.2), int(self.w * 0.75):self.w]

    def auto_find_qr_code(self):
        if self.w > self.h:
            self.img = cv2.rotate(self.img, cv2.ROTATE_90_COUNTERCLOCKWISE ) #ROTATE_90_CLOCKWISE)
            (self.h, self.w, self.d) = self.img.shape

        data_barcode = self.decode_barcodes(self.return_image_corner())

        if data_barcode:
            return data_barcode

        self.img = cv2.rotate(self.img, cv2.ROTATE_180)
        data_barcode = self.decode_barcodes(self.return_image_corner())

        return data_barcode

    def resize_scan(self):
        if self.h > 1280:
            coef = 1280 / self.h
            self.img = cv2.resize(self.img, (0,0), fx=coef, fy=coef)
            (self.h, self.w, self.d) = self.img.shape


    @staticmethod
    def show_img(_img):
        cv2.imshow("Image", _img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':

    fd = open('../../test/IMG/ddd.jpg', "rb")
    img_str = fd.read()
    fd.close()

    qr_r = IMAGE_PR(byte_string=img_str)

    # qr_r = IMAGE_PR('../../test/IMG/ddd.jpg')
    qr_code = qr_r.auto_find_qr_code()


    print(qr_code)

    print(qr_r.h, qr_r.w)

    # qr_r.show_img(qr_r.return_image_corner(qr_r.img, qr_r.TOP_LEFT) )
    qr_r.resize_scan()
    print(qr_r.h, qr_r.w)
    qr_r.show_img(qr_r.img)


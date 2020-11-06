import cv2
import numpy as np
from pyzbar import pyzbar

class ReadyQR:
    TOP_LEFT = 'TOP_LEFT'
    TOP_RIGHT ='TOP_RIGHT'
    LOWER_LEFT = 'LOWER_LEFT'
    LOWER_RIGHT = 'LOWER_RIGHT'
    TYPES_CORNER = (None, TOP_LEFT, TOP_RIGHT, LOWER_LEFT, LOWER_RIGHT)

    def __init__(self, filename=None, byte_string=None):
        if filename:
            self.img = cv2.imread(filename)
        elif byte_string:
            self.img = cv2.imread(filename)

        (self.h, self.w, self.d) = self.img.shape

        print(type(self.img))

    def decode_cv2(self):
        detector = cv2.QRCodeDetector()

        new_img = self.img

        retval, straight_qrcod = detector.detect(new_img)
        print(retval, straight_qrcod)

    def decode_barcodes(self, _img):
        barcodes = pyzbar.decode(_img)

        if barcodes:
            barcode = barcodes[0]
            barcodeData = barcode.data.decode("utf-8")
            return barcodeData
        else:
            return None


    def return_image_corner(self, _img, type_corner):
        if type_corner == self.TOP_LEFT:
            return _img[0:int(self.h * 0.25), 0:int(self.w*0.2)]

        elif type_corner == self.TOP_RIGHT:
            return _img[0:int(self.h * 0.2), int(self.w * 0.75):self.w]

        elif type_corner == self.LOWER_LEFT:
            (h, w, d) = _img.shape
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, 180, 1.0)
            new_img = cv2.warpAffine(_img, M, (w, h))
            return self.return_image_corner(new_img, self.TOP_RIGHT)

        elif type_corner == self.LOWER_RIGHT:
            (h, w, d) = _img.shape
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, 180, 1.0)
            new_img = cv2.warpAffine(_img, M, (w, h))
            return self.return_image_corner(new_img, self.TOP_LEFT)

        else:
            return self.img

    def auto_find_qr_code(self):
        for type_corner in  self.TYPES_CORNER:
            # print(type_corner)
            new_img = self.return_image_corner(self.img, type_corner)

            data_barcode = self.decode_barcodes(new_img)
            # self.show_img(new_img)
            if data_barcode:
                print(data_barcode)
                break
        return data_barcode

    def show_img(self, _img):
        cv2.imshow("Image", _img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    qr_r = ReadyQR('../../test/IMG/ddd.jpg')
    # qr_r = ReadyQR('../../test/IMG/test2.jpg')
    qr_code = qr_r.auto_find_qr_code()
    # qr_code =  qr_r.decode_barcodes(qr_r.img)
    print(qr_code)

    # qr_r.show_img(qr_r.return_image_corner(qr_r.img, qr_r.TOP_LEFT) )


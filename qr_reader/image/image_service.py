import cv2
import numpy as np
import io
from pyzbar import pyzbar
from pdf2image import convert_from_bytes


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

    def resize_image(self, max_size=1280):
        if self.h > max_size:
            coef = max_size / self.h
            self.img = cv2.resize(self.img, (0,0), fx=coef, fy=coef)
            (self.h, self.w, self.d) = self.img.shape

    @property
    def image_to_byte(self):
        img_param = [int(cv2.IMWRITE_JPEG_QUALITY), 70]
        _, img_encode = cv2.imencode('.jpeg', self.img, img_param)

        pp = img_encode.tobytes()
        return  pp

    @staticmethod
    def show_img(_img):
        cv2.imshow("Image", _img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def rotate_image(self, code_rotate=90):
        cv2_code_rotate =  cv2.ROTATE_90_COUNTERCLOCKWISE if int(code_rotate) == 90 else cv2.ROTATE_180
        self.img = cv2.rotate(self.img, cv2_code_rotate)

class PDF_TO_JPEG:
    def __init__(self, file):
        self._file = file

    def convert_pdf_to_jpeg(self):
        images = convert_from_bytes(self._file, fmt="jpeg")


        if images:
            buf = io.BytesIO()
            images[0].save(buf, format='JPEG')
            byte_im = buf.getvalue()

            return byte_im

        return None


if __name__ == '__main__':
    pass

import cv2
from pyzbar import pyzbar

img_name="./IMG/IMG_20201021_150749.jpg"
# img_name="./IMG/IMG_20201021_150736.jpg"

# img_name="./IMG/test3.jpg"

img = cv2.imread(img_name)
detector = cv2.QRCodeDetector()

print(img.shape)
(h, w, d) = img.shape
if h > w:
    img = img[0:h // 5, (7 * w // 10) : w]
    (h, w, d) = img.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 90, 1.0)
    img = cv2.warpAffine(img, M, (w, h))
else:
    img = img[0:(3 * h // 10), 0:w // 5]

print(img.shape)

retval, straight_qrcod = detector.detect(img)
print(retval, straight_qrcod)


# gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, threshold_image = cv2.threshold(img, 127, 255, 0)
#
#
# data, bbox, _ = detector.detectAndDecode(img)
# print(data)
#
# data, bbox, _ = detector.detectAndDecode(gray_image)
# print(data)
#
# data, bbox, _ = detector.detectAndDecode(threshold_image)
# print(data)
#
barcodes = pyzbar.decode(img)
for barcode in barcodes:
    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type
    text = "{} ({})".format(barcodeData, barcodeType)
    # cv2.putText(img, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    print("[INFO] found {} barcode {}".format(barcodeType, barcodeData))

#
# # print(barcodes)
#
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

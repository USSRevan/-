import cv2
from qr_scanner import scan_qrcode


camera_id = 0
camera = None

cam_width = 1280
cam_height = 720

crop_y = 0
crop_h = 600
crop_x = 128
crop_w = 650 

def camera_open(cam_index=camera_id):
    global camera
    camera = cv2.VideoCapture(cam_index)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, cam_width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, cam_height)
    return cam
    
def capture_and_crop():
    rec, image = camera.read()
    cropped = image[crop_y:crop_h, crop_x:crop_w]
    return cropped

def camera_close():
    del(camera)
	
def image_save(image, image_name):
	cv2.imwrite(image_name, image)
	


def scan_qrcode(image):
    qrDecoder = cv2.QRCodeDetector()
    data,__,__ = qrDecoder.detectAndDecode(inputImage)
    data = data.strip()
    return data

    
    
def scan_and_save(image_name="temp.png"):
    image = capture_and_crop()
    data = scan_qrcode(image)
    image_save(image, image_name)
    return data





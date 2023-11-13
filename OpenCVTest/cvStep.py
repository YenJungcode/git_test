import time
import cv2
import os
import numpy as np

from skimage.metrics import structural_similarity as ssim
from skimage.metrics import mean_squared_error as mse
from skimage import io, color
from scipy.signal import correlate2d

def setCamera(device=0):
    global deviceCamera
    # 0 represents the default camera, change if you have multiple cameras
    deviceCamera = device
    print("Camera set successful !")


# Capture a frame
def captureImage():
    global deviceCamera
    try:
        capture = cv2.VideoCapture(deviceCamera)
    except:
        assert False, "Unable to set the camera !"

    if not capture.isOpened():
        assert False, "Cannot open camera !!!"

    ret, frame = capture.read()
    if not ret:
        assert False, "Failed to capture an image !!!"

    # Release the camera
    capture.release()

    return ret, frame


# action : manual = Please print any key to close the image.
# action : empty = Image will close after 10s.
def showImage(action=None):
    ret, frame = captureImage()

    # Show the captured image
    cv2.imshow('Captured Image', frame)
    print("The code will stop until the image is closed !")

    if "manual" in action:
        print("Please print any key to close the image.")
        cv2.waitKey(0)  # Waits indefinitely until a key is pressed
    else:
        print("Image will close after 10s")
        time.sleep(10)

    cv2.destroyAllWindows()


def saveImage(fileName):
    print("Ready to save the image ...")
    ret, frame = captureImage()

    # The path of image to save
    currentPath = os.getcwd()
    testPatternPath = currentPath + "\\test_pattern\\"

    # Save the captured image
    imageFilename = testPatternPath + fileName
    cv2.imwrite(imageFilename, frame)
    print(f"Image captured and saved as {imageFilename}")

    return imageFilename


def removeImage(fileName):
    print("Ready to remove the image ...")
    currentPath = os.getcwd()
    testPatternPath = currentPath + "\\test_pattern\\"
    imageFilename = testPatternPath + fileName

    try:
        os.remove(imageFilename)
        print(f"File {imageFilename} removed successfully")
    except FileNotFoundError:
        print(f"File {imageFilename} not found")
    except Exception as e:
        print(f"An error occurred: {e}")


def checkIfDisplayed(fileName):
    # Get the capture from camera
    imageFilename = saveImage("inTest.jpg")
    time.sleep(3)

    # Read the images
    fromTestPattern = io.imread(fileName)
    fromCameraCapture = io.imread(imageFilename)

    # Convert the images to grayscale
    fromTestPatternGray = color.rgb2gray(fromTestPattern)
    fromCameraCaptureGray = color.rgb2gray(fromCameraCapture)

    # Specify the data_range parameter (assuming 0 to 255 for typical images)
    dataRange = fromTestPatternGray.max() - fromTestPatternGray.min()

    # Calculate the SSIM score
    similarityIndex, _ = ssim(fromTestPatternGray, fromCameraCaptureGray, full=True, data_range=dataRange)
    print(f"SSIM: {similarityIndex}")
    # Calculate the MSE score
    mseScore = mse(fromTestPatternGray, fromCameraCaptureGray)
    print(f"MSE: {mseScore}")

    removeImage("inTest.jpg")

    # # TODO: Waiting to discuss and test how much SSIM score needs to be greater than
    # # A Higher score indicates higher similarity
    # print(f"SSIM: {similarityIndex}")
    # # A lower MSE indicates higher similarity
    # print(f"MSE: {mseScore}")
    # #
    # print(f"NCC: {nccScore}")



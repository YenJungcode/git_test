import time
import cv2


def setCamera(device):
    global deviceCamera
    # 0 represents the default camera, change if you have multiple cameras
    deviceCamera = device


# Capture a frame
def captureImage():
    global deviceCamera
    capture = cv2.VideoCapture(deviceCamera)
    if not capture.isOpened():
        assert "Cannot open camera !!!"

    ret, frame = capture.read()
    if not ret:
        assert "Failed to capture an image !!!"

    return ret, frame
    # Release the camera
    capture.release()


# action : manual = Please print any key to close the image.
# action : other = Image will close after 10s.
def showImage(action):
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
    ret, frame = captureImage()

    # Save the captured image
    image_filename = fileName
    cv2.imwrite(image_filename, frame)
    print(f"Image captured and saved as {image_filename}")
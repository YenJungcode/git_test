import time
import cvStep



if __name__ == "__main__":

   cvStep.setCamera(0)
   imageFilename = cvStep.saveImage("test.jpg")

   time.sleep(5)
   cvStep.checkIfDisplayed(imageFilename)



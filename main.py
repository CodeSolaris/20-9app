import cv2
from emailing import send_email
from glob import glob
import os
from threading import Thread
from time import sleep
# Initialize video capture
video_capture = cv2.VideoCapture(0)

# Set initial frame as None
first_frame = None
status_list = []
count = 1

def clean_folder():
    all_images = glob("images/*.jpg")
    for image in all_images:
        os.remove(image)
while True:
    status = 0
    # Read frame from video capture
    check, frame = video_capture.read()
    if not check:
        break

    # Convert frame to grayscale and apply Gaussian blur
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gaussian = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        # Set first frame as the initial frame
        first_frame = gray_frame_gaussian

    # Calculate the absolute difference between the current frame and the first frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gaussian)

    # Apply thresholding to obtain a binary image
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]

    # Dilate the thresholded image to fill in gaps
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Display the resulting frame
    # cv2.imshow("Capturing", dil_frame)

    # Find contours in the dilated frame
    contours, check = cv2.findContours(
        dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Iterate over contours and draw rectangles around large enough contours
    for contour in contours:
        if cv2.contourArea(contour) < 7000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.jpg", frame)
            count += 1
            all_images = glob("images/*.jpg")
            index = int(len(all_images) / 2)
            image_path = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        thread_email = Thread(target=send_email, args=(image_path,))
        thread_email.daemon = True
        thread_clean = Thread(target=clean_folder)
        thread_clean.daemon = True

        thread_email.start()
        

    cv2.imshow("Video", frame)
    # Check for 'q' key press to exit the loop
    key = cv2.waitKey(1)
    if key == ord("q"):
        thread_clean.start()
        sleep(5)
        break

# Release the video capture
video_capture.release()



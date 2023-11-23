import cv2

# Initialize video capture
video_capture = cv2.VideoCapture(0)

# Set initial frame as None
first_frame = None

while True:
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
    cv2.imshow("Capturing", dil_frame)

    # Find contours in the dilated frame
    contours, _ = cv2.findContours(
        dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Iterate over contours and draw rectangles around large enough contours
    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Check for 'q' key press to exit the loop
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Release the video capture
video_capture.release()

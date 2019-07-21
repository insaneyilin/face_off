import cv2
from video_capture_app import VideoCaptureApp


# face_img_path = 'data/images/batman_head.jpg'
face_img_path = 'data/images/wuyanzu.jpg'
vid_cap = VideoCaptureApp(capture=cv2.VideoCapture('data/videos/david.webm'),
		face_img_path=face_img_path, should_mirror=True)
vid_cap.run()

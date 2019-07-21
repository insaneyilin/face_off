import cv2
from video_capture_app import VideoCaptureApp


face_img_path = 'data/images/batman_head.jpg'
vid_cap = VideoCaptureApp(face_img_path=face_img_path, should_mirror=True)
vid_cap.run()

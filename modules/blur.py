import cv2

def blur_face(frame, x, y, w, h):
    face = frame[y:y+h, x:x+w]
    face = cv2.GaussianBlur(face, (99, 99), 30)
    frame[y:y+h, x:x+w] = face
    return frame
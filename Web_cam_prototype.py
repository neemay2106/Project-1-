import cv2
from cv2.gapi.wip.draw import Circle

toggle = False
toggle2 = False
toggle_flip = False

out = None
recording = False
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
cv2.namedWindow('Webcam feed')
circle_container = []
def draw_circle(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        circle_container.append((x,y))

cv2.setMouseCallback('Webcam feed', draw_circle)

while True:
    ret,frame = cap.read()

    if not ret:
        break
    key = cv2.waitKey(1) & 0xFF# waits for 1 millisecond - while loops runs multiple times in a second so it works


    frame = cv2.resize(frame,(640,480))
    #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame = cv2.rectangle(frame ,(250,50),(640,480),(0,255,0),2)
    frame = cv2.putText(frame ,  "neemay", (395,40),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2 )

    for (x,y) in circle_container:
        cv2.circle(frame,(x,y),100,(255,255,255))
    if key == ord('g'):
        toggle = True
        toggle2 = False
    if key == ord('b'):
        toggle = False
        toggle2 = False
        toggle_flip = False
    if key == ord('i'):
        toggle2 = True
        toggle = False


    display_frame = frame.copy()


    if toggle:
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if toggle2:
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



    if key == ord('t'):
        toggle_flip = True
    if toggle_flip:
        display_frame = cv2.rotate(display_frame, cv2.ROTATE_90_CLOCKWISE)

    if key == ord('q'):
        cap.release()
        break
    if key == ord("p"):
        cv2.imwrite("file.png", display_frame)



    if key == ord('r'):
        out = cv2.VideoWriter("my_vid.mp4", fourcc, 30, (display_frame.shape[1], display_frame.shape[0]))
        recording = True
        print("VideoWriter opened?", out.isOpened())
        print("recording...")

    if key == ord('s'):
        out.release()
        out = None
        recording = False
        print("stoped recording")
    if recording and out is not None:
        out.write(display_frame)
    cv2.imshow('Webcam feed', display_frame)



cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()



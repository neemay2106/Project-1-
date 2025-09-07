import cv2
import torch
import time as tm

toggle = False
toggle2 = False
toggle_flip = False
toggle_ai = False

out = None
recording = False

#setting up the feed
cap = cv2.VideoCapture(0) # creates a videocapture object , the 0 means its accessing the default camera
cap.set(cv2.CAP_PROP_FPS, 30) # the set method takes two arguments propId ( id of the property u wanna change) and the value u want to change it too
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)#cv2.CAP_PROP_FRAME_WIDTH and the others are key values it get and we can change too desired
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


print("Camera FPS:", cap.get(cv2.CAP_PROP_FPS))
print("Camera Width:", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("Camera Height:", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

list1 = []

fourcc = cv2.VideoWriter_fourcc(*'mp4v') # it does work lamo , this gets a 4 digit code specific to mp4v or anything we choose so we can tell video writer which format we wabt the video to be stored in
cv2.namedWindow('Webcam feed')



#Drawing circles on clicking the mouse
circle_container = []
def draw_circle(event,x_cor,y_cor,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:# .EVENT_LBUTTONDOWN tells openCV that the left mouse button was clicked
        circle_container.append((x_cor,y_cor))
cv2.setMouseCallback('Webcam feed', draw_circle)# when mouse is on screen or when left button is clicked the method attaches the function to the window and then opencv backend gives the values



# using torch to load in the model
model = torch.hub.load('yolov5', 'yolov5s', source='local', pretrained=True)

frame_count = 0
start = tm.time()
frame_duration = 1/30



while True:
     #finds time at the start of the loop or when the frame is created
    ret,frame = cap.read() # ret returns true or false values if the frame is read or not, and frame get the frame and stores it as a numpy array

    if not ret:
        break
    key = cv2.waitKey(1) & 0xFF# waits for 1 millisecond - while loops runs multiple times in a second so it works







    frame = cv2.resize(frame,(640,480))


    for (x,y) in circle_container:
         cv2.circle(frame,(x,y),100,(255,255,255))



    if key == ord('a'):
        toggle_ai= True

    if toggle_ai:
        results = model(frame)
        detections = results.xyxy[0]
        for det in detections:
            x1 = str(det[0].item())  # x_min
            y1 = str(det[1].item())  # y_min
            x2 = str(det[2].item())  # x_max
            y2 = str(det[3].item() ) # y_max
            conf = det[4].item()  # confidence score
            cls = str(det[5].item())
            list1.append(cls)
            list1.append(x1)
            list1.append(y1)
        with open('frame_file.txt', "w") as f:
            for i in list1:
                f.write(i)
        frame = results.render()[0].copy() # essentially making a box around the objects



    frame = cv2.rectangle(frame, (250, 50), (640, 480), (0, 255, 0), 2)
    frame = cv2.putText(frame, "neemay", (395, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    display_frame = frame.copy() #the reason we created the display frame is so that we are able to have both the ai and the rectangle made by cv on the screen

    #make it grayscale
    if key == ord('g'):
         toggle = True
         toggle2 = False
    if toggle:
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #make it innverted
    if key == ord('i'):
         toggle2 = True
         toggle = False
    if toggle2:
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    #to flip
    if key == ord('t'):
        toggle_flip = True
    if toggle_flip:
        display_frame = cv2.rotate(display_frame, cv2.ROTATE_90_CLOCKWISE)

    # to get it back to normal
    if key == ord('b'):
         toggle = False
         toggle2 = False
         toggle_flip = False
         toggle_ai = False

    if key == ord('q'):
        cap.release()
        break
    if key == ord("p"):
        cv2.imwrite("file.png", display_frame)


    #Recording

    if key == ord('r'):
         out = cv2.VideoWriter("my_vid.mp4", fourcc, 30, (display_frame.shape[1], display_frame.shape[0]))  # creates a video file to save im mp4 style based on the fourcc
         recording = True
         print("VideoWriter opened?", out.isOpened())
         print("recording...")


    if key == ord('s'):
        out.release()
        out = None
        recording = False
        print("stoped recording")
    if recording and out is not None:
        if recording and out is not None:
            now = tm.time()
            elapsed = now - start
            start = now
            frame_count += 1


            # Always write the current frame
            out.write(display_frame) # puts the frame in video (so as iterations go one it puts more and makes a video)

            # Calculate how many frames should have happened in "elapsed"
            expected_frames = int(round(elapsed / frame_duration))
            if expected_frames < 1:
                expected_frames = 1

            # Write duplicates if needed
            for _ in range(expected_frames - 1):
                out.write(display_frame)

    e = tm.time() - start
    fps = 1/e

    cv2.putText(display_frame, f"{fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            # Smooth FPS estimate






    cv2.imshow('Webcam feed', display_frame)



cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()



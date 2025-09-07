import time
import cv2
#
# start = time.time()
# # some code to measure
# for i in range(1000000):
#     pass
# end = time.time()
#
# print("Execution time:", end - start, "seconds")
#
#
# im = cv2.imread("/Users/neemayrajan/Desktop/SurDrone/Inaugurated-in-November-2021--the-Chandigarh-Bird-_1727120632738.webp")
#
# if im is None:
#     print("Failed to load image")
# else:
#     cv2.imshow("image", im)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#     (b,g,r) = im[20,20]
#     print("b=",b,"g=",g,"r=",r)



cap = cv2.VideoCapture(0)
print(cap.get(cv2.CAP_PROP_FPS))
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
p = False
out = None
recording = False
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
while True:
    ret , frame = cap.read()
    # print("is the frame read??",ret )

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cap.release(  )
        cv2.destroyAllWindows()
        break
    if key == ord('s'):
        p = True
    if p:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if key == ord("r"):
        out = cv2.VideoWriter("Test.mp4",fourcc, 30, (frame.shape[1], frame.shape[0]))
        recording = True
    if key == ord('t'):
        recording = False
    if recording and out is not None:
        out.write(frame)





    cv2.imshow('Webcam feed', frame)



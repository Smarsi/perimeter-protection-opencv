import cv2

from controller import DrawObject
global_draw_object = DrawObject()

# Camera configuration
camera = cv2.VideoCapture(0)
original_fps = int(camera.get(cv2.CAP_PROP_FPS))

def calc_perimiter(contour):
    return cv2.arcLength(contour, True)

def mouse_event(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"X: {x}, Y: {y}")
        global_draw_object.set_initial(x, y)

    if event == cv2.EVENT_LBUTTONUP:
        print(f"X: {x}, Y: {y}")
        global_draw_object.set_final(x, y)

    if event == cv2.EVENT_RBUTTONDOWN:
        global_draw_object.reset()

while True:

    (grabbed, frame) = camera.read()

    if not grabbed:
        break

    frame = frame.copy()

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # edges = cv2.Canny(gray, 50, 150)

    # contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # # Running through all contours
    # for contour in contours:
    #     perimeter = calc_perimiter(contour)
    #     cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

    #     if perimeter > 100:
    #         cv2.putText(frame, "Perimetro Protegido", (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    

    if global_draw_object.is_ready:
        cv2.rectangle(frame, (global_draw_object.initial_x, global_draw_object.initial_y), (global_draw_object.final_x, global_draw_object.final_y), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    cv2.setMouseCallback("Frame", mouse_event)

camera.release()
cv2.destroyAllWindows()


import cv2
import argparse
import numpy as np

from controller import DrawObject
global_draw_object = DrawObject()

global_detection = False

ap = argparse.ArgumentParser()

ap.add_argument('-v', '--video', required=True,
                help = 'path to input device')

ap.add_argument('-c', '--config', required=True,
                help = 'path to yolo config file')

ap.add_argument('-cl', '--classes', required=True,
                help = 'path to text file containing class names')

ap.add_argument('-w', '--weights', required=True,
                help = 'path to yolo pre-trained weights')

args = ap.parse_args()


# Camera configuration
camera = cv2.VideoCapture(args.video)
original_fps = int(camera.get(cv2.CAP_PROP_FPS))


def get_output_layers(net):
    
    layer_names = net.getLayerNames()
    try:
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    except:
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):

    label = str(classes[class_id])

    color = COLORS[class_id]

    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)

    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def mouse_event(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"X: {x}, Y: {y}")
        global_draw_object.set_initial(x, y)

    if event == cv2.EVENT_LBUTTONUP:
        print(f"X: {x}, Y: {y}")
        global_draw_object.set_final(x, y)

    if event == cv2.EVENT_RBUTTONDOWN:
        global_draw_object.reset()

classes = None

with open(args.classes, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
net = cv2.dnn.readNet(args.weights, args.config)

while True:
    global_detection = False
    (grabbed, frame) = camera.read()

    frame = frame.copy()

    Width = frame.shape[1]
    Height = frame.shape[0]
    scale = 0.00392

    if global_draw_object.is_ready:
        cv2.rectangle(frame, (global_draw_object.initial_x, global_draw_object.initial_y), (global_draw_object.final_x, global_draw_object.final_y), (0, 255, 0), 2)

        blob = cv2.dnn.blobFromImage(frame, scale, (416,416), (0,0,0), True, crop=False)
        net.setInput(blob)

        outs = net.forward(get_output_layers(net))


        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and class_id == 0:
                    center_x = int(detection[0] * Width)
                    center_y = int(detection[1] * Height)
                    w = int(detection[2] * Width)
                    h = int(detection[3] * Height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        for i in indices:
            try:
                box = boxes[i]
            except:
                i = i[0]
                box = boxes[i]
            
            x = box[0]
            y = box[1]
            w = box[2]
            h = box[3]

            for point in range(global_draw_object.initial_x, global_draw_object.final_x):
                if x < point < x + w:
                    for point_y in range(global_draw_object.initial_y, global_draw_object.final_y):
                        if y < point_y < y + h:
                            global_detection = True
            draw_prediction(frame, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

    if global_detection:
        cv2.putText(frame, "INVASOR DETECTADO", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    cv2.setMouseCallback("Frame", mouse_event)

camera.release()
cv2.destroyAllWindows()


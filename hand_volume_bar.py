import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ------------------ Pycaw Setup ------------------
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_min, vol_max = volume.GetVolumeRange()[:2]

# ------------------ MediaPipe Setup ------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# ------------------ Webcam ------------------
cap = cv2.VideoCapture(0)

# For smoothing
vol_bar = 400  # initial position of the bar
vol_percentage = 0

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            if lm_list:
                x1, y1 = lm_list[4][1], lm_list[4][2]   # Thumb tip
                x2, y2 = lm_list[8][1], lm_list[8][2]   # Index tip

                # Draw circles and line
                cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

                # Calculate distance
                length = math.hypot(x2 - x1, y2 - y1)

                # Map distance to volume range
                vol = np.interp(length, [20, 200], [vol_min, vol_max])
                vol_bar = np.interp(length, [20, 200], [400, 150])  # bar position
                vol_percentage = np.interp(length, [20, 200], [0, 100])
                volume.SetMasterVolumeLevel(vol, None)

    # Draw volume bar
    cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 0), 3)  # bar outline
    cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, f'{int(vol_percentage)} %', (40, 430),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    cv2.imshow("Gesture Volume Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

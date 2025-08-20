import cv2
import mediapipe as mp

# ------------------ Setup MediaPipe ------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # track only one hand
mp_draw = mp.solutions.drawing_utils

# ------------------ Capture Webcam ------------------
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    # Convert to RGB for MediaPipe
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # Draw hand landmarks and extract coordinates
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            if lm_list:
                thumb_tip = lm_list[4]   # Thumb tip
                index_tip = lm_list[8]   # Index tip
                print(f"Thumb: {thumb_tip}, Index: {index_tip}")

    # Display webcam feed
    cv2.imshow("Hand Tracking", img)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

"""MediaPipe wrapper. This is the only file that imports MediaPipe.

Uses the Tasks HandLandmarker in IMAGE mode with num_hands=2. The model file
(hand_landmarker.task) gets downloaded in the Dockerfile, don't commit it.
"""

import os
from functools import lru_cache

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import BaseOptions, vision

MODEL_PATH = os.environ.get(
    "HAND_MODEL_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task"),
)

# MediaPipe labels hands as if the image were a mirrored selfie. The browser
# sends unmirrored frames, so swap the labels to get the player's own hands.
# Check on a real hand: hold up only your left hand, it should say "Left".
SWAP_HANDEDNESS = True
SWAPPED = {"Left": "Right", "Right": "Left"}


@lru_cache(maxsize=1)
def get_landmarker():
    """Load the model once, the first time it's needed."""
    options = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=vision.RunningMode.IMAGE,
        num_hands=2,
    )
    return vision.HandLandmarker.create_from_options(options)


def decode_jpeg(jpeg):
    """Turn JPEG bytes into an RGB array. Raises ValueError if it isn't an image."""
    bgr = cv2.imdecode(np.frombuffer(jpeg, dtype=np.uint8), cv2.IMREAD_COLOR)
    if bgr is None:
        raise ValueError("couldn't decode the image")
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)


def find_hands(jpeg):
    """Find the hands in one JPEG frame (bytes).

    Returns (hands, aspect):
    - hands: [{"label": "Left", "points": [(x, y), ...]}, ...] with the 21
      points normalized to 0-1 and not mirrored. "Left" is the player's own
      left hand.
    - aspect: the frame's width / height, for logic.fingers_up
    """
    rgb = decode_jpeg(jpeg)
    height, width = rgb.shape[:2]
    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = get_landmarker().detect(image)

    hands = []
    for landmarks, handedness in zip(result.hand_landmarks, result.handedness):
        label = handedness[0].category_name
        if SWAP_HANDEDNESS:
            label = SWAPPED.get(label, label)
        hands.append({"label": label, "points": [(p.x, p.y) for p in landmarks]})
    return hands, width / height

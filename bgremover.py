import cv2
import math
import numpy as np
import mediapipe as mp
import argparse


# Graycolors for segmentation mask
BG_COLOR = (192, 192, 192)  # gray
MASK_COLOR = (255, 255, 255)  # white

# Windows size for showing intermediate results
MAX_SIZE = 480

# Arguments
def parse_args() -> argparse.Namespace:

    """Parses and returns the command line arguments
    Returns:
        argparse.Namespace: parsed arguemnts
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--image",
        type=str,
        required=True,
        help="path to the input image",
    )

    parser.add_argument(
        "-b",
        "--background",
        type=str,
        required=False,
        help="path to the background image",
        default=None,
    )

    parser.add_argument(
        "-t",
        "--thresshold",
        type=float,
        required=False,
        help="thresshold to classify foreground and background",
        default=0.1,
    )

    args = parser.parse_args()
    return args


def resize_ratio(image):
    """Resize the image to the defined size keeping ratio

    Args:
        image (image): Image to resize

    Returns:
        image: Resized image
    """
    h, w = image.shape[:2]
    if h < w:
        img = cv2.resize(image, (MAX_SIZE, math.floor(h / (w / MAX_SIZE))))
    else:
        img = cv2.resize(image, (math.floor(w / (h / MAX_SIZE)), MAX_SIZE))
    return img


def main(args):
    """Perform the a background removal/chage using mediapipe

    Args:
        args (argparse.Namespace): Arguments for the process: image, background and ratio
    """
    # Read images with OpenCV.
    image = cv2.imread(args.image)
    # Prepare selfie segmentation
    mp_selfie_segmentation = mp.solutions.selfie_segmentation

    with mp_selfie_segmentation.SelfieSegmentation() as selfie_segmentation:
        # Convert the BGR image to RGB and process it with MediaPipe Selfie Segmentation.
        print(f"Image shape: {image.shape}")
        results = selfie_segmentation.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Generate solid color images for showing the output selfie segmentation mask.
        fg_image = np.zeros(image.shape, dtype=np.uint8)
        fg_image[:] = MASK_COLOR
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        # Apply the thresshold to set what is background and foreground, a lower ratio will keep less pixels from the original image
        # and higher values will keep more pixels from the original image.
        condition = (
            np.stack((results.segmentation_mask,) * 3, axis=-1) > args.thresshold
        )
        # Apply the condition to generate the image
        output_image = np.where(condition, fg_image, bg_image)
        output_image = resize_ratio(output_image)
        cv2.imshow("main", output_image)
        cv2.waitKey(0)

        # This code will generate a transparent image (PNG) and save it to disk (imshow do not show alpha channels) if the
        # background image is not provide, in other case it will show the composition of the backgrund and the image.
        if args.background is None:
            transparent_layer = np.zeros(
                (image.shape[0], image.shape[1]), dtype=np.uint8
            )
            opaque_layer = np.ones((image.shape[0], image.shape[1]), dtype=np.uint8)
            condition = np.stack(results.segmentation_mask, axis=0) > args.thresshold
            output_image = np.where(condition, opaque_layer, transparent_layer)
            transparent_image = np.dstack((image, (output_image * 255)))
            transparent_image = resize_ratio(transparent_image)
            cv2.imwrite("output_alpha.png", transparent_image)

        else:
            background = cv2.imread(args.background)
            output_image = np.where(condition, image, background)
            output_image = resize_ratio(output_image)
            cv2.imwrite("output_background.png", output_image)
            cv2.imshow("main", output_image)
            cv2.waitKey(0)


if __name__ == "__main__":
    args = parse_args()
    main(args)

# Bgremoval with Mediapipe

The goal here is using mediapipe to generate a background removal/shifter for normal images.

## Dependencies

* Mediapipe
* OpencV
* Numpy

## Run the script:

* To generate a transparent png images:

`python bgremover.py -i ./images/image.jpg`

* To swap backgrounds:

`python bgremover.py -i ./images/image.jpg -b ./images/background.jpg`

* To modify the thresshold for the segmentation:


`python bgremover.py -i ./images/image.jpg -b ./images/background.jpg -t 0.2`

![image_small](https://user-images.githubusercontent.com/1952508/157209602-cbf821b0-60a5-490f-866f-56899641a368.jpg  | width=256)
![output](https://user-images.githubusercontent.com/1952508/157206774-a03b0745-f9b9-4903-9eb0-762b169efd1b.png  | width=256)
![output_background](https://user-images.githubusercontent.com/1952508/157209344-6ad3203d-5944-4752-a675-81af0050278a.png  | width=256)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
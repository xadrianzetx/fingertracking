# fingertracking


OpenCV based finger pointing detection and gesture recognition used to control IoT devices

## Gesture recognition

<p align="center">
<image src="https://github.com/xadrianzetx/fingertracking/blob/master/assets/hand_track.gif"></image>
</p>


Hand tracking and gesture recognition based on Single Shot Detector with MobileNet V2 as feature extractor. This works by calculating center of bounding box with highest proba, and then tracing movement of this point through capture areas. Order in which areas are visited is compared to pre defined list of available moves and information is propagated to browser based UI if match is found. [Model checkpoint](https://github.com/victordibia/handtracking/tree/master/model-checkpoint/ssdlitemobilenetv2) was exported to frozen graph using tensorflow 1.11.0

## Detecting pointing direction

<p align="center">
<image src="https://github.com/xadrianzetx/fingertracking/blob/master/assets/ft5.gif"></image>
</p>


Hand detection is done by sampling image from pre defined area and calculating HSV histogram. This allows to pick up skin tone. Each frame is then thresholded and pixels falling out of calculated distribution are masked. Next step is to create contour of non-masked area, calculate its centroid and outermost point - the fingertip. Line between those two points gives us pointing direction, and its linear function is found in order to extrapolate pointing direction in relation to upper edge of frame, where device hit boxes are located.

## Server

App runs on Flask based server and has open connection to Redis database running from Docker container on Raspberry Pi Zero. This solution allows to run multiple instances of app controlling multiple devices on variety of endpoints scattered around location within one network. State of every device is kept in db allowing administration and handling endpoint failures. Each endpoint has minimalistic browser based UI.

## Run

```
git clone https://github.com/xadrianzetx/fingertracking.git
python app.py
```

Requires Redis connection.

## TODO

Contenerize app to run on ARMv7 endpoint (Rpi3)

## References

* [Histograms](https://docs.opencv.org/3.1.0/d1/db7/tutorial_py_histogram_begins.html)
* [Image thresholding](https://en.wikipedia.org/wiki/Thresholding_(image_processing))
* [Victor Dibia, Real-time Hand-Detection using Neural Networks (SSD) on Tensorflow, (2017), GitHub repository](https://github.com/victordibia/handtracking)
* [SSD: Single Shot MultiBox Detector](https://arxiv.org/abs/1512.02325)
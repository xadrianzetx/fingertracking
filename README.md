# fingertracking


OpenCV based finger pointing detection and gesture recognition used to control IoT devices

## Detecting pointing direction

<p align="center">
<image src="https://github.com/xadrianzetx/fingertracking/blob/master/assets/ft5.gif"></image>
</p>


Hand detection is done by sampling image from pre defined area and calculating HSV histogram. This allows to pick up skin tone. Each frame is then thresholded and pixels falling out of calculated distribution are masked. Next step is to create contour of non-masked area, calculate its centroid and outermost point - the fingertip. Line between those two points gives us pointing direction, and its linear function is found in order to extrapolate pointing direction in relation to upper edge of frame, where device hit boxes are located.

## Gesture recognition

** Under developement **

Based on Single Shot Detector with MobileNet V2 as feature extractor. [Model checkpoint](https://github.com/victordibia/handtracking/tree/master/model-checkpoint/ssdlitemobilenetv2) was exported to frozen graph using tensorflow 1.11.0

# Server

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
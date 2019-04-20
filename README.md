# fingertracking


OpenCV based finger pointing detection used to control IoT devices

<p align="center">
<image src="https://github.com/xadrianzetx/fingertracking/blob/master/assets/ft5.gif"></image>
</p>

## Tracking

Hand detection is done by sampling image from pre defined area and calculating HSV histogram. This allows to pick up skin tone. Each frame is then thresholded and pixels falling out of calculated distribution are masked. Next step is to create contour of non-masked area, calculate its centroid and outermost point - the fingertip. Line between those two points gives us pointing direction, and its linear function is found in order to extrapolate pointing direction in relation to upper edge of frame, where device hit boxes are located.

## Server

App runs on Flask based server and has open connection to Redis database running from Docker container on Raspberry Pi Zero. This solution allows to run multiple instances of app controlling multiple devices on variety of endpoints scattered around location within one network. State of every device is kept in db allowing administration and handling endpoint filures. Each endpoint has minimalistic browser based UI.

## Run

'''
git clone https://github.com/xadrianzetx/fingertracking.git
python app.py
'''

Requires Redis connection.

## TODO

Contenerize app to run on ARMv7 endpoint (Rpi3)
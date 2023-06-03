# Create report in html format with image.

This script generates HTML reports with images and JSON data. It converts the HTML reports to images and combines them into a video.
It is useful when you have image and meta data related to image.
It creates HTML, Images, and Video.

## Prerequisites

### Install `wkhtmltoimage`
1. Open a terminal.

2. Add the wkhtmltopdf package repository:

```shell
Copy code
sudo apt-add-repository -y ppa:ecometrica/servers
Update the package lists:
sudo apt update
sudo apt install wkhtmltopdf
```
3. To verify the installation, you can run the following command in the terminal to check the version of wkhtmltoimage:

```shell
wkhtmltoimage --version
```

### Install Python Dependencies
```shell
pip install -r requirements.txt
```

## Usage

```shell
python report.py [--image-directory IMAGE_DIRECTORY] [--json-directory JSON_DIRECTORY]
                [--output-directory OUTPUT_DIRECTORY] [--video-output VIDEO_OUTPUT]
                [--image-width IMAGE_WIDTH] [--image-height IMAGE_HEIGHT]
                [--frame-rate FRAME_RATE]
```

Optional Arguments:

--image-directory IMAGE_DIRECTORY: Path to the directory containing the input images (default: "images").
--json-directory JSON_DIRECTORY: Path to the directory containing the JSON files (default: "meta").
--output-directory OUTPUT_DIRECTORY: Path to the directory where the HTML reports will be saved (default: "html_reports").
--video-output VIDEO_OUTPUT: Path to the output video file (default: "output.mp4").
--image-width IMAGE_WIDTH: Width of the output images and video frames (default: 1280).
--image-height IMAGE_HEIGHT: Height of the output images and video frames (default: 720).
--frame-rate FRAME_RATE: Frame rate of the output video (default: 5).
Note: The script expects the input images and JSON files to have the same filename (except for the extension). For example, if the image is "image1.jpg", the corresponding JSON file should be "image1.json".

## Example
```shell
python report.py --image-directory images --json-directory meta --output-directory html_reports
                 --video-output output.mp4 --image-width 1280 --image-height 720 --frame-rate 5
```

This example generates HTML reports from images in the "images" directory using the JSON data from the "meta" directory. The HTML reports are saved in the "html_reports" directory. The output video file "output.mp4" is created with a width of 1280 pixels, a height of 720 pixels, and a frame rate of 5 frames per second.

You can adjust the values of the optional arguments according to your requirements.
import glob
import json
import os
import re
from datetime import datetime
import imgkit

import cv2
import typer
from yattag import Doc, indent


def get_datetime_from_filename(filename):
    pattern = r"-(\d+)\."
    match = re.search(pattern, filename)
    if match:
        epoch_time = int(match.group(1))
        datetime_obj = datetime.fromtimestamp(epoch_time)
        datetime_str = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")
        return datetime_str
    else:
        return None


# Function to generate the HTML report
def generate_html_report(report_id, image_path, json_data):

    # Create a new HTML document
    doc, tag, text = Doc(
        defaults={'ingredient': ['chocolate', 'coffee']}
    ).tagtext()

    # Add the HTML content
    with tag("html"):
        with tag("head"):
            with tag("title"):
                text("Report")
            with tag("style"):
                # Add the CSS code here
                with open('css/default.css', 'r') as file:
                    css_code = file.read()
                text(css_code)
        with tag("body"):
            with tag("h1"):
                text(f"Report {report_id}")

            file_name = os.path.basename(image_path)
            timeTaken = get_datetime_from_filename(file_name)

            if timeTaken is None:
                with tag("h2"):
                    text(f"File name： {file_name}")

            else:
                with tag("h2"):
                    text(f"Photo taken at {timeTaken}")

            with tag("div", klass="rwd-table"):
                with tag("img", src=image_path):
                    pass


                with tag("table", klass="rwd-table"):
                    # Generate HTML report table headers dynamically based on JSON keys
                    with tag("tr"):
                        with tag("th"):
                            text("Item")
                        for key in json_data[next(iter(json_data))].keys():
                            with tag("th"):
                                text(key.capitalize().replace("_", " "))

                    # Add the data rows dynamically based on JSON values
                    for item, item_data in json_data.items():
                        with tag("tr"):
                            with tag("td"):
                                text(item)
                            for value in item_data.values():
                                with tag("td"):
                                    text(str(value))

    return indent(doc.getvalue())


def main(
    image_directory: str = "images", # it must be absolute path for image loading.
    json_directory: str = "meta",
    output_directory: str = "html_reports",
    video_output: str = "output.mp4",
    image_width: int = 1280,
    image_height: int = 720,
    frame_rate: int = 5,
):
    image_files = sorted(glob.glob(os.path.join(image_directory, "*.jpg")))
    os.makedirs(output_directory, exist_ok=True)

    reports = []
    for i, image_file in enumerate(image_files, start=1):
        image_name = os.path.basename(image_file)
        json_file = os.path.join(
            json_directory, f"{os.path.splitext(image_name)[0]}.json"
        )

        with open(json_file) as f:
            json_data = json.load(f)

        reports.append({"image_path": image_file, "json_data": json_data})

        html_report = generate_html_report(i, image_file, json_data)
        report_file = os.path.join(output_directory, f"report_{i}.html")

        with open(report_file, "w") as file:
            file.write(html_report)

        image_output = os.path.join(output_directory, f"report_{i}.jpg")

        options = {
            'format': 'jpg',
            'encoding': "UTF-8",
            'enable-local-file-access': None
        }

        imgkit.from_file(report_file, image_output, options=options)


    images = sorted(glob.glob(os.path.join(output_directory, "*.jpg")))

    video = cv2.VideoWriter(
        video_output,
        cv2.VideoWriter_fourcc(*"mp4v"),
        frame_rate,
        (image_width, image_height),
    )

    for image in images:
        frame = cv2.imread(image)
        frame = cv2.resize(frame, (image_width, image_height))
        video.write(frame)

    cv2.destroyAllWindows()
    video.release()


if __name__ == "__main__":
    typer.run(main)

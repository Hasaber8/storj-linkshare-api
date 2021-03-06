from flask import Flask, jsonify, request
from requests.api import get
from shell_utils import run_command
from requests import head
import os
import re
import logging
from pycountry_convert import country_alpha2_to_continent_code

# This part is PixelExperience Specific but can be used as an example for other wanting to implement their stuff in Python + PhP.

app = Flask(__name__)
BUCKET_NAME = os.getenv("BUCKET_NAME")
API_TOKEN = os.getenv("API_TOKEN")
REQUIRED_ARGS = ["device", "build", "build_size", "api_token", "country"]
EXPIRE_TIME = "6h" # This creates a new link for each file every 6 hours, it is done to prevent deeplinking.
DEFAULT_MIRROR = "NA"

# As of now Storj doesnt automatically connects to the nearest Storage node so we have to do it manually.
STORJ_MIRRORS = {
    "AS": "link.ap1.storjshare.io",
    "AF": "link.ap1.storjshare.io",
    "OC": "link.ap1.storjshare.io",
    "EU": "link.eu1.storjshare.io",
    "NA": "link.us1.storjshare.io",
    "SA": "link.us1.storjshare.io"
}

# This fuction basically check if the bucket and file exist.
def file_exists(bucket_name, device, build, build_size):
    output = run_command('bin/uplink_linux_amd64 --config-dir config/ ls sj://{0}/{1}/{2}'.format(bucket_name, device, build))
    cmp = "{0} {1}/{2}".format(build_size, device, build)
    return cmp in output

# This validates the URL.
def is_link_valid(url):
    response = head(url, timeout=15)
    status_code = response.status_code
    if status_code != 200:
        app.logger.error('Linkshare url ' + url + ' return status: ' + str(status_code))
        return False
    return True

# The next two fuctions connects the user to the closest node and give them the valid url.
def get_closest_mirror(country):
    try:
        continent_code = country_alpha2_to_continent_code(country)
        return STORJ_MIRRORS[continent_code]
    except:
        return STORJ_MIRRORS[DEFAULT_MIRROR]

def share_link(bucket_name, device, build, expire_time, country):
    output = run_command('bin/uplink_linux_amd64 --config-dir config/ share sj://{0}/{1}/{2} --url --not-after +{3}'.format(bucket_name, device, build, expire_time))
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', output)
    for url in urls:
        url = url.replace('\\n', '').replace('\\', '')
        if build in url:
            url = url.replace("link.us1.storjshare.io", get_closest_mirror(country))
            if is_link_valid(url):
                return url
    app.logger.error('Unable to find linkshare url in output: ' + output)
    return False

@app.route('/')
def index():
    args = request.args
    for arg in REQUIRED_ARGS:
        if arg not in args:
            return jsonify(success=False, msg='Missing parameter: ' + arg)
    device = args["device"]
    build = args["build"]
    build_size = args["build_size"]
    api_token = args["api_token"]
    country = args["country"]
    if api_token != API_TOKEN:
        return jsonify(success=False, msg='Invalid token')
    if file_exists(BUCKET_NAME, device, build, build_size):
        url = share_link(BUCKET_NAME, device, build, EXPIRE_TIME, country)
        if not url:
            return jsonify(success=False, msg='Failed to generate linkshare url')
        return jsonify(success=True, url=url)
    return jsonify(success=False, msg='File not found')

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
#!/Users/jon.gaul/src/moonsetter/venv/bin/python

from datetime import datetime
import re
import requests
import os


log_okay = True
log_errors = True


def delete_old_wallpaper():
    for f in os.listdir():
        if re.search(r'curr_moon\d*\.tif', f):
            os.remove(f)


def download_current_moon_image():
    curr_year = 2025
    if datetime.now().year != curr_year:
        raise Exception('Year out of date')

    hours_since_new_years = int((datetime.utcnow() - datetime(curr_year, 1, 1)).total_seconds() // 3600 + 1)
    absolute_picture_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'curr_moon{hours_since_new_years}.tif')
    # nasa_url = f'https://svs.gsfc.nasa.gov/vis/a000000/a004800/a004874/frames/5760x3240_16x9_30p/plain/moon.{hours_since_new_years}.tif'
    # nasa_url = f'https://svs.gsfc.nasa.gov/vis/a000000/a004900/a004955/frames/5760x3240_16x9_30p/plain/moon.{hours_since_new_years:04d}.tif'
    # nasa_url = f'https://svs.gsfc.nasa.gov/vis/a000000/a005000/a005048/frames/5760x3240_16x9_30p/plain/moon.{hours_since_new_years:04d}.tif'
    # nasa_url = f'https://svs.gsfc.nasa.gov/vis/a000000/a005100/a005187/frames/5760x3240_16x9_30p/plain/moon.{hours_since_new_years:04d}.tif'
    nasa_url = f'https://svs.gsfc.nasa.gov/vis/a000000/a005400/a005415/frames/5760x3240_16x9_30p/plain/moon.{hours_since_new_years:04d}.tif'
    response = requests.get(nasa_url, verify=False)
    if response.status_code != 200:
        raise Exception(f'Bad status code: {response.status_code}')
    with open(absolute_picture_filename, 'wb') as pic_file:
        pic_file.write(response.content)
    return absolute_picture_filename


def set_wallpaper(picture_filename):
    os.system(f"""osascript -e 'tell application "System Events" to tell every desktop to set picture to "{picture_filename}" as POSIX file'""")


def log_info(info, should_log):
    if should_log:
        with open('log.txt', "a") as log_file:
            log_file.write(f'{datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}: {info}\n')


def main():
    try:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        delete_old_wallpaper()
        picture_filename = download_current_moon_image()
        set_wallpaper(picture_filename)
        log_info('OK', log_okay)
    except Exception as err:
        os.system(f"""osascript -e 'display notification "{err}" with title "Moon Script"'""")
        log_info(err, log_errors)


if __name__ == '__main__':
    main()

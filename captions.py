# modify these values
filename = 'videos.csv'                                           # filname with video ids
colname = 'contentDetails_videoId'                                # column storing video ids
publishedcolname = 'contentDetails_videoPublishedAt'              # column storing video upload time
delimiter = ','                                                   # delimiter, e.g. ',' for CSV or '\t' for TAB
waittime = 15                                                     # seconds browser waits before giving up
sleeptime = [5,10]                                                # random seconds range before loading next video id
headless = False                                                  # select True if you want the browser window to be invisible (but not inaudible)

# To enable AdBlock, it should be already installed on your Chorme nrowser
# Fetch the `Profile Path` from chrome://version and then find the extentions folder
# The AdBlock extention key is `cfhdojbkjhnklbpkdaibdccddilifddb`
# Add the version installed on your machine
# The overall path should look like this `/home/<USER>/.config/google-chrome/Default/Extensions/cfhdojbkjhnklbpkdaibdccddilifddb/<VERSION>/`
adblock_path = '/home/harris/.config/google-chrome/Default/Extensions/gighmmpiobklfepjocnamgkkbiglidom/5.16.0_0/'

#do not modify below
from time import sleep
import csv
import json
import random
import os.path

from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def storecaptions(writefilename, captions=""):
    file = open(writefilename,"w")
    file.write(captions)
    file.close() 

def format_transcript(data):
    # Check for the expected structure in the JSON file
    if 'events' in data:
        data = data['events']
    else:
        return "Unexpected JSON structure."

    # Initialize variables for the formatted transcript
    formatted_transcript = ""
    current_segment = ""
    segment_start_time = 0

    # Loop through each segment in the transcript
    for segment in data:
        if 'segs' in segment:
            # Calculate the start time of the segment
            start_time = segment.get('tStartMs', 0) // 1000

            # If this is the first segment or the current segment exceeds 5 seconds, start a new line
            if not current_segment or start_time - segment_start_time >= 5:
                if current_segment:
                    # Format and append the current segment to the transcript
                    minutes = segment_start_time // 60
                    seconds = segment_start_time % 60
                    formatted_transcript += f"[{minutes:02}:{seconds:02}] {current_segment.strip()}\n"
                current_segment = ""
                segment_start_time = start_time

            # Append the text of the current 'segs' to the current segment
            for seg in segment['segs']:
                current_segment += seg['utf8'] + " "

    # Append the last segment if it exists
    if current_segment:
        minutes = segment_start_time // 60
        seconds = segment_start_time % 60
        formatted_transcript += f"[{minutes:02}:{seconds:02}] {current_segment.strip()}\n"

    return formatted_transcript

def gettranscript(driver, videoid, publishedAt):
    # check if transcript file already exists
    filekey = "_".join([publishedAt, videoid]) if publishedAt else videoid
    writefilename = 'captions/transcript_%s.txt' % filekey
    writefilename_as_json = 'captions/transcript_%s.json' % filekey
    if os.path.isfile(writefilename) or os.path.isfile(writefilename_as_json):
        msg = 'transcript file already exists'
        return msg

    # navigate to video
    driver.get("https://www.youtube.com/watch?v=%s&vq=small" % videoid)

    try:
        element = WebDriverWait(driver, waittime).until(EC.presence_of_element_located((By.CLASS_NAME, "ytp-subtitles-button")))
    except:
        msg = 'could not find subtitles button'
        return msg

    # save an empty file if this video has no subtitles, so we don't revisit it if the script is run again
    if "unavailable" in element.get_attribute("title"):
        msg = 'video has no captions'
        storecaptions(writefilename)
        return msg

    # enable subtitles
    try:
        element.click()
    except:
        msg = 'could not click'
        return msg

    # wait for the subtitles to be fetched
    try: 
        request = driver.wait_for_request('/timedtext', timeout=15)
        captionsResp = request.response
        captions = ""
        if captionsResp:
            print("FOUND")
            if captionsResp.status_code >= 200 and captionsResp.status_code < 300:
                content = decode(captionsResp.body, captionsResp.headers.get('Content-Encoding', 'identity'))
                captions =  json.dumps(json.loads(content), sort_keys=True, indent=4) # json.loads(content)
                # captions = format_transcript(captions)
                storecaptions(writefilename, captions)
            else:
                print("Returned with error")
    except:
        msg = 'no captions'
        return msg

    # cool down
    sleep(random.uniform(sleeptime[0],sleeptime[1]))

    # clear all requests
    del driver.requests

    return 'ok'

# log function
def logit(id,msg):
    logwriter.writerow({'id':id,'msg':msg})
    

# prepare log file
logwrite = open('captions.log','w',newline='\n')
logwriter = csv.DictWriter(logwrite, fieldnames=['id','msg'])
logwriter.writeheader()

# read CSV file
csvread = open(filename, newline='\n')
csvreader = csv.DictReader(csvread, delimiter=delimiter, quoting=csv.QUOTE_NONE)
rowcount = len(open(filename).readlines())

# create driver
options = Options()

if adblock_path:
    options.add_argument('load-extension=' + adblock_path)

if headless:
    options.add_argument("--headless")

options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# track only youtube requests
driver.scopes = [
    '.*youtube.*',
]

if adblock_path:
    #let adblock installation finish
    sleep(10)
    #switch back to main tab
    driver.switch_to.window(driver.window_handles[0])

try: 
    for row in csvreader:
        videoId = row[colname]
        publishedOn = row[publishedcolname] if publishedcolname in row else None
        msg = gettranscript(driver, videoId, publishedOn)
        logit(row[colname],msg)
        rowcount -= 1
        print(str(rowcount) + " :  " + row[colname] + " : " + msg)
finally: 
    driver.quit()
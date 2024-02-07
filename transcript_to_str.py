import json

def storecaptions(writefilename, captions=""):
    file = open(writefilename,"w")
    file.write(captions)
    file.close() 

def format_transcript_v4(file_path):
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

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

# Example usage with the file path
formatted_transcript_v4 = format_transcript_v4('transcript__mEXEIwsNkU.json')

writefilename = 'transcript_%s.txt' % '_mEXEIwsNkU'
storecaptions(writefilename, formatted_transcript_v4)


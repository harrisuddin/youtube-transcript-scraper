import json
import os

def storecaptions(writefilename, captions=""):
    with open(writefilename, "w") as file:
        file.write(captions)

def format_transcript_v4(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    if 'events' in data:
        data = data['events']
    else:
        return "Unexpected JSON structure."

    formatted_transcript = ""
    current_segment = ""
    segment_start_time = 0

    for segment in data:
        if 'segs' in segment:
            start_time = segment.get('tStartMs', 0) // 1000
            if not current_segment or start_time - segment_start_time >= 5:
                if current_segment:
                    minutes = segment_start_time // 60
                    seconds = segment_start_time % 60
                    formatted_transcript += f"[{minutes:02}:{seconds:02}] {current_segment.strip()}\n"
                current_segment = ""
                segment_start_time = start_time

            for seg in segment['segs']:
                current_segment += seg['utf8'] + " "

    if current_segment:
        minutes = segment_start_time // 60
        seconds = segment_start_time % 60
        formatted_transcript += f"[{minutes:02}:{seconds:02}] {current_segment.strip()}\n"

    return formatted_transcript

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            formatted_transcript = format_transcript_v4(file_path)
            writefilename = filename.replace('.json', '.txt')
            storecaptions(save_path + writefilename, formatted_transcript)

# Example usage with the folder path
folder_path = 'captions/'
save_path = 'captions/processed/'
process_folder(folder_path)

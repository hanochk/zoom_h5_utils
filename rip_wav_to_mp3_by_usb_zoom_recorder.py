import os
import time
import psutil
from pydub import AudioSegment
from tqdm import tqdm
import argparse
def find_usb_drive(volume_label=None):
    """
    Detect connected USB drives. Optionally filter by volume label.

    Args:
        volume_label (str): Specific label of the USB drive to detect.

    Returns:
        str: Path to the detected USB drive, or None if not found.
    """
    for partition in psutil.disk_partitions():
        if "removable" in partition.opts.lower():
            if volume_label:
                # Match USB drive by its volume label
                try:
                    if os.path.basename(partition.device).startswith(volume_label):
                        return partition.mountpoint
                except Exception:
                    continue
            else:
                return partition.mountpoint
    return None


def convert_wav_to_mp3(input_directory, output_directory, bitrate="192k"):
    """
    Convert all WAV files in the input_directory to MP3 and save them in the output_directory.

    Args:
        input_directory (str): Path to the directory containing WAV files.
        output_directory (str): Path to the directory where MP3 files will be saved.
        bitrate (str): Desired bitrate for MP3 files (e.g., "192k").
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    for subdir, dirs, files in os.walk(input_directory):
        for subs_insub in dirs:
            for filename in tqdm(os.listdir(os.path.join(subdir, subs_insub))):
                full_path = os.path.join(subdir, subs_insub, filename)
                if full_path.lower().endswith(".wav"):
                    wav_path = full_path
                    mp3_path = os.path.join(output_directory, os.path.splitext(filename)[0] + ".mp3")

                    print(f"Converting: {wav_path} -> {mp3_path}")
                    try:
                        audio = AudioSegment.from_wav(wav_path)
                        audio.export(mp3_path, format="mp3", bitrate=bitrate)
                        print(f"Successfully converted: {mp3_path}")
                    except Exception as e:
                        print(f"Error converting {filename}: {e}")


def monitor_usb_and_process(volume_label=None, output_directory="converted_mp3s",
                            bitrate="192k", interval=5, opt=''):
    """
    Monitor for a USB drive, extract WAV files, and convert them to MP3.

    Args:
        volume_label (str): Specific label of the USB drive to detect (optional).
        output_directory (str): Path to save converted MP3 files.
        bitrate (str): Desired bitrate for MP3 files.
        interval (int): Time interval (seconds) to check for USB drives.
    """
    print("Monitoring for USB drives...")
    while True:
        usb_drive = find_usb_drive(volume_label)
        if usb_drive:
            print(f"USB drive detected: {usb_drive}")
            wav_directory = os.path.join(usb_drive, opt.zoom_rootpath)  # Assuming WAV files are stored in a "WAV" folder
            if not os.path.exists(wav_directory):
                print(f"No WAV directory found in {usb_drive}. Skipping...")
                time.sleep(interval)
                continue

            print(f"Processing WAV files in: {wav_directory}")
            convert_wav_to_mp3(wav_directory, output_directory, bitrate)
            print("Processing complete. Waiting for new USB drives...")

        time.sleep(interval)


if __name__ == "__main__":
    # Output directory for MP3 files
    output_dir = r'c:\HanochWorkSPace\zoom_h5'  # Replace with the desired output directory

    parser = argparse.ArgumentParser()

    parser.add_argument('--zoom-rootpath', default='MULTI\FOLDER01', help='save to project/name')


    opt = parser.parse_args()


    # Monitor for any USB drive (set volume_label=None) or specify a volume label
    monitor_usb_and_process(volume_label=None, output_directory=output_dir,
                            bitrate="192k", interval=5, opt=opt)


"""
Key Features in the Updated Script
USB Drive Detection:

The find_usb_drive function uses psutil.disk_partitions() to check for removable drives.
Optionally, you can filter by volume label (e.g., volume_label="ZOOM_H5").
WAV Directory Assumption:

The script assumes WAV files are stored in a WAV folder on the USB drive. You can adjust this path if needed.
Monitoring Loop:

The monitor_usb_and_process function continuously checks for USB drives at regular intervals (interval=5 seconds by default).
Automatic Processing:

Once a USB drive is detected, WAV files are processed and converted to MP3 automatically.
How to Use
Connect Your Zoom Recorder:
Plug in the Zoom H4 or H5 recorder via USB.
Run the Script:
bash
Copy code
python usb_wav_to_mp3_converter.py
Conversion Begins Automatically:
The script will detect the connected USB drive, locate the WAV files, and convert them to MP3 in the specified output directory.
Optional Enhancements
GUI Notification: Add desktop notifications when a USB drive is detected or processing is complete.
Multithreading: Allow concurrent processing of files for faster conversions.
Progress Bar: Use libraries like tqdm to display progress for file conversions.
"""
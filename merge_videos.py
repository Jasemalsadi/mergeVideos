import subprocess

import sys
import os
import multiprocessing
from optparse import OptionParser
import re

print("\nMerge webm  Videos based on Major version X.something.something")
sorted_vids = []


def save_files(major_version, selected_videos, sourcDir, saveDir, extension_=0):
    extension = "." + str(extension_) if extension_ else ""
    if not sourcDir.endswith("/"):
        sourcDir += "/"
    if not saveDir.endswith("/"):
        saveDir += "/"
    videos_to_be_merged_str = ""
    selected_videos_path = []
    i = 0
    for video in selected_videos:
        video_path = sourcDir + video
        selected_videos_path.append(video_path)
        if i == 0:
            videos_to_be_merged_str += add_qoutes(video_path)
        else:
            videos_to_be_merged_str += " + " + add_qoutes(video_path)
        i += 1

    output_file = saveDir + str(major_version) + extension + ".0.webm"
    #print("Before saving file  " + str(major_version) + extension + ".0.webm" "\n")
    command_to_be_executed = " mkvmerge -o " + add_qoutes(
        output_file) + "  -w  " + videos_to_be_merged_str + " --quiet  "
    # --quiet
    output = 0
    sterr = ""
    p = subprocess.Popen([command_to_be_executed], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")

    if not p.returncode:
        print("Saving  " + str(major_version) + extension + ".0.webm" + " Done ! \n ")
        return
    print(
        f"Error in saving the file {major_version}{extension}.0.webm maybe encoding issue, so we need to re-encode it \n")
    video_of_error = (re.findall(rb"('[^']*\.webm')+", output)[-2]).decode("utf-8").replace("'", "")
    # [^']* match anything except ' with zero or more
    # \. escape .
    if video_of_error in selected_videos_path:
        index_of_video_error = selected_videos_path.index(video_of_error)
        first_arr = selected_videos[0:index_of_video_error]
        last_arr = selected_videos[index_of_video_error:]
        if (extension_ >= 1): extension_ -= 1
        save_files(major_version, first_arr, sourcDir, saveDir, extension_=extension_ + 1)
        save_files(major_version, last_arr, sourcDir, saveDir, extension_=extension_ + 2)
        #  merge from 0 to video_of_error-1
    # + merge from video_of_error + 1 to end
    # keep the video of issue as it's to save it


def add_qoutes(str):
    return '"' + str + '"'


def main():
    if (sys.version_info < (3, 0)):
        print("U need to run the code in python 3 ")
        sys.exit()
    if (not is_tool("mkvmerge")):
        print("U need to install mkvmerge on the terminal ")
        sys.exit()
    # parse command line
    parser = OptionParser(usage="usage: %prog [options], version=%prog 1.0")

    parser.add_option("-s", "--source", action="store", type="string", dest="source_videos_path", default=False,
                      help="Path to the Videos folder (without recursively)  ")

    parser.add_option("-d", "--destination", action="store", type="string", dest="destination_video_path",
                      default=False,
                      help="Destination path to save the folder")

    (options, args) = parser.parse_args()
    if len(vars(options)) != 2 or not options.source_videos_path or not options.destination_video_path:
        parser.print_help()
        sys.exit()
    sourcDir = options.source_videos_path.replace("\\", "").strip()
    saveDir = options.destination_video_path.strip()
    # 1. List all embb files there
    # print(os.listdir(sourcDir))
    onlyfiles = []
    try:
        onlyfiles = [f for f in os.listdir(sourcDir) if
                     os.path.isfile(os.path.join(sourcDir, f)) and os.path.join(sourcDir, f).endswith(tuple([
                         ".WEBM", ".webm"
                     ]))]
    except Exception as e:
        print(e)
        exit(1)

    if not len(onlyfiles):
        print("The directory doesn't have any videos!")
        exit(0)
        # print("The .web files :" + "".join(onlyfiles))
        # 2. sort the videos
    onlyfiles.sort(key=lambda val: list(map(int, val.split('.webm')[0].split('.'))))
    # 3. save each major in the saveDir (1.x.x)
    fist_major_version = get_major_version(0, onlyfiles)
    last_major_version = get_major_version(-1, onlyfiles)
    print("Begin Merging Videos")
    processes = []
    for current_major_version in range(fist_major_version, last_major_version + 1):
        # Group version videos
        selected_videos = list(
            filter(lambda v: int(v.split('.webm')[0].split('.')[0]) == current_major_version, onlyfiles))
        # Save them
        p = multiprocessing.Process(name="merge_videos_" + str(current_major_version), target=save_files,
                                    args=[current_major_version, selected_videos, sourcDir, saveDir])

        processes.append(p)
        p.start()

    print("ًWaiting processes to complete saving, it will take time and memory .. ")

    for t1 in processes:
        t1.join()
    print("------------Done !-------------- ")

    for t1 in processes:
        t1.close()


def get_major_version(index, onlyfiles):
    return int(onlyfiles[index].split(".webm")[0].split('.')[0])


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which(name) is not None


main()

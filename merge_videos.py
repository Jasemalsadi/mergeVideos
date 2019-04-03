from moviepy.editor import VideoFileClip, concatenate_videoclips
import sys
import os
import threading

from optparse import OptionParser

print("\nMerge webm  Videos based on Major version X.something.something")
sorted_vids = []


def save_files(major_version, selected_videos, sourcDir, saveDir):
    if not sourcDir.endswith("/"):
        sourcDir += "/"
    if not saveDir.endswith("/"):
        saveDir += "/"
    cmd = ["ffmpeg"]
    clips = []
    for video in selected_videos:
        video_path = sourcDir + video
        clips.append(VideoFileClip(video_path))

    final_clip = concatenate_videoclips(clips)
    output_file = saveDir + str(major_version) + ".0.webm"
    print("Saving " + output_file + "... \n")

    final_clip.write_videofile(output_file, threads=4, logger=None)

    pass


def main():
    # parse command line
    parser = OptionParser(usage="usage: %prog [options], version=%prog 1.0")

    parser.add_option("-s", "--source", action="store", type="string", dest="source_videos_path", default=False,
                      help="Path to the Videos folder (without recursivity)  ")

    parser.add_option("-d", "--destination", action="store", type="string", dest="destination_video_path",
                      default=False,
                      help="Destination path to save the folder")

    (options, args) = parser.parse_args()
    if len(vars(options)) != 2:
        parser.print_help()
        sys.exit()
    sourcDir = options.source_videos_path.replace("\\", "")
    saveDir = options.destination_video_path
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
    threads = []
    for major_version in range(fist_major_version, last_major_version + 1):
        # Group version videos
        selected_videos = list(
            filter(lambda v: int(v.split('.webm')[0].split('.')[0]) == fist_major_version, onlyfiles))
        # Save them
        thread = threading.Thread(target=save_files, args=[major_version, selected_videos, sourcDir, saveDir])
        thread.start()
        threads.append(thread)

    print("ًWaiting threads to complete saving, it will take time .. ")

    for t1 in threads:
        t1.join()
    print("Done ! ")


def get_major_version(index, onlyfiles):
    return int(onlyfiles[index].split(".webm")[0].split('.')[0])


main()

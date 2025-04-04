import argparse
import cv2
import os
import sys
import shutil

'''
coomand line tool to dump all frames from a video into a directory
'''

def main():

    #handle argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_video", type=str, default=None, help = 'path to video', required = True)
    parser.add_argument("-o", "--output_dir", type=str, default=None, help = 'output path', required = True)

    args = parser.parse_args()

    #check that directory does not exist
    if os.path.isdir(args.output_dir):
        response = input('Should current directory be deleted? y/n:  ')
        if response.lower() not in ['y', 'n'] or response.lower() == 'n':
            sys.exit()
        else:
            shutil.rmtree(args.output_dir)
    
    os.makedirs(args.output_dir)

    video_capture = cv2.VideoCapture(args.input_video)
    if not video_capture.isOpened():
        raise Exception(f"Could not open video file: {args.input_video}")

    fnum = 0
    while True:
        
        ret, frame = video_capture.read()
        if not ret:
            break  # End of video
        
        image_name = os.path.join(args.output_dir, f'fram_{fnum}.png')
        print('saving frame: ', image_name)
        cv2.imwrite(image_name, frame)
        fnum += 1

if __name__ == '__main__':
    main()



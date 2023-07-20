import os
import cv2
import argparse
import natsort

def parse_args():
    parser = argparse.ArgumentParser(description='Extract data from rosbags.')
    parser.add_argument('--dir', '-d', type=str, required=True, 
                        help='Path to the input directory.')
    
    parser.add_argument('--video', '-v', type=str, required=True,  
                        help='Path to the video file to be saved.')
    
    parser.add_argument('--fps', '-f', type=int, default=30, 
                        help='Framerate of the output video. Defaults to 30.')
    
    parser.add_argument('--sync', '-s', action='store_true',  
                        help='If specified, the program will use the file timstamps to try to synchronize video')

    args = parser.parse_args()

    return args

def main(video_file, input_dir):
    # Get a list of all the JPEG images in the directory
    image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.jpg')]
    image_files = natsort.natsorted(image_files,reverse=False) # Sort the image files by their timestamp
    
    # Calculate the time delta between each frame
    frame_times = [int(os.path.splitext(os.path.basename(f))[0]) / 1e9 for f in image_files]
    frame_deltas = [t - frame_times[i-1] if i > 0 else 0 for i, t in enumerate(frame_times)]
    
    
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_size = cv2.imread(image_files[0]).shape[:2][::-1]
    
    video_frame_delta = 1/args.fps

    out = cv2.VideoWriter(video_file, fourcc, args.fps, frame_size)
    
    frame_index = 0
    
    print("Writing video")
    
    for image_file, delta in zip(image_files, frame_deltas):
 
        if args.sync:
            frame_count = int(delta // video_frame_delta)
        else:
            frame_count = 1
        
        # Write the frame for appropriate amount of times to keep the framerate
        for _ in range(frame_count):
            out.write(cv2.imread(image_file))
            
                
        # add current frame to video writer
        frame_index += 1
        print(f"Frame {frame_index} / {len(image_files)}", end='\r')

    # Release the video writer
    out.release()
    print()
        
if __name__ == '__main__':
    
    args = parse_args()
    
    input_dir = os.path.abspath(os.path.expanduser(args.dir))
    video_file = os.path.abspath(os.path.expanduser(args.video))

    if not os.path.exists(input_dir):
        print(f"Input directory does not exist.")
        exit()

    main(video_file, input_dir)

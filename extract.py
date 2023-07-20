import os
import cv2
import shutil
import argparse
import numpy as np

from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr

def parse_args():
    parser = argparse.ArgumentParser(description='Extract data from rosbags.')
    parser.add_argument('--rosbag', '-r', type=str, required=True,  help='Path to the rosbag file.')
    parser.add_argument('--dir', '-d', type=str, required=True, help='Path to the output directory.')
    parser.add_argument('--uncompressed', '-u', action='store_true', help='Extract uncompressed images.')

    args = parser.parse_args()

    return args

def main(rosbag_file, output_dir):
    
    # Create reader instance and open for reading
    with Reader(rosbag_file) as reader:
        
        if args.uncompressed:
            msgtype = 'sensor_msgs/msg/Image'
        else:
            msgtype = 'sensor_msgs/msg/CompressedImage'
        
        # Topic and msgtype information is available on .connections list
        for i, connection in enumerate(reader.connections):
            print(connection.topic, connection.msgtype)

            if connection.msgtype == msgtype:
                new_name = connection.topic.replace('/', '_')
                subfolder = os.path.join(output_dir, new_name)
                os.makedirs(subfolder)
                
                msg_count = reader.metadata['topics_with_message_count'][i]['message_count']
                
                counter = 0
                
                for conn, timestamp, rawdata in reader.messages(connections=[connection,]):
                    msg = deserialize_cdr(rawdata, conn.msgtype)
                    # Read image data
                    frame = np.frombuffer(msg.data, dtype=np.uint8)
                    
                    if msgtype == 'sensor_msgs/msg/Image':
                        # Uncompressed image
                        frame = frame.reshape((msg.height, msg.width, 3))
                    
                    filename = str(timestamp) + '.jpg'
                    file_path = os.path.join(subfolder, filename)
                    
                    if args.uncompressed:
                        cv2.imwrite(file_path, frame)
                    else:
                        # Compressed image
                        with open(file_path, 'wb') as f:
                            f.write(frame)    
                    
                    counter += 1
                    print(f"Extracting {counter} / {msg_count}", end='\r')
        
if __name__ == '__main__':
    
    args = parse_args()
    
    rosbag_file = os.path.abspath(os.path.expanduser(args.rosbag))
    output_dir = os.path.abspath(os.path.expanduser(args.dir))

    if os.path.exists(output_dir):
        print(f"Output directory already exists. Removing '{output_dir}' and creating a new one.")
        try:
            shutil.rmtree(output_dir)
        except OSError as e:
            print(f"Error removing directory '{output_dir}': {e}")
            exit(1)

    try:
        os.makedirs(output_dir)
    except OSError as e:
        print(f"Error creating directory '{output_dir}': {e}")
        exit(1)
        
        
    main(rosbag_file, output_dir)

import cv2


def count_frames(video_path):
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    video.release()
    return total_frames


def cut_video(video_path, start_frame, end_frame, output_path):
    video = cv2.VideoCapture(video_path)
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)

   
    output_video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    frame_count = 0

    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            break

        if frame_count >= start_frame and frame_count <= end_frame:
            # Write the frame to the output video
            output_video.write(frame)

        if frame_count > end_frame:
            break

        frame_count += 1

    video.release()
    output_video.release()

    return


def process_frames(video_path):
    video = cv2.VideoCapture(video_path)
    frame_count = 0

    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            break

        # Perform any desired processing on the frame here
        # For example, you can display the frame or perform some analysis

        # Increment the frame count
        frame_count += 1

        # Display the frame
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

    return frame_count


def extract_images(video_path, start_frame, end_frame, output_folder):
    video = cv2.VideoCapture(video_path)
    frame_count = 0

    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            break

        if frame_count >= start_frame and frame_count <= end_frame:
            # Save the frame as a PNG image
            output_path = f"{output_folder}/frame_{frame_count}.png"
            cv2.imwrite(output_path, frame)

        if frame_count > end_frame:
            break

        frame_count += 1

    video.release()

    return

#
# # Example usage
# mkv_video_path = 'E:\\EXP-20-APR-2023\\PP12\\recordings_pp12\\214191945255252_1.mkv'
# mp4_video_path = 'E:\\EXP-20-APR-2023\\PP12\\recordings_pp12\\939570349352546_0.mp4'
#
# # Count frames in the MKV video
# mkv_frame_count = count_frames(mkv_video_path)
# print("MKV video frame count:", mkv_frame_count)
# mp4_frame_count = count_frames(mp4_video_path)
# print("MKV video frame count:", mp4_frame_count)
# #
# cut_video(video_path=mp4_video_path, start_frame=10, end_frame=1900,
#            output_path='D:\\Thesis\\data\\videos\\PP6\\P1\\new_mp.mp4')
# extract_images(video_path=mp4_video_path, start_frame=10, end_frame=1900,
#                output_folder='D:\\Thesis\\data\\videos\\PP6\\P1\\img')
#
# # Process and iterate through frames in the MP4 video
# mp4_frame_count = process_frames(mp4_video_path)
# print("MP4 video frame count:", mp4_frame_count)


# dir_in = 'G:\\PP2\\recordings_PP2\\'


dir_out = 'G:\\lefs_cut_vids\\'
cut_name = 'pp02_stress.mkv'

# img_dir_out = 'G:\\lefs_cut_vids\\pp02_neutral_img'
img_dir_out = dir_out + cut_name[:-4] + '_img'
mkv_video_path = 'G:\\PP2\\recordings_PP2\\1681199666_0.mkv'
# Count frames in the MKV video
mkv_frame_count = count_frames(mkv_video_path)
print("MKV video frame count:", mkv_frame_count)

#45mins for 30min (ish) video to be cut n saved
cut_video(video_path= mkv_video_path, start_frame=166007, end_frame=220007,
            output_path= dir_out + cut_name)

# extract_images(video_path=mkv_video_path, start_frame=62639, end_frame=116639,
#                 output_folder=img_dir_out)

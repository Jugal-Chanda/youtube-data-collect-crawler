import webbrowser

# Read the video IDs from the source file
with open("video_ids.txt", "r") as f:
    video_ids = f.read().splitlines()

# Load the existing approved and rejected video IDs
with open("approved_video_ids.txt", "r") as f:
    approved_video_ids = set(f.read().splitlines())

with open("rejected_video_ids.txt", "r") as f:
    rejected_video_ids = set(f.read().splitlines())

# Remove the approved and rejected video IDs from the source list
video_ids = [id for id in video_ids if id not in approved_video_ids and id not in rejected_video_ids]

# Set the batch size
batch_size = 100

# Play the videos and prompt for approval in batches
for i in range(0, len(video_ids), batch_size):
    batch_video_ids = video_ids[i:i+batch_size]

    # Play the first two videos in the batch
    for video_id in batch_video_ids:
        # Construct the video URL and open it in the default web browser
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        webbrowser.open(video_url)

    # Prompt the user for approval or rejection
   
        while True:
            decision = input("Approve (a), reject (r), or skip (s) this video: ")
            if decision == "a":
                approved_video_ids.add(video_id)
                video_ids.remove(video_id) 
                with open("video_ids.txt", "w") as f:
                    f.write("\n".join(video_ids))
                # Write the approved and rejected video IDs to separate files
                with open("approved_video_ids.txt", "w") as f:
                    f.write("\n".join(approved_video_ids))
                break
            elif decision == "r":
                rejected_video_ids.add(video_id)
                video_ids.remove(video_id) 
                with open("video_ids.txt", "w") as f:
                    f.write("\n".join(video_ids))
                # Write the approved and rejected video IDs to separate files
                with open("rejected_video_ids.txt", "w") as f:
                    f.write("\n".join(rejected_video_ids))
                break
            elif decision == "s":
                break
            else:
                print("Invalid input. Please enter 'a', 'r', or 's'.")

    # Prompt the user to continue to the next batch or quit the program
    if i + batch_size < len(video_ids):
        next_batch = input("Continue to the next batch (y/n)? ")
        if next_batch.lower() != "y":
            break

# Write the updated video IDs back to the source file


print("Processing complete.")

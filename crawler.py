import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Set up the YouTube API client
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret_970828352629-5ib4l9c39pea636m7158msv73s1jgho7.apps.googleusercontent.com.json"

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
flow.redirect_uri = f"http://localhost:49303/callback"
credentials = flow.run_local_server(port=49303)
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)


# Set up the search request parameters
search_query = "ring camera video of a car break-in"
max_results = 50
next_page_token = ""
videos = set()
page_ids = []
new_videos = set()
with open("video_ids.txt") as f:
    lines = f.readlines()
    videos = set(lines)

videos = {x.strip() for x in videos}


while len(videos) < 2000:
    # Call the YouTube API with the search request parameters
    search_response = youtube.search().list(
        q=search_query,
        type="video",
        pageToken=next_page_token,
        order="relevance",
        part="id",
        maxResults=max_results
    ).execute()

    # Check that all video IDs in the response are unique
    new_video_ids = {search_result["id"]["videoId"]
                     for search_result in search_response.get("items", [])}
    for x in new_video_ids:
        if x not in videos:
            new_videos.add(x)
    videos.update(new_video_ids)

    # with open("video_ids.txt", "w") as f:
    #     f.write("\n".join(videos))

    next_page_token = search_response.get("nextPageToken", "")
    page_ids.append(next_page_token)
    with open("page_ids.txt", "w") as f:
        f.write("\n".join(page_ids))
    if next_page_token != "":
        with open("next_page_token.txt", "w") as f:
            f.write(next_page_token)

    # Exit the loop if there are no more pages to fetch
    if not next_page_token:
        print(search_response.get("prevPageToken", ""))
        print("no page token")
        break


new_file_name = search_query.split(" ")
new_file_name = "_".join(new_file_name)+".txt"

with open(new_file_name, "w") as f:
    f.write("\n".join(new_videos))

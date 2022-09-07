from pytube import YouTube

if __name__ == "__main__":
    path_video="/home/francesco/Desktop/UniPd/thesis/master_project/videos/"
    videolist=open("/home/francesco/Desktop/UniPd/thesis/master_project/videolists/sports_video.txt","r")
    videos_url=videolist.read().splitlines()
    for video_url in videos_url:
        print("[i] Downloading: "+video_url+" ...")
        try:
            YouTube(video_url).streams.first().download(path_video)
        except Exception as e:
            print("[-] Error downloading:",e)

    videolist.close()
    #YouTube('video_url').streams.first().download('path_video')

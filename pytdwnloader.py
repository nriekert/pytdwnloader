import yt_dlp
import os

def download_video(url, output_path='downloads', quality='best'):
    
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',  # Single file format
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': False,
        'no_warnings': False,
    }
    
    if quality == 'worst':
        ydl_opts['format'] = 'worst[ext=mp4]/worst'
    elif quality == '720p':
        ydl_opts['format'] = 'best[height<=720][ext=mp4]/best[height<=720]'
    elif quality == '1080p':
        ydl_opts['format'] = 'best[height<=1080][ext=mp4]/best[height<=1080]'
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from: {url}")
            info = ydl.extract_info(url, download=True)
            print(f"\nDownload complete!")
            print(f"Title: {info.get('title', 'Unknown')}")
            print(f"Duration: {info.get('duration', 0)} seconds")
            print(f"Saved to: {output_path}")
            
    except Exception as e:
        print(f"Error downloading video: {str(e)}")

def download_audio_only(url, output_path='downloads'):

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading audio from: {url}")
            info = ydl.extract_info(url, download=True)
            print(f"\nDownload complete!")
            print(f"Title: {info.get('title', 'Unknown')}")
            print(f"Saved to: {output_path}")
            
    except Exception as e:
        print(f"Error downloading audio: {str(e)}")

def get_video_info(url):

    ydl_opts = {'quiet': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            print(f"Title: {info.get('title', 'N/A')}")
            print(f"Duration: {info.get('duration', 0)} seconds")
            print(f"Views: {info.get('view_count', 'N/A')}")
            print(f"Uploader: {info.get('uploader', 'N/A')}")
            print(f"Upload Date: {info.get('upload_date', 'N/A')}")
            
            print("\nAvailable formats:")
            for fmt in info.get('formats', [])[:5]:  # Show first 5 formats
                print(f"  - {fmt.get('format_note', 'N/A')} ({fmt.get('ext', 'N/A')})")
                
    except Exception as e:
        print(f"Error getting video info: {str(e)}")


if __name__ == "__main__":
    print("YouTube Video Downloader")
    print("=" * 50)
    
    while True:
        video_url = input("\nEnter YouTube URL (or 'q' to quit): ").strip()
        
        if video_url.lower() == 'q':
            print("Goodbye!")
            break
        
        if not video_url:
            print("Please enter a valid URL!")
            continue
        
        print("\nOptions:")
        print("1. Download video (best quality)")
        print("2. Download video (720p)")
        print("3. Download audio only (MP3)")
        print("4. Get video info only")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            download_video(video_url, quality='best')
        elif choice == '2':
            download_video(video_url, quality='720p')
        elif choice == '3':
            download_audio_only(video_url)
        elif choice == '4':
            get_video_info(video_url)
        else:
            print("Invalid choice!")
        
        print("\n" + "=" * 50)
    
    input("\nPress Enter to exit...")

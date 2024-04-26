from tqdm import tqdm
from stqdm import stqdm
import argparse
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError
from pathlib import Path


class YouTubeDownloader:

    def __init__(self, url, file_extension='mp4', output_path=Path.cwd(), quality='highest'):
        self.url = url
        self.file_extension = file_extension
        self.output_path = output_path
        self.quality = quality
        self.pbar = None
        self.yt = YouTube(self.url, 
                          on_progress_callback=self.on_progress, 
                          on_complete_callback=self.on_complete)
    def ExtRes(self):

        stream = self.yt.streams.filter(progressive=True)
        ext = ['Please select an option']
        res = ['Please select an option']
        for i in range(len(stream)):
            if stream[i].mime_type.split('/')[1] not in ext:
                ext.append(stream[i].mime_type.split('/')[1])
            if stream[i].resolution not in res:
                res.append(stream[i].resolution)
        return ext, res

    def Download(self):
        try:
            self.yt.check_availability()
        except VideoUnavailable:
            print('Video is Unavailable!')
            return
        
        if self.quality.lower() == 'highest':
            stream = self.yt.streams.filter(progressive=True,
                                            file_extension=self.file_extension,
                                            ).get_highest_resolution()
        else:
            stream = self.yt.streams.filter(progressive=True,
                                            file_extension=self.file_extension,
                                            res=self.quality).first()
        try:
            #self.pbar = tqdm(desc=self.yt.title, total=stream.filesize, unit='B', unit_scale=True) # for terminal
            self.pbar = stqdm(desc=self.yt.title, total=stream.filesize, unit='B', unit_scale=True, frontend=True) # for streamlit
            stream.download(self.output_path)

        except AttributeError:
            print('The video with your file_extension and quality is not exist')
            return
    
    def on_progress(self, stream, chunk, bytes_remaining):
        """
        Updates the progress bar during the download.

        :param stream: Stream being downloaded.
        :param chunk: Chunk of data being downloaded.
        :param bytes_remaining: Number of bytes remaining to be downloaded.
        """
        current = stream.filesize - bytes_remaining
        self.pbar.update(current - self.pbar.n)  # update pbar with the downloaded bytes

    def on_complete(self, stream, file_path):
        """
        Completes the progress bar and prints the download completion message.

        :param stream: Stream that has been downloaded.
        :param file_path: The file path of the downloaded video.
        """
        self.pbar.close()
        print(f"\nDownloaded {self.yt.title} successfully to: {file_path}")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Download a YouTube video at a specified quality and output path.')
    parser.add_argument('url', help='The YouTube URL to download')
    parser.add_argument('-q', '--quality', help='The desired video quality (e.g., 720p, 1080p, highest)',
                        default='highest', type=str)
    parser.add_argument('-o', '--output_path', help='The output directory to save the video',
                        default=Path.cwd(), type=str)
    parser.add_argument('-f', '--file_extension', help='The file extension to download the video',
                        default='mp4', type=str)
    
    args = parser.parse_args()

    try:
        downloader = YouTubeDownloader(url=args.url, 
                                       file_extension=args.file_extension, 
                                       output_path=args.output_path, 
                                       quality=args.quality)
        downloader.Download()

    except RegexMatchError:
        print(f'could not find match for {args.url}')


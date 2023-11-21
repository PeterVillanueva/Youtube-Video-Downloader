import customtkinter
import customtkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
import threading


class YouTubeDownloaderApp:
	def __init__(self, root):
		self.root = root
		self.root.geometry("720x480")
		self.root.title("YouTube Video Downloader")

		self.video_link_label = tk.CTkLabel(root, text="Enter YouTube Video URL:")
		self.video_link_label.pack(padx=10, pady=10)

		self.video_link_entry = tk.CTkEntry(root, width=350, height=40)
		self.video_link_entry.pack(pady=5)

		self.button_frame = tk.CTkFrame(root, width=350, height=40)
		self.button_frame.pack()

		self.download_button = tk.CTkButton(self.button_frame, text="Download Video", command=self.download_video)
		self.download_button.pack(side=tk.LEFT, padx=17.5, pady=15)

		self.download_mp3_button = tk.CTkButton(self.button_frame, text="Download MP3", command=self.download_audio)
		self.download_mp3_button.pack(side=tk.RIGHT, padx=17, pady=15)

		self.progress = ttk.Progressbar(root, length=460, mode="determinate")
		self.progress.pack(padx=10, pady=10)

		self.download_status_label = tk.CTkLabel(root, text="")
		self.download_status_label.pack(pady=10)

		self.reset_button = tk.CTkButton(root, width=200, height=30, text="Download Another Video", state="disabled", command=self.reset)
		self.reset_button.pack(padx=10, pady=10)

		self.video_title_label = tk.CTkLabel(root, text="")
		self.video_title_label.pack(pady=10)

		self.audio_title_label = tk.CTkLabel(root, text="")
		self.audio_title_label.pack(pady=10)

		self.video = None
		self.audio = None
		self.video_stream = None
		self.audio_stream = None

	def download_video(self):
		video_url = self.video_link_entry.get()
		if video_url:
			self.download_button.configure(state=tk.DISABLED)
			try:
				self.download_status_label.configure(text="Downloading...")
				self.progress["value"] = 0
				self.video = YouTube(video_url, on_progress_callback=self.update_progress)
				self.video_stream = self.video.streams.get_highest_resolution()
				self.video_title_label.configure(text="Video Title: " + self.video.title)
				self.download_thread = threading.Thread(target=self.download_thread_function)
				self.download_thread.start()
			except Exception as e:
				self.download_status_label.configure(text="Error: " + str(e))
		else:
			messagebox.showerror("Error", "Please enter a valid YouTube video URL")

	def download_audio(self):
		video_url = self.video_link_entry.get()
		if video_url:
			self.download_mp3_button.configure(state=tk.DISABLED)
			try:
				self.download_status_label.configure(text="Converting to MP3...")
				self.progress["value"] = 0
				self.audio = YouTube(video_url, on_progress_callback=self.update_progress).streams.filter(
					only_audio=True).first()
				self.audio_stream = self.audio
				self.audio_title_label.configure(text="Audio Title: " + self.audio.title)
				self.download_audio_thread = threading.Thread(target=self.download_audio_thread_function)
				self.download_audio_thread.start()
			except Exception as e:
				self.download_status_label.configure(text="Error: " + str(e))
		else:
			messagebox.showerror("Error", "Please enter a valid YouTube video URL")

	def download_thread_function(self):
		try:
			self.video_stream.download("downloads/")
			self.download_status_label.configure(text="Video Downloaded!")
			self.reset_button.configure(state="normal")
		except Exception as e:
			self.download_status_label.configure(text="Error: " + str(e))

	def download_audio_thread_function(self):
		try:
			self.audio_stream.download("downloads/")
			self.download_status_label.configure(text="MP3 Downloaded!")
			self.reset_button.configure(state="normal")
		except Exception as e:
			self.download_status_label.configure(text="Error: " + str(e))

	def update_progress(self, stream, chunk, bytes_remaining):
		total_size = stream.filesize if stream else 0
		bytes_downloaded = total_size - bytes_remaining
		download_percentage = (bytes_downloaded / total_size) * 100 if total_size > 0 else 0
		self.progress["value"] = download_percentage
		self.progress.update()

	def reset(self):
		self.download_button.configure(state="normal")
		self.download_mp3_button.configure(state="normal")
		self.video_link_entry.delete(0, tk.END)
		self.progress["value"] = 0
		self.download_status_label.configure(text="")
		self.reset_button.configure(state="disabled")
		self.video_title_label.configure(text="")
		self.audio_title_label.configure(text="")


if __name__ == "__main__":
	root = customtkinter.CTk()
	app = YouTubeDownloaderApp(root)
	root.mainloop()

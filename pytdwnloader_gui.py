import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import sys
import os

# Import functions from cli version
from pytdwnloader import download_video, download_audio_only, get_video_info

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("pytdwnloader")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Variables
        self.url_var = tk.StringVar()
        self.output_path_var = tk.StringVar(value=os.path.join(os.getcwd(), "downloads"))
        self.quality_var = tk.StringVar(value="Best")
        self.download_type_var = tk.StringVar(value="video")
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure column weights for proper alignment
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="pytdwnloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # URL input
        url_label = ttk.Label(main_frame, text="YouTube URL:")
        url_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=45)
        url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Output path
        output_label = ttk.Label(main_frame, text="Output Folder:")
        output_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path_var, width=45)
        output_entry.pack(side=tk.LEFT)
        
        browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_folder)
        browse_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Download type
        type_label = ttk.Label(main_frame, text="Download Type:")
        type_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(5, 0))
        
        video_radio = ttk.Radiobutton(type_frame, text="Video", 
                                      variable=self.download_type_var, 
                                      value="video", command=self.update_quality_options)
        video_radio.pack(side=tk.LEFT)
        
        audio_radio = ttk.Radiobutton(type_frame, text="Audio Only (MP3)", 
                                     variable=self.download_type_var, 
                                     value="audio", command=self.update_quality_options)
        audio_radio.pack(side=tk.LEFT, padx=(20, 0))
        
        # Quality selection
        quality_label = ttk.Label(main_frame, text="Quality:")
        quality_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.quality_combo = ttk.Combobox(main_frame, textvariable=self.quality_var, 
                                         state="readonly", width=45)
        self.quality_combo['values'] = ("Best", "1080p", "720p", "Worst")
        self.quality_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        self.quality_combo.current(0)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        info_btn = ttk.Button(button_frame, text="Get Video Info", 
                             command=self.get_info_threaded)
        info_btn.pack(side=tk.LEFT, padx=5)
        
        download_btn = ttk.Button(button_frame, text="Download", 
                                 command=self.download_threaded)
        download_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_output)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready")
        progress_label = ttk.Label(main_frame, text="Status:")
        progress_label.grid(row=6, column=0, sticky=tk.W, pady=5)
        
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate', length=400)
        self.progress_bar.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        self.status_label = ttk.Label(main_frame, textvariable=self.progress_var, 
                                     foreground="gray")
        self.status_label.grid(row=7, column=0, columnspan=2, pady=(5, 10))
        
        # Output text area
        output_label = ttk.Label(main_frame, text="Output:")
        output_label.grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        self.output_text = scrolledtext.ScrolledText(main_frame, height=12, width=80, 
                                                     wrap=tk.WORD, state=tk.DISABLED)
        self.output_text.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Redirect print to output text
        self.original_print = print
        sys.stdout = self
        
    def update_quality_options(self):
        if self.download_type_var.get() == "audio":
            self.quality_combo['values'] = ()
            self.quality_var.set("")
            self.quality_combo.config(state="disabled")
        else:
            self.quality_combo['values'] = ("Best", "1080p", "720p", "Worst")
            self.quality_combo.config(state="readonly")
            self.quality_var.set("Best")
            self.quality_combo.current(0)
    
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_path_var.get())
        if folder:
            self.output_path_var.set(folder)
    
    def write(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def flush(self):
        pass
    
    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def get_info_threaded(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL!")
            return
        
        self.progress_bar.start()
        self.progress_var.set("Getting video information...")
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"Fetching info for: {url}\n")
        self.output_text.insert(tk.END, "-" * 50 + "\n")
        self.output_text.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.get_info, args=(url,), daemon=True)
        thread.start()
    
    def get_info(self, url):
        try:
            get_video_info(url)
            self.root.after(0, self.info_complete)
        except Exception as e:
            self.root.after(0, lambda: self.download_error(str(e)))
    
    def info_complete(self):
        self.progress_bar.stop()
        self.progress_var.set("Information retrieved successfully")
    
    def download_threaded(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL!")
            return
        
        output_path = self.output_path_var.get().strip()
        if not output_path:
            messagebox.showerror("Error", "Please specify an output folder!")
            return
        
        download_type = self.download_type_var.get()
        
        self.progress_bar.start()
        self.progress_var.set("Downloading...")
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"Starting download: {url}\n")
        self.output_text.insert(tk.END, "-" * 50 + "\n")
        self.output_text.config(state=tk.DISABLED)
        
        if download_type == "audio":
            thread = threading.Thread(target=self.download_audio, args=(url, output_path), daemon=True)
        else:
            quality = self.quality_var.get().lower()
            thread = threading.Thread(target=self.download_vid, args=(url, output_path, quality), daemon=True)
        
        thread.start()
    
    def download_vid(self, url, output_path, quality):
        try:
            download_video(url, output_path, quality)
            self.root.after(0, self.download_complete)
        except Exception as e:
            self.root.after(0, lambda: self.download_error(str(e)))
    
    def download_audio(self, url, output_path):
        try:
            download_audio_only(url, output_path)
            self.root.after(0, self.download_complete)
        except Exception as e:
            self.root.after(0, lambda: self.download_error(str(e)))
    
    def download_complete(self):
        self.progress_bar.stop()
        self.progress_var.set("Download complete!")
        messagebox.showinfo("Success", "Download completed successfully!")
    
    def download_error(self, error_msg):
        self.progress_bar.stop()
        self.progress_var.set("Error occurred")
        messagebox.showerror("Error", f"An error occurred:\n{error_msg}")
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, f"ERROR: {error_msg}\n")
        self.output_text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()

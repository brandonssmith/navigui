import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import toml
import os
import sys
from pathlib import Path

class NavidromeConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Navidrome Configuration GUI")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Configuration data
        self.config = {}
        self.config_file = "navidrome.toml"
        
        # Create main frame with scrollbar
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Title
        title_label = ttk.Label(scrollable_frame, text="Navidrome Configuration", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Load existing config
        self.load_config()
        
        # Create configuration sections
        self.create_general_section(scrollable_frame)
        self.create_paths_section(scrollable_frame)
        self.create_scanning_section(scrollable_frame)
        self.create_transcoding_section(scrollable_frame)
        self.create_web_interface_section(scrollable_frame)
        self.create_security_section(scrollable_frame)
        self.create_advanced_section(scrollable_frame)
        
        # Buttons
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=20, fill=tk.X)
        
        ttk.Button(button_frame, text="Save Configuration", 
                  command=self.save_config).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Load Configuration", 
                  command=self.load_config_file).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Reset to Defaults", 
                  command=self.reset_to_defaults).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="View Raw TOML", 
                  command=self.view_raw_toml).pack(side=tk.LEFT)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel
        canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        canvas = event.widget.master.master
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def create_section_frame(self, parent, title):
        """Create a titled section frame"""
        section_frame = ttk.LabelFrame(parent, text=title, padding="10")
        section_frame.pack(fill=tk.X, pady=(0, 15))
        return section_frame
    
    def create_general_section(self, parent):
        """General configuration options"""
        section = self.create_section_frame(parent, "General Settings")
        
        # Log Level
        ttk.Label(section, text="Log Level:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.log_level_var = tk.StringVar(value=self.config.get('LogLevel', 'INFO'))
        log_level_combo = ttk.Combobox(section, textvariable=self.log_level_var, 
                                       values=['DEBUG', 'INFO', 'WARN', 'ERROR'], 
                                       state="readonly", width=15)
        log_level_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Port
        ttk.Label(section, text="Port:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.port_var = tk.StringVar(value=str(self.config.get('Port', 4533)))
        ttk.Entry(section, textvariable=self.port_var, width=15).grid(row=1, column=1, 
                                                                     sticky=tk.W, padx=(10, 0), pady=5)
        
        # Address
        ttk.Label(section, text="Address:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.address_var = tk.StringVar(value=self.config.get('Address', '0.0.0.0'))
        ttk.Entry(section, textvariable=self.address_var, width=20).grid(row=2, column=1, 
                                                                       sticky=tk.W, padx=(10, 0), pady=5)
        
        # Data Folder
        ttk.Label(section, text="Data Folder:").grid(row=3, column=0, sticky=tk.W, pady=5)
        data_frame = ttk.Frame(section)
        data_frame.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        self.data_folder_var = tk.StringVar(value=self.config.get('DataFolder', './data'))
        ttk.Entry(data_frame, textvariable=self.data_folder_var, width=30).pack(side=tk.LEFT)
        ttk.Button(data_frame, text="Browse", 
                  command=lambda: self.browse_folder(self.data_folder_var)).pack(side=tk.LEFT, padx=(5, 0))
    
    def create_paths_section(self, parent):
        """Music and media paths"""
        section = self.create_section_frame(parent, "Music & Media Paths")
        
        # Music Folder
        ttk.Label(section, text="Music Folder:").grid(row=0, column=0, sticky=tk.W, pady=5)
        music_frame = ttk.Frame(section)
        music_frame.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        self.music_folder_var = tk.StringVar(value=self.config.get('MusicFolder', ''))
        ttk.Entry(music_frame, textvariable=self.music_folder_var, width=40).pack(side=tk.LEFT)
        ttk.Button(music_frame, text="Browse", 
                  command=lambda: self.browse_folder(self.music_folder_var)).pack(side=tk.LEFT, padx=(5, 0))
        
        # FFmpeg Path
        ttk.Label(section, text="FFmpeg Path:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ffmpeg_frame = ttk.Frame(section)
        ffmpeg_frame.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        self.ffmpeg_path_var = tk.StringVar(value=self.config.get('FFmpegPath', ''))
        ttk.Entry(ffmpeg_frame, textvariable=self.ffmpeg_path_var, width=40).pack(side=tk.LEFT)
        ttk.Button(ffmpeg_frame, text="Browse", 
                  command=lambda: self.browse_file(self.ffmpeg_path_var, [("Executable", "*.exe"), ("All files", "*.*")])).pack(side=tk.LEFT, padx=(5, 0))
    
    def create_scanning_section(self, parent):
        """Library scanning options"""
        section = self.create_section_frame(parent, "Library Scanning")
        
        # Scan Schedule
        ttk.Label(section, text="Scan Schedule:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.scan_schedule_var = tk.StringVar(value=self.config.get('ScanSchedule', '@every 24h'))
        scan_combo = ttk.Combobox(section, textvariable=self.scan_schedule_var, 
                                  values=['@every 1h', '@every 6h', '@every 12h', '@every 24h', 
                                         '@every 48h', '@weekly', '@monthly', 'manual'], 
                                  state="readonly", width=20)
        scan_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Auto Scan
        self.auto_scan_var = tk.BooleanVar(value=self.config.get('AutoScan', True))
        ttk.Checkbutton(section, text="Auto Scan", variable=self.auto_scan_var).grid(row=1, column=0, 
                                                                                   columnspan=2, sticky=tk.W, pady=5)
        
        # Scan at Startup
        self.scan_at_startup_var = tk.BooleanVar(value=self.config.get('ScanAtStartup', True))
        ttk.Checkbutton(section, text="Scan at Startup", variable=self.scan_at_startup_var).grid(row=2, column=0, 
                                                                                               columnspan=2, sticky=tk.W, pady=5)
    
    def create_transcoding_section(self, parent):
        """Audio transcoding options"""
        section = self.create_section_frame(parent, "Audio Transcoding")
        
        # Transcoding Cache Size
        ttk.Label(section, text="Cache Size:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cache_size_var = tk.StringVar(value=self.config.get('TranscodingCacheSize', '150MiB'))
        cache_combo = ttk.Combobox(section, textvariable=self.cache_size_var, 
                                   values=['50MiB', '100MiB', '150MiB', '200MiB', '500MiB', '1GiB'], 
                                   state="readonly", width=15)
        cache_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Enable Transcoding
        self.enable_transcoding_var = tk.BooleanVar(value=self.config.get('EnableTranscoding', True))
        ttk.Checkbutton(section, text="Enable Transcoding", variable=self.enable_transcoding_var).grid(row=1, column=0, 
                                                                                                     columnspan=2, sticky=tk.W, pady=5)
        
        # Transcoding Format
        ttk.Label(section, text="Default Format:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.transcode_format_var = tk.StringVar(value=self.config.get('TranscodingFormat', 'mp3'))
        format_combo = ttk.Combobox(section, textvariable=self.transcode_format_var, 
                                    values=['mp3', 'aac', 'ogg', 'opus'], 
                                    state="readonly", width=15)
        format_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    def create_web_interface_section(self, parent):
        """Web interface options"""
        section = self.create_section_frame(parent, "Web Interface")
        
        # Enable Web Interface
        self.enable_web_var = tk.BooleanVar(value=self.config.get('EnableWebInterface', True))
        ttk.Checkbutton(section, text="Enable Web Interface", variable=self.enable_web_var).grid(row=0, column=0, 
                                                                                               columnspan=2, sticky=tk.W, pady=5)
        
        # Theme
        ttk.Label(section, text="Theme:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.theme_var = tk.StringVar(value=self.config.get('Theme', 'default'))
        theme_combo = ttk.Combobox(section, textvariable=self.theme_var, 
                                   values=['default', 'dark', 'light'], 
                                   state="readonly", width=15)
        theme_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Enable Downloads
        self.enable_downloads_var = tk.BooleanVar(value=self.config.get('EnableDownloads', True))
        ttk.Checkbutton(section, text="Enable Downloads", variable=self.enable_downloads_var).grid(row=2, column=0, 
                                                                                                 columnspan=2, sticky=tk.W, pady=5)
    
    def create_security_section(self, parent):
        """Security and authentication options"""
        section = self.create_section_frame(parent, "Security & Authentication")
        
        # Enable Authentication
        self.enable_auth_var = tk.BooleanVar(value=self.config.get('EnableAuthentication', True))
        ttk.Checkbutton(section, text="Enable Authentication", variable=self.enable_auth_var).grid(row=0, column=0, 
                                                                                                 columnspan=2, sticky=tk.W, pady=5)
        
        # Session Timeout
        ttk.Label(section, text="Session Timeout (hours):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.session_timeout_var = tk.StringVar(value=str(self.config.get('SessionTimeout', 24)))
        ttk.Entry(section, textvariable=self.session_timeout_var, width=15).grid(row=1, column=1, 
                                                                               sticky=tk.W, padx=(10, 0), pady=5)
        
        # Enable Registration
        self.enable_registration_var = tk.BooleanVar(value=self.config.get('EnableRegistration', False))
        ttk.Checkbutton(section, text="Enable User Registration", variable=self.enable_registration_var).grid(row=2, column=0, 
                                                                                                            columnspan=2, sticky=tk.W, pady=5)
    
    def create_advanced_section(self, parent):
        """Advanced configuration options"""
        section = self.create_section_frame(parent, "Advanced Options")
        
        # Database Path
        ttk.Label(section, text="Database Path:").grid(row=0, column=0, sticky=tk.W, pady=5)
        db_frame = ttk.Frame(section)
        db_frame.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        self.db_path_var = tk.StringVar(value=self.config.get('DbPath', './navidrome.db'))
        ttk.Entry(db_frame, textvariable=self.db_path_var, width=30).pack(side=tk.LEFT)
        ttk.Button(db_frame, text="Browse", 
                  command=lambda: self.browse_file(self.db_path_var, [("Database files", "*.db"), ("All files", "*.*")])).pack(side=tk.LEFT, padx=(5, 0))
        
        # Log File
        ttk.Label(section, text="Log File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        log_frame = ttk.Frame(section)
        log_frame.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        self.log_file_var = tk.StringVar(value=self.config.get('LogFile', ''))
        ttk.Entry(log_frame, textvariable=self.log_file_var, width=30).pack(side=tk.LEFT)
        ttk.Button(log_frame, text="Browse", 
                  command=lambda: self.browse_file(self.log_file_var, [("Log files", "*.log"), ("All files", "*.*")])).pack(side=tk.LEFT, padx=(5, 0))
        
        # Verbose Logging
        self.verbose_logging_var = tk.BooleanVar(value=self.config.get('VerboseLogging', False))
        ttk.Checkbutton(section, text="Verbose Logging", variable=self.verbose_logging_var).grid(row=2, column=0, 
                                                                                                columnspan=2, sticky=tk.W, pady=5)
    
    def browse_folder(self, string_var):
        """Browse for a folder"""
        folder = filedialog.askdirectory()
        if folder:
            string_var.set(folder)
    
    def browse_file(self, string_var, file_types):
        """Browse for a file"""
        file_path = filedialog.askopenfilename(filetypes=file_types)
        if file_path:
            string_var.set(file_path)
    
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = toml.load(f)
            else:
                self.config = {}
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {str(e)}")
            self.config = {}
    
    def load_config_file(self):
        """Load configuration from a selected file"""
        file_path = filedialog.askopenfilename(
            title="Select Navidrome Configuration File",
            filetypes=[("TOML files", "*.toml"), ("All files", "*.*")]
        )
        if file_path:
            self.config_file = file_path
            self.load_config()
            self.update_ui_from_config()
            messagebox.showinfo("Success", f"Configuration loaded from {file_path}")
    
    def update_ui_from_config(self):
        """Update UI elements with loaded configuration"""
        # Update all variables with loaded config
        if hasattr(self, 'log_level_var'):
            self.log_level_var.set(self.config.get('LogLevel', 'INFO'))
        if hasattr(self, 'port_var'):
            self.port_var.set(str(self.config.get('Port', 4533)))
        if hasattr(self, 'address_var'):
            self.address_var.set(self.config.get('Address', '0.0.0.0'))
        if hasattr(self, 'data_folder_var'):
            self.data_folder_var.set(self.config.get('DataFolder', './data'))
        if hasattr(self, 'music_folder_var'):
            self.music_folder_var.set(self.config.get('MusicFolder', ''))
        if hasattr(self, 'ffmpeg_path_var'):
            self.ffmpeg_path_var.set(self.config.get('FFmpegPath', ''))
        if hasattr(self, 'scan_schedule_var'):
            self.scan_schedule_var.set(self.config.get('ScanSchedule', '@every 24h'))
        if hasattr(self, 'auto_scan_var'):
            self.auto_scan_var.set(self.config.get('AutoScan', True))
        if hasattr(self, 'scan_at_startup_var'):
            self.scan_at_startup_var.set(self.config.get('ScanAtStartup', True))
        if hasattr(self, 'cache_size_var'):
            self.cache_size_var.set(self.config.get('TranscodingCacheSize', '150MiB'))
        if hasattr(self, 'enable_transcoding_var'):
            self.enable_transcoding_var.set(self.config.get('EnableTranscoding', True))
        if hasattr(self, 'transcode_format_var'):
            self.transcode_format_var.set(self.config.get('TranscodingFormat', 'mp3'))
        if hasattr(self, 'enable_web_var'):
            self.enable_web_var.set(self.config.get('EnableWebInterface', True))
        if hasattr(self, 'theme_var'):
            self.theme_var.set(self.config.get('Theme', 'default'))
        if hasattr(self, 'enable_downloads_var'):
            self.enable_downloads_var.set(self.config.get('EnableDownloads', True))
        if hasattr(self, 'enable_auth_var'):
            self.enable_auth_var.set(self.config.get('EnableAuthentication', True))
        if hasattr(self, 'session_timeout_var'):
            self.session_timeout_var.set(str(self.config.get('SessionTimeout', 24)))
        if hasattr(self, 'enable_registration_var'):
            self.enable_registration_var.set(self.config.get('EnableRegistration', False))
        if hasattr(self, 'db_path_var'):
            self.db_path_var.set(self.config.get('DbPath', './navidrome.db'))
        if hasattr(self, 'log_file_var'):
            self.log_file_var.set(self.config.get('LogFile', ''))
        if hasattr(self, 'verbose_logging_var'):
            self.verbose_logging_var.set(self.config.get('VerboseLogging', False))
    
    def save_config(self):
        """Save configuration to file"""
        try:
            # Build configuration dictionary from UI variables
            config = {}
            
            # General settings
            config['LogLevel'] = self.log_level_var.get()
            config['Port'] = int(self.port_var.get())
            config['Address'] = self.address_var.get()
            config['DataFolder'] = self.data_folder_var.get()
            
            # Paths
            if self.music_folder_var.get():
                config['MusicFolder'] = self.music_folder_var.get()
            if self.ffmpeg_path_var.get():
                config['FFmpegPath'] = self.ffmpeg_path_var.get()
            
            # Scanning
            config['ScanSchedule'] = self.scan_schedule_var.get()
            config['AutoScan'] = self.auto_scan_var.get()
            config['ScanAtStartup'] = self.scan_at_startup_var.get()
            
            # Transcoding
            config['TranscodingCacheSize'] = self.cache_size_var.get()
            config['EnableTranscoding'] = self.enable_transcoding_var.get()
            config['TranscodingFormat'] = self.transcode_format_var.get()
            
            # Web interface
            config['EnableWebInterface'] = self.enable_web_var.get()
            config['Theme'] = self.theme_var.get()
            config['EnableDownloads'] = self.enable_downloads_var.get()
            
            # Security
            config['EnableAuthentication'] = self.enable_auth_var.get()
            config['SessionTimeout'] = int(self.session_timeout_var.get())
            config['EnableRegistration'] = self.enable_registration_var.get()
            
            # Advanced
            config['DbPath'] = self.db_path_var.get()
            if self.log_file_var.get():
                config['LogFile'] = self.log_file_var.get()
            config['VerboseLogging'] = self.verbose_logging_var.get()
            
            # Save to file
            with open(self.config_file, 'w', encoding='utf-8') as f:
                toml.dump(config, f)
            
            messagebox.showinfo("Success", f"Configuration saved to {self.config_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
    
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        if messagebox.askyesno("Reset Configuration", 
                              "Are you sure you want to reset all settings to defaults?"):
            self.config = {}
            self.update_ui_from_config()
            messagebox.showinfo("Success", "Configuration reset to defaults")
    
    def view_raw_toml(self):
        """View the raw TOML configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                content = "# No configuration file found"
            
            # Create new window to display TOML
            toml_window = tk.Toplevel(self.root)
            toml_window.title("Raw TOML Configuration")
            toml_window.geometry("600x500")
            
            text_widget = scrolledtext.ScrolledText(toml_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read TOML file: {str(e)}")

def main():
    # Check if toml module is available
    try:
        import toml
    except ImportError:
        messagebox.showerror("Missing Dependency", 
                           "The 'toml' module is required. Please install it with:\npip install toml")
        return
    
    root = tk.Tk()
    app = NavidromeConfigGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

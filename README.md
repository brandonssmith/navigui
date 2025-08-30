# Navidrome Configuration GUI

A user-friendly graphical interface for configuring [Navidrome](https://github.com/navidrome/navidrome), the open-source music streaming server.

Basically I got sick of trying to configure Navidrome through a text interface so I wroate a quick gui for the config. It loads your navidrome.toml file, allows you to modify it and then save back to it.

BAT and PS1 startup files are included for easy startup if you so choose.

## Features

The GUI provides an intuitive way to configure all major Navidrome settings organized into logical sections:

### 🎯 General Settings
- **Log Level**: Choose between DEBUG, INFO, WARN, or ERROR
- **Port**: Set the server port (default: 4533)
- **Address**: Configure the server address (default: 0.0.0.0)
- **Data Folder**: Set the folder for Navidrome's data files

### 🎵 Music & Media Paths
- **Music Folder**: Browse and set your music library location
- **FFmpeg Path**: Specify the path to your FFmpeg executable for transcoding

### 🔍 Library Scanning
- **Scan Schedule**: Choose from predefined intervals or manual scanning
- **Auto Scan**: Enable/disable automatic library scanning
- **Scan at Startup**: Control whether to scan when Navidrome starts

### 🎧 Audio Transcoding
- **Cache Size**: Set transcoding cache size (50MiB to 1GiB)
- **Enable Transcoding**: Toggle transcoding functionality
- **Default Format**: Choose output format (mp3, aac, ogg, opus)

### 🌐 Web Interface
- **Enable Web Interface**: Toggle the web UI
- **Theme**: Choose between default, dark, or light themes
- **Enable Downloads**: Control download functionality

### 🔒 Security & Authentication
- **Enable Authentication**: Toggle user authentication
- **Session Timeout**: Set session duration in hours
- **Enable Registration**: Control user self-registration

### ⚙️ Advanced Options
- **Database Path**: Set custom database location
- **Log File**: Specify custom log file path
- **Verbose Logging**: Enable detailed logging

## Installation & Usage

### Prerequisites
- Python 3.6 or higher
- Windows 10/11 (the GUI is designed for Windows)

### Quick Start (Windows)

1. **Download the files** to your desired directory
2. **Double-click** `run_navidrome_config.bat`
3. The batch file will automatically:
   - Check if Python is installed
   - Install required dependencies
   - Launch the configuration GUI

### Manual Installation

1. **Install Python dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

2. **Run the GUI**:
   ```cmd
   python navidrome_config_gui.py
   ```

## How to Use

### Loading Configuration
- The GUI automatically loads `navidrome.toml` if it exists in the same directory
- Use "Load Configuration" to open a different config file
- Use "Reset to Defaults" to restore default settings

### Making Changes
1. **Navigate** through the different configuration sections
2. **Modify** settings using the intuitive controls:
   - Dropdown menus for predefined options
   - Text fields for custom values
   - Checkboxes for boolean settings
   - Browse buttons for file/folder selection
3. **Save** your configuration using the "Save Configuration" button

### Viewing Raw Configuration
- Use "View Raw TOML" to see the generated TOML file
- This helps verify that your settings are correctly formatted

## Configuration File

The GUI generates a `navidrome.toml` file that Navidrome can read directly. The file follows the [TOML format](https://toml.io/) and includes all the standard Navidrome configuration options.

### Example Generated Configuration
```toml
LogLevel = 'INFO'
Port = 4533
Address = '0.0.0.0'
DataFolder = './data'
MusicFolder = 'E:\\Music'
FFmpegPath = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
ScanSchedule = '@every 24h'
AutoScan = true
ScanAtStartup = true
TranscodingCacheSize = '150MiB'
EnableTranscoding = true
TranscodingFormat = 'mp3'
EnableWebInterface = true
Theme = 'default'
EnableDownloads = true
EnableAuthentication = true
SessionTimeout = 24
EnableRegistration = false
DbPath = './navidrome.db'
VerboseLogging = false
```

## Troubleshooting

### Common Issues

**Python not found**
- Install Python from [python.org](https://www.python.org/downloads/)
- Ensure "Add Python to PATH" is checked during installation

**Missing dependencies**
- The batch file automatically installs required packages
- Manual installation: `pip install toml`

**Configuration not saving**
- Check file permissions in the target directory
- Ensure the target path is writable

**GUI not responding**
- Check if the configuration file is corrupted
- Try resetting to defaults and reconfiguring

### Getting Help

- **Navidrome Documentation**: [navidrome.org/docs](https://www.navidrome.org/docs)
- **Navidrome GitHub**: [github.com/navidrome/navidrome](https://github.com/navidrome/navidrome)
- **Configuration Options**: [navidrome.org/docs/usage/configuration-options](https://www.navidrome.org/docs/usage/configuration-options)

## File Structure

```
navigui/
├── navidrome_config_gui.py    # Main GUI application
├── run_navidrome_config.bat   # Windows launcher script
├── requirements.txt           # Python dependencies
├── README.md                 # This file
└── navidrome.toml            # Your Navidrome configuration
```

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the GUI. The application is designed to be easily extensible for additional configuration options.

## License

This GUI is provided as-is to help users configure Navidrome. Navidrome itself is licensed under GPL-3.0.

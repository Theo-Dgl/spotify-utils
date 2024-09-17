# Spotify Playlist Manager

Spotify Playlist Manager is a powerful command-line tool designed to help Spotify users efficiently organize and manage their playlists. This application offers a range of features to streamline your music library, including:

- Removing duplicate tracks within playlists
- Identifying duplicate songs across multiple playlists
- Syncing playlist tracks with your Liked Songs
- Exporting playlist information to CSV files for easy analysis
- Cleaning up playlists by removing unliked songs
- Analyzing similarity between playlists
- Creating an 'Unclassified' playlist for orphaned liked songs
- Automatically following artists based on your listening preferences

Built with Python and utilizing the Spotify API, this tool provides an intuitive interface for music enthusiasts to maintain a well-organized and personalized Spotify library. Whether you're a casual listener or a playlist curator, Spotify Playlist Manager offers the functionality to enhance your music management experience.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- A Spotify account
- Spotify Developer credentials (Client ID and Client Secret)

### Installation

1. Set up a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
Copy
2. Install required packages:
pip install -r requirements.txt
Copy
3. Create a `.env` file in the project root and add your Spotify API credentials:
```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

### Usage

1. Run the main script:
`python main.py`

2. On first run, you'll be prompted to authorize the application with your Spotify account. Follow the URL provided and grant the necessary permissions.

3. Use the menu to select the desired operation:
- Enter the number corresponding to the action you want to perform.
- Follow any additional prompts for specific actions.

4. To exit the application, select option '0' from the main menu.

### Notes

- Ensure you have a stable internet connection while using the application.
- Some operations may take time depending on the size of your playlists and library.
- It's recommended to backup your playlists before making significant changes.
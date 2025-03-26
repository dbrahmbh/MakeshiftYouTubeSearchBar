# Makeshift YouTube Search Bar

A web application that allows users to search for YouTube videos based on keywords. Users can view video titles, channel names, descriptions, publish dates, thumbnails, and access direct links to the videos.

## Features

- **Search Functionality**: Input keywords to retrieve relevant YouTube videos.
- **Results Display**: View video details including title, channel, description, publish date, and thumbnail.
- **Filters**: Apply filters such as regular expressions, specify the number of results, and reverse the order of results.

## Prerequisites

- **Python 3.x**: Ensure Python is installed. Download it from the [official website](https://www.python.org/).
- **pip**: Python's package installer. It comes bundled with Python 3.4 and above.
- **Git**: For cloning the repository. Download it from the [official website](https://git-scm.com/).

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/dbrahmbh/MakeshiftYouTubeSearchBar.git
   ```

   Navigate to the project directory:

   ```bash
   cd MakeshiftYouTubeSearchBar
   ```

2. **Set Up a Virtual Environment**:

   It's recommended to use a virtual environment to manage dependencies.

   On Windows:

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   With the virtual environment activated, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

   If `requirements.txt` is not available, manually install the dependencies:

   ```bash
   pip install flask flask-bootstrap flask-sqlalchemy sqlalchemy google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib flask-markdown
   ```

4. **Obtain a YouTube Data API Key**:

   - Visit the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.
   - Navigate to **APIs & Services** > **Library**.
   - Enable the **YouTube Data API v3**.
   - Go to **APIs & Services** > **Credentials**.
   - Click **Create Credentials** > **API key**.
   - Copy the generated API key.

5. **Configure the Application**:

   Create a `.env` file in the project root directory and add your API key:

   ```env
   YOUTUBE_API_KEY=YOUR_API_KEY_HERE
   ```

   Replace `YOUR_API_KEY_HERE` with the API key obtained from the Google Cloud Console.

6. **Initialize the Database**:

   If running the application for the first time or if you need to reset the database:

   ```bash
   python db_manager.py
   ```

   This will set up the SQLite database (`youtube.sqlite`).

## Running the Application

1. **Activate the Virtual Environment**:

   Ensure the virtual environment is active.

2. **Start the Flask Application**:

   ```bash
   python youtube_api.py
   ```

   The application will start, and you'll see output indicating it's running, such as:

   ```
   Running on http://127.0.0.1:5000/
   ```

3. **Access the Application**:

   Open your web browser and navigate to `http://127.0.0.1:5000/`. You should see the home page with the search bar.

## Usage

1. **Search**:

   - Enter a keyword or phrase in the search bar.
   - Click **Submit** to view search results.

2. **Apply Filters**:

   - Navigate to the **Filters** page.
   - Set desired filters:
     - **Regular Expression**: Filter results based on regex patterns.
     - **Number of Results**: Specify how many results to display.
     - **Reverse Results**: Display results in reverse order.
   - Save and apply filters to refine your search.

## Troubleshooting

- **ModuleNotFoundError**: Ensure all dependencies are installed in the virtual environment.
- **API Errors**: Verify that the YouTube Data API v3 is enabled and the API key is correct.
- **Port Issues**: If port 5000 is in use, modify the `youtube_api.py` to run on a different port:

  ```python
  if __name__ == '__main__':
      app.run(port=5001)
  ```

  Then, access the application at `http://127.0.0.1:5001/`.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - The web framework used.
- [YouTube Data API v3](https://developers.google.com/youtube/v3) - For fetching YouTube data.
- [Bootstrap](https://getbootstrap.com/) - For front-end styling.

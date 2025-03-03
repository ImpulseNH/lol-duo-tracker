<a id="readme-top"></a>



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://duotracker.pythonanywhere.com/">
    🔎
  </a>

  <h3 align="center">League of Legends Duo Tracker</h3>

  <p align="center">
    League of Legends match analyzer to find common games between two summoners
    <br />
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#search-strategy">Search Strategy</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#setup">Setup</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is a web app that finds and displays common matches between two League of Legends players.

### Features
- Search for matches between two players using their Riot IDs (currently only last 100 games)
- Displays match details including champions, items, and game statistics
- Supports multiple regions
- Shows match history with timestamps

### Search Strategy

The app mainly uses the MATCH-V5 endpoint to search for common matches by comparing a user-defined number of match IDs (`match_id`) in the `settings.py`.
This approach avoids the need to review each match's info to determine if one summoner participated in another summoner's match, avoiding extra API calls.

However, this method may not be effective if either player has many recent matches.
One way I tried to address this is by searching for recent matches starting from the date of the last match played between both summoners.

While the app serves its purpose, I know that it needs improvements to make it more efficient and effective.
This app was developed with practical purposes in mind, to test and demonstrate my current knowledge. Therefore, I will likely continue to review and improve it.

### Built With

Built with Python 3.10.

* [![Flask][Flask.com]][Flask-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

In order for the app to work properly, you must obtain a valid Riot API key at [Riot Developer Portal](https://developer.riotgames.com/).

### Prerequisites

* Python 3.10 or higher
* Valid Riot API key

### Setup

1. Clone the repo
   ```sh
   git clone https://github.com/ImpulseNH/lol-duo-tracker.git
   ```
2. Create a virtual enviroment
   ```sh
   python -m venv venv
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with your Riot API key and Flask secret key:
   ```
   RIOT_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```
5. Run the app:
   ```bash
   python run.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
1. Open your browser and navigate to `http://localhost:5000`
2. Select the region for both players
3. Enter two Riot IDs in the format `gamename#tagline` (e.g., `Faker#KR1`)
4. Click "Search" to find common matches
5. View match details including:
   - Champions played
   - Items built
   - KDA ratios
   - Match duration
   - Game mode
   - Match date

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Choose an Open Source License](https://choosealicense.com)
* [Img Shields](https://shields.io)
* [GitHub Readme Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[Flask.com]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com

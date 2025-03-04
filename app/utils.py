# Import libraries
import os
import requests
from typing import Dict, Any, List, Optional
import time
from requests.exceptions import HTTPError

# dotenv
from dotenv import load_dotenv

# Settings  
from . import settings

# Base URL
BASE_URL = "api.riotgames.com"

# Load environment variables
load_dotenv()


def get_api_key() -> str:
    api_key = os.getenv("RIOT_API_KEY")
    if not api_key:
        raise ValueError("RIOT_API_KEY not found in environment variables.")
    return api_key


def build_api_url(endpoint: str, region: str) -> str:
    return f"https://{region}.{BASE_URL}/{endpoint}"


def get_account_data(gameName: str, tagLine: str, region: str = settings.DEFAULT_REGION) -> Dict[str, Any]:
    """
    Fetches the account data based on the game name and tag line.
    
    :param gameName: The game name of the account.
    :param tagLine: The tag line of the account.
    :param region: The region to query (default is settings.DEFAULT_REGION).
    :return: The account's data.
    :raises: ValueError if API key is missing, RequestException if API request fails
    """
    api_key = get_api_key()
    api_url = build_api_url(f"riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}", region)
    params = {
        "api_key": api_key
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except HTTPError as err:
        print(err)
        if err.response.status_code == 404:
            raise ValueError(f"Account not found: {gameName}#{tagLine}")
        raise ValueError(f"Error fetching account data")


def get_matches_ids(puuid: str, start: int = 0, count: int = settings.DEFAULT_MATCH_COUNT, endTime: int = None, region: str = settings.DEFAULT_REGION) -> List[str]:
    """
    Fetches the match history of a summoner based on the summoner's PUUID.
    
    :param puuid: The PUUID of the summoner.
    :param count: Number of matches to retrieve.
    :param endTime: End timestamp for filtering matches (in seconds).
    :param region: The region to query.
    :return: The summoner's match history.
    :raises: ValueError if API key is missing or PUUID is invalid, RequestException if API request fails
    """
    api_key = get_api_key()
    
    if not puuid:
        raise ValueError("PUUID not provided.")
    
    api_url = build_api_url(f"lol/match/v5/matches/by-puuid/{puuid}/ids", region)
    params = {
        "api_key": api_key,
        "start": start,
        "count": count
    }
    
    if endTime is not None:
        params["endTime"] = endTime
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except HTTPError as err:
        print(err)
        raise ValueError(f"Error fetching match history")


def get_match_data(match_id: str, region: str = settings.DEFAULT_REGION) -> Dict[str, Any]:
    """
    Fetches the match data based on the match ID.
    
    :param match_id: The ID of the match.
    :param region: The region to query (default is settings.DEFAULT_REGION).
    :return: The match data.
    :raises: ValueError if API key is missing, RequestException if API request fails
    """
    api_key = get_api_key()
    api_url = build_api_url(f"lol/match/v5/matches/{match_id}", region)
    params = {
        "api_key": api_key
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        return response.json()
    except HTTPError as err:
        print(err)
        if err.response.status_code == 404:
            raise ValueError(f"Match not found: {match_id}")
        elif err.response.status_code == 429:
            raise ValueError("Rate limit exceeded, could not fetch all matches. Please try again later.")
        else:
            raise ValueError(f"Error fetching match data")
    

def get_last_match_timestamp(summoner1_puuid: str, summoner2_puuid: str, region: str = settings.DEFAULT_REGION) -> int:
    """
    Gets the oldest timestamp between the last matches of two summoners.

    Example: If summoner1's last match was on 2024-01-01 and summoner2's last match was on 2023-01-01,
    it will return the timestamp from 2023-01-01 (the oldest one).
    
    :param summoner1_puuid: PUUID of the first summoner
    :param summoner2_puuid: PUUID of the second summoner
    :param region: Region to query (default is settings.DEFAULT_REGION)
    :return: Timestamp of the oldest last match (in seconds)
    :raises: ValueError if no matches found for either summoner
    """
    # Get the last id of the last match of each summoner
    count = 1
    summoner1_matches_ids = get_matches_ids(summoner1_puuid, start=0, count=count, region=region)
    summoner2_matches_ids = get_matches_ids(summoner2_puuid, start=0, count=count, region=region)
    
    if not summoner1_matches_ids or not summoner2_matches_ids:
        raise ValueError("No matches found for one or both summoners")
    
    # Get the match data of the last match of each summoner
    summoner1_last_match_data = get_match_data(summoner1_matches_ids[0], region)
    summoner2_last_match_data = get_match_data(summoner2_matches_ids[0], region)

    # Get the timestamp of the last match of each summoner
    summoner1_last_match_timestamp = summoner1_last_match_data.get('info', {}).get('gameStartTimestamp')
    summoner2_last_match_timestamp = summoner2_last_match_data.get('info', {}).get('gameStartTimestamp')
    
    if not summoner1_last_match_timestamp or not summoner2_last_match_timestamp:
        raise ValueError("Could not get match timestamps")
    
    return int(min(summoner1_last_match_timestamp, summoner2_last_match_timestamp) / 1000)


def get_matches_ids_from_timestamp(summoner1_puuid: str, summoner2_puuid: str, last_match_timestamp: int, region: str = settings.DEFAULT_REGION) -> Optional[List[str]]:
    """
    Fetches the match history of both summoners from a specific timestamp.

    Example: If summoner1's last match was on 2024-01-01 and summoner2's last match was on 2023-01-01,
    matches will be fetched starting from 2023-01-01 (the oldest timestamp).

    This is used to start the search from the oldest match between both summoners,
    avoiding unnecessary match searches.
    
    :param summoner1_puuid: The PUUID of the summoner 1.
    :param summoner2_puuid: The PUUID of the summoner 2.
    :param last_match_timestamp: The last match timestamp from which to start the search.
    :param region: The region to query.
    :return: The match history of both summoners.
    """
    summoner1_match_history = []
    summoner2_match_history = []

    # Variable used as start parameter for the matches ids request
    match_index = 0
    # MATCH-V5 API limits requests to 100 matches per call.
    # Multiple requests are needed to fetch more matches, using
    # the 'start' parameter to paginate through results
    for i in range(0, settings.MAX_MATCH_HISTORY_REQUESTS):
        match_index = i * settings.DEFAULT_MATCH_COUNT

        # Get matches for summoner1
        summoner1_match_history.extend(get_matches_ids(
            summoner1_puuid, 
            start=match_index,
            count=settings.DEFAULT_MATCH_COUNT,
            endTime=last_match_timestamp,
            region=region
        ))

        # Get matches for summoner2
        summoner2_match_history.extend(get_matches_ids(
            summoner2_puuid,
            start=match_index,
            count=settings.DEFAULT_MATCH_COUNT,
            endTime=last_match_timestamp,
            region=region
        ))
    
    if not summoner1_match_history or not summoner2_match_history:
        raise ValueError("Could not get match history")

    # Return the matches ids of both summoners
    return summoner1_match_history, summoner2_match_history


def get_current_game_version() -> str:
    """
    Fetches the current game version from the Riot API.
    
    :return: The current game version.
    """
    response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json", params={})
    versions = response.json()

    if not versions:
        raise ValueError("Could not get game version")
    
    return versions[0]


def get_time_ago(timestamp_ms: int) -> str:
    """
    Calculates the time elapsed from a timestamp until now.
    
    :param timestamp_ms: Timestamp in milliseconds.
    :return: String with the elapsed time in readable format.
    """
    # Convert milliseconds to seconds
    timestamp_s = timestamp_ms / 1000
    
    # Get current time in seconds
    now = time.time()
    
    # Calculate difference in seconds
    diff = now - timestamp_s
    
    # Convert to different time units
    if diff < 60:
        return "less than a minute ago"
    elif diff < 3600:
        minutes = int(diff / 60)
        return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"
    elif diff < 86400:
        hours = int(diff / 3600)
        return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
    elif diff < 2592000:  # 30 days
        days = int(diff / 86400)
        return f"{days} {'day' if days == 1 else 'days'} ago"
    elif diff < 31536000:  # 365 days
        months = int(diff / 2592000)
        return f"{months} {'month' if months == 1 else 'months'} ago"
    else:
        years = int(diff / 31536000)
        return f"{years} {'year' if years == 1 else 'years'} ago"
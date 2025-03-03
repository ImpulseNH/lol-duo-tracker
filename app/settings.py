# API configuration
DEFAULT_REGION = "AMERICAS"
DEFAULT_MATCH_COUNT = 100  # Default number of matches to return in one request
MAX_MATCH_LIST_SIZE = 100  # Maximum number of matches to analyze
MAX_MATCH_HISTORY_REQUESTS = MAX_MATCH_LIST_SIZE // DEFAULT_MATCH_COUNT # Maximum number of requests to get match history
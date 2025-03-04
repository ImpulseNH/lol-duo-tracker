from flask import Blueprint, render_template, flash
from .forms import MyForm
from . import utils, settings

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    common_matches = []
    region = None
    current_game_version = None
    last_match_timestamp = 0
    found_summoners = False

    # Check if form was submitted
    if form.validate_on_submit():
        try:
            # Get the current game version
            current_game_version = utils.get_current_game_version()

            # Get the selected region
            region = form.option.data

            # Get summoner data
            summoner1_parts = form.summoner1.data.split("#")
            summoner2_parts = form.summoner2.data.split("#")
            summoner1_gamename, summoner1_tagline = summoner1_parts[0], summoner1_parts[1]
            summoner2_gamename, summoner2_tagline = summoner2_parts[0], summoner2_parts[1]
            
            # Get account data
            summoner1_account_data = utils.get_account_data(summoner1_gamename, summoner1_tagline, region)
            summoner2_account_data = utils.get_account_data(summoner2_gamename, summoner2_tagline, region)

            # Get PUUID and save it to the form
            summoner1_puuid = summoner1_account_data.get('puuid')
            summoner2_puuid = summoner2_account_data.get('puuid')
            form.summoner1_puuid.data = summoner1_puuid
            form.summoner2_puuid.data = summoner2_puuid
            found_summoners = True

            # Get last match timestamp comparing both summoners to start the search from the oldest match between them
            last_match_timestamp = utils.get_last_match_timestamp(summoner1_puuid, summoner2_puuid, region)

            summoner1_match_history = []
            summoner2_match_history = []

            # Get matches ids from oldest match timestamp
            summoner1_match_history, summoner2_match_history = utils.get_matches_ids_from_timestamp(summoner1_puuid, summoner2_puuid, last_match_timestamp, region)

            # Convert to set for faster lookup
            summoner1_matches_set = set(summoner1_match_history)

            # Find common matches
            common_matches_id = [match_id for match_id in summoner2_match_history if match_id in summoner1_matches_set]

            # Get match data for common matches
            for match_id in common_matches_id:
                common_matches.append(utils.get_match_data(match_id, region))

        except ValueError as e:
            flash(str(e), 'danger')
        except Exception as e:
            flash('An unexpected error occurred. Please try again.', 'danger')

    return render_template(
        'index.html',
        form=form,
        found_summoners=found_summoners,
        common_matches=common_matches,
        get_time_ago=utils.get_time_ago,
        current_game_version=current_game_version,
        settings=settings
    )
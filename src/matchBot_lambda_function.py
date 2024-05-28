import json
import boto3
import pandas as pd
import os
from dateutil.parser import parse
from datetime import datetime

s3 = boto3.client('s3')

# Constants
BUCKET_NAME = 'iplmatch2019'
EXCEL_FILE_KEY = 'IPL_Matches_Gravitas_AI_Problem_Statement_Sorted_Data.xlsx'
local_file_path = "/tmp/ipl.xlsx"

def lambda_handler(event, context):
    try:
        # Download the file from S3
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        s3.download_file(BUCKET_NAME, EXCEL_FILE_KEY, local_file_path)
        excel_data = pd.read_excel(local_file_path)
        print(f"File downloaded successfully from S3 bucket '{BUCKET_NAME}' with key '{EXCEL_FILE_KEY}' to '{local_file_path}'.")
    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        return generate_response("Error downloading file from S3", str(e), False)

    try:
        # Extract data from the Lex event
        print(event)
        session_state = event['sessionState']
        intent = session_state['intent']
        slots = intent.get('slots', {})
        intent_name = intent.get('name')

        # Handle the intent based on its name
        if intent_name == 'MatchDetails':
            response = handle_match_details_intent(excel_data, slots)
        elif intent_name == 'TeamStats':
            response = handle_team_stats_intent(excel_data, slots)
        elif intent_name == 'PlayerOfTheMatch':
            response = handle_player_of_the_match_intent(excel_data, slots)
        elif intent_name == 'TossDetails':
            response = handle_toss_details_intent(excel_data, slots)
        else:
            response = generate_response("Failed", "Sorry, I am not able to handle that request.", False)

        return response

    except Exception as e:
        print(f"Error processing the event: {e}")
        return generate_response("Error processing the event", str(e), False)

def check_missing_slot(slots, slot_name, prompt_message, intent_name):
    slot_value = slots.get(slot_name, {}).get('value', {}).get('interpretedValue')

    if not slot_value:
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "slotToElicit": slot_name,
                },
                "intent": {
                    "name": intent_name,
                    "slots": slots,
                    "state": "InProgress"
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": prompt_message
                }
            ]
        }
    return slot_value

def handle_match_details_intent(excel_data, slots):
    try:
        team_one = check_missing_slot(slots, 'TeamOne', "Please provide the name of the first team.", "MatchDetails")
        if isinstance(team_one, dict):
            return team_one

        team_two = check_missing_slot(slots, 'TeamTwo', "Please provide the name of the second team.", "MatchDetails")
        if isinstance(team_two, dict):
            return team_two

        match_date = check_missing_slot(slots, 'MatchDate', "Please provide the date of the match.", "MatchDetails")
        if isinstance(match_date, dict):
            return match_date

        given_date = convert_to_date(match_date)
        formatted_date = given_date.strftime('%d-%m-%Y')

        # Filter DataFrame based on match details
        match_details = excel_data[(excel_data['team1'] == team_one) & 
                                   (excel_data['team2'] == team_two) &
                                   (excel_data['date'] == formatted_date)
                                ]

        # Check if the match is found
        if not match_details.empty:
            venue = match_details.iloc[0]['venue']
            city = match_details.iloc[0]['city']
            winner = match_details.iloc[0]['winner']
            win_by_runs = match_details.iloc[0]['win_by_runs']
            win_by_wickets = match_details.iloc[0]['win_by_wickets']
            dl_applied = match_details.iloc[0]['dl_applied']
            player_of_match = match_details.iloc[0]['player_of_match']

            # Construct response message
            response_message = f"The match between {team_one} and {team_two} on {match_date} at {venue} in {city} was won by {winner}."
            response_message += f" {winner} won by {win_by_runs} runs." if win_by_runs > 0 else ""
            response_message += f" {winner} won by {win_by_wickets} wickets." if win_by_wickets > 0 else ""
            response_message += f" (DL applied)." if dl_applied else ""
            response_message += f" Player of the match: {player_of_match}."
        else:
            response_message = "Sorry, I couldn't find details for the specified match."

        return generate_response("MatchDetails", response_message, True)

    except Exception as e:
        print(f"Error handling MatchDetails intent: {e}")
        return generate_response("MatchDetails", str(e), False)

def handle_player_of_the_match_intent(excel_data, slots):
    try:
        team_one = check_missing_slot(slots, 'TeamOne', "Please provide the name of the first team.", "PlayerOfTheMatch")
        if isinstance(team_one, dict):
            return team_one

        team_two = check_missing_slot(slots, 'TeamTwo', "Please provide the name of the second team.", "PlayerOfTheMatch")
        if isinstance(team_two, dict):
            return team_two

        match_date = check_missing_slot(slots, 'MatchDate', "Please provide the date of the match.", "PlayerOfTheMatch")
        if isinstance(match_date, dict):
            return match_date

        given_date = convert_to_date(match_date)
        formatted_date = given_date.strftime('%d-%m-%Y')

        # Filter DataFrame based on match details
        match_details = excel_data[(excel_data['team1'] == team_one) & 
                                   (excel_data['team2'] == team_two) &
                                   (excel_data['date'] == formatted_date)]

        # Check if the match is found
        if not match_details.empty:
            player_of_match = match_details.iloc[0]['player_of_match']
            venue = match_details.iloc[0]['venue']
            city = match_details.iloc[0]['city']

            # Construct response message
            response_message = f"The player of the match for the match between {team_one} and {team_two} on {match_date} at {venue} in {city} was {player_of_match}."

        else:
            response_message = "Sorry, I couldn't find details for the specified match."

        return generate_response("PlayerOfTheMatch", response_message, True)

    except Exception as e:
        print(f"Error handling PlayerOfTheMatch intent: {e}")
        return generate_response("PlayerOfTheMatch", str(e), False)

def handle_toss_details_intent(excel_data, slots):
    try:
        team_one = check_missing_slot(slots, 'TeamOne', "Please provide the name of the first team.", "TossDetails")
        if isinstance(team_one, dict):
            return team_one

        team_two = check_missing_slot(slots, 'TeamTwo', "Please provide the name of the second team.", "TossDetails")
        if isinstance(team_two, dict):
            return team_two

        match_date = check_missing_slot(slots, 'MatchDate', "Please provide the date of the match.", "TossDetails")
        if isinstance(match_date, dict):
            return match_date

        given_date = convert_to_date(match_date)
        formatted_date = given_date.strftime('%d-%m-%Y')

        # Filter DataFrame based on match details
        match_details = excel_data[(excel_data['team1'] == team_one) & 
                                   (excel_data['team2'] == team_two) &
                                   (excel_data['date'] == formatted_date)]

        # Check if the match is found
        if not match_details.empty:
            toss_winner = match_details.iloc[0]['toss_winner']
            toss_decision = match_details.iloc[0]['toss_decision']
            venue = match_details.iloc[0]['venue']

            # Construct response message
            response_message = f"The toss for the match between {team_one} and {team_two} on {match_date} at {venue} was won by {toss_winner}, and they decided to {toss_decision}."
        else:
            response_message = "Sorry, I couldn't find details for the specified match."

        return generate_response("TossDetails", response_message, True)

    except Exception as e:
        print(f"Error handling TossDetails intent: {e}")
        return generate_response("TossDetails", str(e), False)

def handle_team_stats_intent(excel_data, slots):
    try:
        team_name = check_missing_slot(slots, 'TeamName', "Please provide the name of the team.", "TeamStats")
        if isinstance(team_name, dict):
            return team_name

        # Filter DataFrame based on team name
        team_matches = excel_data[(excel_data['team1'] == team_name) | (excel_data['team2'] == team_name)]

        # Check if the team is found
        if not team_matches.empty:
            total_matches = len(team_matches)
            wins = len(team_matches[(team_matches['winner'] == team_name)])
            losses = total_matches - wins

            # Construct response message
            response_message = f"{team_name} played {total_matches} matches, won {wins} and lost {losses} in IPL 2019."
        else:
            response_message = "Sorry, I couldn't find stats for the specified team."

        return generate_response("TeamStats", response_message, True)

    except Exception as e:
        print(f"Error handling TeamStats intent: {e}")
        return generate_response("TeamStats", str(e), False)

def generate_response(intent_name, message, is_fulfilled):
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close",
            },
            "intent": {
                "name": intent_name,
                "state": "Fulfilled" if is_fulfilled else "Failed"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }

# Function to convert any string to a datetime object
def convert_to_date(date_string):
    try:
        date_obj = parse(date_string)
        return date_obj
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

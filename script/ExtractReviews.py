import logging
import time
from typing import Dict, List
import os
import requests
import json
from datetime import datetime, timedelta

GPLAY_BASE_URL = "https://gplayapi.cashlessconsumer.in"
PLAYDATA_PATH = '../raw-data/reviews/'
REPO_NAME = 'https://flatgithub.com/DigitalIndiaArchiver/NammaYatriStats'

def get_appinfo(app_id):
    url = f"{GPLAY_BASE_URL}/api/apps/{app_id}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def get_permissions(app_id):
    url = f"{GPLAY_BASE_URL}/api/apps/{app_id}/permissions"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def get_datasafety(app_id):
    url = f"{GPLAY_BASE_URL}/api/apps/{app_id}/datasafety"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def get_reviews(app_id, next_pagination_token=None):
    url = f"{GPLAY_BASE_URL}/api/apps/{app_id}/reviews"
    params = {"nextPaginationToken": next_pagination_token} if next_pagination_token else {}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

def flatten_criterias(review):
    flattened_criterias = {}
    for criteria in review.get("criterias", []):
        flattened_criterias[criteria["criteria"]] = criteria.get("rating")
    return flattened_criterias

def extract_all_reviews(app_id, upto_date=None):
    all_reviews = []
    next_pagination_token = None

    while True:
        data = get_reviews(app_id, next_pagination_token)
        if not data:
            break

        reviews = data.get("results", {}).get("data", [])
        next_pagination_token = data.get("results", {}).get("nextPaginationToken")

        if upto_date:
            reviews = [r for r in reviews if datetime.strptime(r["date"], "%Y-%m-%d").date() > upto_date]

        all_reviews.extend(reviews)

        if not next_pagination_token:
            break

    flattened_reviews = []
    for review in all_reviews:
        flattened_review = {
            "id": review["id"],
            "date": review["date"],
            "score": review["score"],
            "scoreText": review["scoreText"],
            "title": review["title"],
            "text": review["text"],
            **flatten_criterias(review),
        }
        flattened_reviews.append(flattened_review)

    return [dict(t) for t in {tuple(d.items()) for d in flattened_reviews}]

def save_app_reviews(app_id: str) -> None:
    """
    Save the reviews of a specific app into a JSON file.

    Args:
        app_id (str): The ID of the app for which the reviews need to be saved.

    Returns:
        None: The function does not return any value. It only saves the reviews into a file.
    """
    review_filename = f"{PLAYDATA_PATH}Reviews_{app_id}.json"
    existing_reviews = []

    if os.path.exists(review_filename):
        with open(review_filename) as review_file:
            existing_reviews = json.load(review_file)
    else:
        existing_reviews = []

    upto_date = (datetime.today() - timedelta(days=7)).date()
    reviews = extract_all_reviews(app_id, upto_date) if existing_reviews else extract_all_reviews(app_id)
    logging.debug('Count of all reviews', len(reviews))
    all_reviews = remove_duplicates(existing_reviews + reviews)
    all_reviews = sorted(all_reviews, key=lambda x: (datetime.strptime(x["date"], "%Y-%m-%d"), x["id"]), reverse=True)
    with open(review_filename, 'w') as file:
        json.dump(all_reviews, file, indent=4)

def remove_duplicates(reviews: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Remove duplicate reviews from the list.

    Args:
        reviews (List[Dict[str, str]]): The list of reviews.

    Returns:
        List[Dict[str, str]]: The list of reviews without duplicates.
    """
    return [dict(t) for t in {tuple(d.items()) for d in reviews}]

def save_app_review_criterias(app_id: str) -> None:
    """
    This function saves the counts of specific criteria in app reviews to a JSON file.

    Args:
        app_id (str): The ID of the app for which the review criteria counts need to be saved.

    Returns:
        None: The function saves the criteria counts to a JSON file.
    """
    logging.log(logging.INFO, 'start of save_app_review_criterias')
    review_filename = f"{PLAYDATA_PATH}Reviews_{app_id}.json"
    criterias_filename = f"{PLAYDATA_PATH}Criterias_{app_id}.json"

    if os.path.exists(review_filename):
        with open(review_filename, 'r') as review_file:
            existing_reviews = json.load(review_file)
    else:
        existing_reviews = []

    criteria_counts: Dict[str, int] = {}

    for single_review in existing_reviews:
        for key in single_review:
            if key.startswith("vaf"):
                criteria_counts[key] = criteria_counts.get(key, 0) + 1
    with open(criterias_filename, 'w') as file:
        json.dump(criteria_counts, file, indent=4)


def generate_markdown_table_with_max_installs(app_package_names):
    # Markdown table header
    markdown_table = "# ONDC Mobility Tracker\n\n"
    markdown_table += "| S.No | App Name | Version | maxInstalls | Score | Ratings | 1 Star | 5 Star | Google Play Info |\n"
    markdown_table += "|------|----------|---------|-------------|-------|---------|--------|--------|------------------|\n"

    for i, app_id in enumerate(app_package_names, start=1):
        data = get_appinfo(app_id)
        if data:
            # Extract relevant information
            app_name = data.get('title', 'N/A')
            max_installs = data.get('maxInstalls', 'N/A')
            score = data.get('score', 'N/A')
            ratings = data.get('ratings', 'N/A')
            one_star = data.get('histogram', {}).get('1', 'N/A')
            five_star = data.get('histogram', {}).get('5', 'N/A')
            version = data.get('version', 'N/A')
            
            review_count = len(json.load(open(f"{PLAYDATA_PATH}Reviews_{app_id}.json")))
            permission_count = len(json.load(open(f"{PLAYDATA_PATH}Permissions_{app_id}.json"))['results'])

            # Generate Google Play and reviews links
            google_play_link = f"[{app_name}](https://play.google.com/store/apps/details?id={app_id})"
            play_info = f"[Reviews ({review_count})]({REPO_NAME}?filename=raw-data%2Freviews%2FReviews_{app_id}.json)"
            play_info += f" - [Permissions ({permission_count})]({REPO_NAME}?filename=raw-data%2Freviews%2FPermissions_{app_id}.json)"

            # Add row to Markdown table
            markdown_table += f"| {i} | {google_play_link} | {version} | {max_installs} | {score} | {ratings} | {one_star} | {five_star} | {play_info} |\n"

    # Write Markdown table to file
    with open('../APPS.md', 'w') as file:
        file.write(markdown_table)


def save_app_permissions(app_id: str) -> None:
    """
    This function saves app permissions to a JSON file.

    Args:
        app_id (str): The ID of the app for which the permissions need to be saved.

    Returns:
        None: The function saves the app permissions to a JSON file.
    """
    logging.log(logging.DEBUG, 'start of save_app_review_criterias')
    permission_filename = f"{PLAYDATA_PATH}Permissions_{app_id}.json"
    data = get_permissions(app_id)
    with open(permission_filename, 'w') as file:
        json.dump(data, file, indent=4)


def save_app_info(app_id: str) -> None:
    """
    This function saves app info to a JSON file.

    Args:
        app_id (str): The ID of the app for which the appinfo need to be saved.

    Returns:
        None: The function saves the app info to a JSON file.
    """
    logging.log(logging.DEBUG, 'start of save_app_review_criterias')
    permission_filename = f"{PLAYDATA_PATH}AppInfo_{app_id}.json"
    data = get_appinfo(app_id)
    with open(permission_filename, 'w') as file:
        json.dump(data, file, indent=4)

def save_app_datasafety(app_id: str) -> None:
    """
    This function saves app datasafety to a JSON file.

    Args:
        app_id (str): The ID of the app for which the datasafety need to be saved.

    Returns:
        None: The function saves the app datasafety to a JSON file.
    """
    logging.log(logging.DEBUG, 'start of save_app_review_criterias')
    datasafety_filename = f"{PLAYDATA_PATH}DataSafety_{app_id}.json"
    data = get_datasafety(app_id)
    with open(datasafety_filename, 'w') as file:
        json.dump(data, file, indent=4)


def generate_data_safety_comparison_table(folder_path):
    # Find all DataSafety* files in the folder
    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.startswith('DataSafety') and file.endswith('.json')]

    # Extract unique types from collectedData across all files
    types = set()
    for file in files:
        with open(file, 'r') as f:
            data = json.load(f)
            types.update(item['type'] for item in data['results']['collectedData'])

    # Group types by main headings
    main_headings = {type.split(' / ')[0] if ' / ' in type else type for type in types}

    # Markdown table header
    markdown_table = "# DataSafety Contents Comparison\n\n| App Name |" + "|".join(f" {main_heading} |" + " ".join(f" {sub_type} |" for sub_type in {type.split(' / ')[1] for type in types if ' / ' in type and type.split(' / ')[0] == main_heading}) for main_heading in main_headings) + "\n| --- |" + "|".join(" --- |" for _ in range(sum(1 + len({type.split(' / ')[1] for type in types if ' / ' in type}) for _ in main_headings))) + "\n"

    # Dictionary to store collectedData items grouped by type for each app
    app_data = {file.replace('.json', ''): {item['type']: item['optional'] for item in json.load(open(file))['results']['collectedData']} for file in files}

    # Iterate through each app and add data to Markdown table
    for app_name, items in app_data.items():
        markdown_table += f"| {app_name} |"
        for main_heading in main_headings:
            for sub_type in {type.split(' / ')[1] for type in types if ' / ' in type and type.split(' / ')[0] == main_heading}:
                type_name = f"{main_heading} / {sub_type}" if sub_type else main_heading
                markdown_table += f" {'Optional' if any(items.get(type_name, {}).values()) else 'Mandatory'} |"
    markdown_table += "\n"
    with open('../APPS2.md', 'w') as file:
        file.write(markdown_table)


if __name__ == "__main__":
    app_ids = ["in.juspay.nammayatri", "in.juspay.nammayatripartner",
                "net.openkochi.yatri", "net.openkochi.yatripartner",
                "in.juspay.jatrisaathi", "in.juspay.jatrisaathidriver",
                "com.yaary.consumer.android", "com.yaary.partner",
                "in.mobility.manayatripartner", "in.mobility.manayatri"]
    logging.basicConfig(filename='ExtractReviews' + time.strftime("%Y%m%d-%H%M%S") + '.log', 
                        format='%(asctime)s %(message)s', level=logging.INFO)
    
    for app_id in app_ids:
        save_app_datasafety(app_id=app_id)
        save_app_info(app_id=app_id)
        save_app_permissions(app_id=app_id)
        save_app_reviews(app_id)
        save_app_review_criterias(app_id)
    generate_markdown_table_with_max_installs(app_ids)
    #markdown_table = generate_data_safety_comparison_table(PLAYDATA_PATH)

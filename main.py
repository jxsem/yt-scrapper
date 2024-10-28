import os
import sys
import json
import re
from bs4 import BeautifulSoup

def extract_video_info_from_html(html_content):
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <a> tags with id="video-title-link"
    video_links = soup.find_all('a', id="video-title-link")

    # List to store data for each video
    video_data = []

    # Function to convert views to a number
    def parse_views(views_text):
        # Remove unwanted characters, keeping only numbers and K/M
        match = re.match(r'([\d,\.]+)\s*([KM]?)', views_text)
        if match:
            number = match.group(1).replace(',', '.')  # Replace ',' with '.' for thousands
            unit = match.group(2)

            # Convert the number to float and adjust based on unit
            number = float(number)
            if unit == 'K':  # Thousands
                number *= 1_000
            elif unit == 'M':  # Millions
                number *= 1_000_000

            return int(number) if number.is_integer() else number
        return 0

    # Extract information for each video
    for a in video_links:
        if 'href' in a.attrs:
            href = a['href']
            # Keep only the part before any additional parameters (&)
            clean_href = href.split('&')[0]
            if clean_href.startswith('/watch?v='):
                video_id = clean_href.split('=')[-1]  # Extract video ID
                title = a.get('title')  # Get the video title

                # Find the views (span tag with specific class)
                views_span = a.find_next('span', class_="inline-metadata-item style-scope ytd-video-meta-block")
                views_text = views_span.get_text(strip=True) if views_span else "0"
                views = parse_views(views_text)  # Parse views text

                # Create a dictionary with video information
                video_info = {
                    'title': title,
                    'id': video_id,
                    'views': views
                }

                # Add dictionary to the list
                video_data.append(video_info)

    return video_data

# Read the .txt file containing HTML
def read_html_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Save JSON to a properly formatted file
def save_hrefs_to_json(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)  # Save as a JSON array

if __name__ == '__main__':
    # Check if folder name is passed as an argument
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_name>")
        sys.exit(1)

    # Get the folder name from the arguments
    folder_name = sys.argv[1]

    # Define input and output paths
    input_file = os.path.join(folder_name, 'input.txt')
    output_file = os.path.join(folder_name, 'output.json')

    # Read HTML content from input.txt file
    html_content = read_html_from_txt(input_file)

    # Extract video information
    video_info_list = extract_video_info_from_html(html_content)

    # Save output in output.json within the same folder
    save_hrefs_to_json(video_info_list, output_file)

    print(f"Content saved to: {output_file}")

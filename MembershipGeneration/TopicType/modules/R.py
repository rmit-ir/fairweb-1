import tarfile
import logging
from bs4 import BeautifulSoup
import re
import spacy
import os
import pandas as pd
import gender_guesser.detector as gender
from collections import Counter
from scholarly import scholarly
import re

from Utilities import get_html_content, write_to_memb_file
nlp = spacy.load("en_core_web_sm")

logging.basicConfig(filename='log_file.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class R:
    def __init__(self):
        self.rGender_memb_file = 'eval.R-GENDER.gmemb'
        self.rHindex_memb_file = 'eval.R-HINDEX.gmemb'

    def get_author_hindex(self, author_name):
        try:
            search_query = scholarly.search_author(author_name)
            first_author_result = next(search_query)
            # Retrieve all the details for the author
            author_text = scholarly.fill(first_author_result)
            hindex = int(author_text['hindex'])
        except:
            hindex = 0

        return hindex

    def extract_text(self, page_content):

        # Remove additional empty spaces using regular expressions
        page_content = re.sub(r'\s+', ' ', page_content)

        # Extract the text between "Content-Length: [some number]"
        match = re.search(r'Content-Length: (\d+)', page_content)

        if match:
            content_length = int(match.group(1))
            start_index = page_content.index(match.group(0)) + len(match.group(0))
            end_index = start_index + content_length
            extracted_text = page_content[start_index:end_index]

        else:
            extracted_text = ' '
            logging.info("Content-Length not found.")

        return extracted_text

    def get_persons(self, page_content):

        extracted_text = self.extract_text(page_content)

        # Extract names from the page
        doc = nlp(extracted_text)
        person_entities = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]

        # Retrieve only first three persons as was done for entity annotations in Pilot

        return person_entities[:3]

    def extract_hindex_membership(self, page_content, target_doc, output_path):
        hindex_1 = 0  # if x < 10
        hindex_2 = 0  # if 10 ≦ x < 30
        hindex_3 = 0  # if 30 ≦ x < 50
        hindex_4 = 0  # if 50 ≦ x

        author_list = self.get_persons(page_content)
        for author_name in author_list:
            hindex = self.get_author_hindex(author_name)
            print(f"{author_name} has an hindex of {hindex}")
            logging.info(f"{author_name} has an hindex of {hindex}")

            if hindex < 10:
                hindex_1 = hindex_1 + 1
            elif (hindex >= 10) and (hindex < 30):
                hindex_2 = hindex_2 + 1
            elif (hindex >= 30) and (hindex < 50):
                hindex_3 = hindex_3 + 1
            elif hindex >= 50:
                hindex_4 = hindex_4 + 1
            else:
                logging.info(f"No valid hindex value extracted from profile for {author_name}")

        data = [target_doc, str(hindex_1), str(hindex_2), str(hindex_3), str(hindex_4)]
        formatted_data = ' '.join(data)

        write_to_memb_file(formatted_data, self.rHindex_memb_file, output_path)

    def extract_gender_membership(self, page_content, target_doc, output_path):

        extracted_text = self.extract_text(page_content)

        # Extract names from the page
        doc = nlp(extracted_text)
        person_entities = [entity.text for entity in doc.ents if entity.label_ == "PERSON"]

        d = gender.Detector()
        gender_list = []
        for entity in person_entities:
            gender_list.append(d.get_gender(entity.split(" ")[0]))

        counts = Counter(gender_list)
        he = counts.get('male', 0)
        she = counts.get('female', 0)
        other = counts.get('andy', 0)

        data = [target_doc, str(he), str(she), str(other)]
        formatted_data = ' '.join(data)

        write_to_memb_file(formatted_data, self.rGender_memb_file, output_path)

    def create_membership(self, doc_id_list, html_files_path, output_path):
        path_prefix = html_files_path.split('.tar.gz')[0]

        try:
            memb_list_rHindex = list(pd.read_csv(output_path + self.rHindex_memb_file, sep=' ', header=None).iloc[:, 0])
        except FileNotFoundError:
            logging.info(f"Initiating memb file {self.rHindex_memb_file}")
            memb_list_rHindex = []

        try:
            memb_list_rGender = list(pd.read_csv(output_path + self.rGender_memb_file, sep=' ', header=None).iloc[:, 0])
        except FileNotFoundError:
            logging.info(f"Initiating memb file {self.rGender_memb_file}")
            memb_list_rGender = []

        for target_doc in doc_id_list:

            if (target_doc not in memb_list_rGender) or (target_doc not in memb_list_rHindex):

                with tarfile.open(html_files_path, 'r:gz') as tar:
                    html_content = get_html_content(path_prefix + '/' + target_doc + '.html', tar)

                    soup = BeautifulSoup(html_content, 'html.parser')
                    title = soup.title.string if soup.title else "No Title Found"
                    url = soup.url
                    page_content = soup.get_text()

                    logging.info(f"Title: {title}")
                    logging.info(f"URL: {url}")

                    if target_doc not in memb_list_rGender:
                        logging.info(f"File '{target_doc}' not processed for {self.rGender_memb_file}...Processing now")
                        self.extract_gender_membership(page_content, target_doc, output_path)

                    if target_doc not in memb_list_rHindex:
                        logging.info(f"File '{target_doc}' not processed for {self.rHindex_memb_file}...Processing now")
                        self.extract_hindex_membership(page_content, target_doc, output_path)
            else:
                logging.info(f"File '{target_doc}' already processed for both {self.rHindex_memb_file} and {self.rGender_memb_file}")



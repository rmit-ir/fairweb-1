import tarfile
import logging
from bs4 import BeautifulSoup
import pandas as pd
from Utilities import get_html_content, write_to_memb_file

logging.basicConfig(filename='log_file.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class M:
    def __init__(self):
        self.mRatings_memb_file = 'eval.M-RATINGS.gmemb'
        self.mOrigin_memb_file = 'eval.M-ORIGIN.gmemb'

    def extract_ratings_membership(self, page_content, target_doc, output_path):
        #print(page_content)



        # TODO Extraction code here and update the variables below accordingly





        rating_1 = 0  # if x < 100
        rating_2 = 0  # if 100 ≦ x < 10K
        rating_3 = 0  # if 10K ≦ x < 1M
        rating_4 = 0  # if 1M ≦ x

        data = [target_doc, str(rating_1), str(rating_2), str(rating_3), str(rating_4)]
        formatted_data = ' '.join(data)

        write_to_memb_file(formatted_data, self.mRatings_memb_file, output_path)

    def extract_origin_membership(self, page_content, target_doc, output_path):
        #print(page_content)



        # TODO Extraction code here and update the dictionary keys accordingly




        origin_dict = {"Africa": 0, "America": 0, "Antarctica": 0, "Asia": 0, "Caribbean": 0, "Europe": 0,
                       "Middle East": 0, "Oceania": 0}

        data = [target_doc, str(origin_dict["Africa"]), str(origin_dict["America"]), str(origin_dict["Antarctica"]),
                str(origin_dict["Asia"]), str(origin_dict["Caribbean"]), str(origin_dict["Europe"]),
                str(origin_dict["Middle East"]), str(origin_dict["Oceania"])]
        formatted_data = ' '.join(data)

        write_to_memb_file(formatted_data, self.mOrigin_memb_file, output_path)

    def create_membership(self, doc_id_list, html_files_path, output_path):
        path_prefix = html_files_path.split('.tar.gz')[0]


        try:
            memb_list_mRatings = list(pd.read_csv(output_path + self.mRatings_memb_file, sep=' ', header=None).iloc[:, 0])
        except FileNotFoundError:
            #logging.info("Initiating memb file")
            memb_list_mRatings = []

        try:
            memb_list_mOrigin = list(pd.read_csv(output_path + self.mOrigin_memb_file, sep=' ', header=None).iloc[:, 0])
        except FileNotFoundError:
            memb_list_mOrigin = []

        for target_doc in doc_id_list:

            if (target_doc not in memb_list_mRatings) or (target_doc not in memb_list_mOrigin):

                with tarfile.open(html_files_path, 'r:gz') as tar:
                    html_content = get_html_content(path_prefix + '/' + target_doc + '.html', tar)

                    # soup = BeautifulSoup(html_content, 'html.parser')
                    # title = soup.title.string if soup.title else "No Title Found"
                    # url = soup.url
                    # page_content = soup.get_text()

                    # TODO either use the html content directly or use the soup object

                    # logging.info(f"Title: {title}")
                    # logging.info(f"URL: {url}")

                    if target_doc not in memb_list_mOrigin:
                        logging.info(f"File '{target_doc}' not processed for {self.mOrigin_memb_file}...Processing now")
                        self.extract_origin_membership(html_content, target_doc, output_path)

                    if target_doc not in memb_list_mRatings:
                        logging.info(f"File '{target_doc}' not processed for {self.mRatings_memb_file}...Processing now")
                        self.extract_ratings_membership(html_content, target_doc, output_path)
            else:
                logging.info(f"File '{target_doc}' already processed for both {self.mRatings_memb_file} and {self.mOrigin_memb_file}")

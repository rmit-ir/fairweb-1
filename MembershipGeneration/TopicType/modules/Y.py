import tarfile
import logging
import pandas as pd
from bs4 import BeautifulSoup
from Utilities import get_html_content, write_to_memb_file

logging.basicConfig(filename='log_file.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class Y:
    def __init__(self):
        self.ySubscs_memb_file = 'eval.Y-SUBSCS.gmemb'

    def extract_subscriber_membership(self, page_content, target_doc, output_path):
        #print(page_content)


        # TODO Extraction code here and update the variables below accordingly



        subsc_1 = 0  # if x < 100
        subsc_2 = 0  # if 100 ≦ x < 10K
        subsc_3 = 0  # if 10K ≦ x < 1M
        subsc_4 = 0  # if 1M ≦ x

        data = [target_doc, str(subsc_1), str(subsc_2), str(subsc_3), str(subsc_4)]
        formatted_data = ' '.join(data)

        write_to_memb_file(formatted_data, self.ySubscs_memb_file, output_path)

    def create_membership(self, doc_id_list, html_files_path, output_path):
        path_prefix = html_files_path.split('.tar.gz')[0]

        try:
            memb_list_ySubscs = list(pd.read_csv(output_path + self.ySubscs_memb_file, sep=' ', header=None).iloc[:, 0])
        except FileNotFoundError:
            logging.info("Initiating memb file")
            memb_list_ySubscs = []

        for target_doc in doc_id_list:
            if target_doc not in memb_list_ySubscs:
                with tarfile.open(html_files_path, 'r:gz') as tar:
                    html_content = get_html_content(path_prefix + '/' + target_doc + '.html', tar)

                    soup = BeautifulSoup(html_content, 'html.parser')
                    title = soup.title.string if soup.title else "No Title Found"
                    url = soup.url
                    page_content = soup.get_text()

                    logging.info(f"Title: {title}")
                    logging.info(f"URL: {url}")

                    self.extract_subscriber_membership(page_content, target_doc, output_path)
            else:
                logging.info(f"File '{target_doc}' already processed for {self.ySubscs_memb_file}")

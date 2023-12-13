import yaml
import pandas as pd
import logging
from TopicType.TopicFactory import TopicFactory
from multiprocessing import Pool
import multiprocessing
from functools import partial
import os
import time

logging.basicConfig(filename='log_file.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def process_topic(df, html_files_path, output_path, topic):
    print(topic)
    logging.info(f"Processing for Topic: {topic}")
    doc_id_list = list(df[df['topic_id'] == topic]['doc_id'])
    topicTypeMembershipGen_obj = TopicFactory(topic).create_topic_type_extraction()
    topicTypeMembershipGen_obj.create_membership(doc_id_list, html_files_path, output_path)


if __name__ == '__main__':
    os.chdir('.')

    # Load data from YAML file
    with open("config.yaml", 'r') as stream:
        config = yaml.safe_load(stream)

    run_path = config['run_path']
    run_file = config['run_file']
    html_files_path = config['html_files_path']
    output_path = config['output_path']
    n_cores = config['n_cores']

    run_name = run_file.split('.txt')[0]

    df = pd.read_csv(run_path + run_file, sep=' ', header=None)
    df.columns = ['topic_id', 'Q0', 'doc_id', 'rank', 'score', 'system']

    topics_list = list(df['topic_id'].unique())

    #topics_list = ["R001"]
    #print(topics_list)
    # for topic in topics_list:
    #     process_topic(df, html_files_path, output_path, topic)

    start_time = time.time()  # Start measuring runtime

    # create a multiprocessing Pool
    pool = Pool(n_cores)

    # create partial function to fix df, html_files_path, and output_path arguments
    process_topic_partial = partial(process_topic, df, html_files_path, output_path)

    # process each topic in the topics_list in parallel
    pool.map(process_topic_partial, topics_list)

    # close the pool and wait for the work to finish
    pool.close()
    pool.join()

    end_time = time.time()  # Stop measuring runtime
    runtime = end_time - start_time
    logging.info(f"Runtime {run_file}: {runtime} seconds")



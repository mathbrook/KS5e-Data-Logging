from folder_selection_utils import select_folder_and_get_path
from download_latest_dbc_from_releases import download_latest_release
from parser_api import *
import sys
import argparse
import subprocess
import parser_logger, logging
sys.path.insert(1, "../telemetry_parsers")
########################################################################
# Entry Point to Framework
########################################################################


def main(args):
    logging.info("Welcome to KSU motorsports parser")
    logging.info("The process will be of two parts: CSV to CSV parsing, and then CSV to MAT parsing.")
    dbc_found = False
    dbc_files_folder_good = True
    if args.getdbc:
        logging.info("Downloading latest dbc")
        download_latest_release()
        
    logging.info("Looking for dbc-files folder: ")
    while not dbc_found:
        if not os.path.exists("dbc-files") or dbc_files_folder_good == False:
            logging.error("'dbc-files' folder was not found or failed to load dbcs.")
            logging.error("please select the folder with dbc files to use for parsing...")
            while True:
                try:
                    dbc_files_path = select_folder_and_get_path()
                except:
                    logging.critical("could not open tkinter prompt to select folder")
                    logging.critical("please get your dbc files in 'dbc-files' then try to run the program again")
                    break
                for file_name in os.listdir(dbc_files_path):
                    if file_name.endswith(".dbc"):
                        logging.info(f"Found DBC file: {file_name}")
                        dbc_found = True
                dbc_file = get_dbc_files(dbc_files_path)
                if dbc_found and dbc_file is not None:
                    break
                else:
                    logging.error(f"No DBCs found in {dbc_files_path}")
                    logging.error("Please select another folder...")

        elif os.path.exists("dbc-files") and dbc_files_folder_good:
            logging.info("dbc-files folder found")
            dbc_files_path = ('dbc-files')

            dbc_file = get_dbc_files(dbc_files_path)
            if dbc_file is not None:
                break
            elif dbc_file is None:
                dbc_files_folder_good = False

    logging.info("Beginning CSV to CSV parsing...")
    parsing_folder_path=None
    if  not args.test:
        logging.info("Select a folder which contains the raw logs to be parsed")
        try:
            parsing_folder_path = select_folder_and_get_path()
        except:
            logging.critical("could not open tkinter prompt to select folder")
    elif args.test:
        logging.info(f"Setting path to test due to 'test' arg being true: {args.test}")
        parsing_folder_path='./test'
    try:
        parse_folder(parsing_folder_path, dbc_file=dbc_file)
    except (TypeError,FileNotFoundError) as e:
        logging.critical(f"Error ({e}) when trying to parse folder {parsing_folder_path} :(")
    logging.info("Finished CSV to CSV parsing.")
    logging.info("Beginning CSV to MAT parsing...")
    create_mat()
    logging.info("Finished CSV to MAT parsing.")
    logging.info("SUCCESS: Parsing Complete.")
    time.sleep(3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='KSU Motorsports parser! \nThese args configure how the parser is run')
    parser.add_argument('--getdbc' ,type=bool, help='True if you want to download the latest dbc.')
    parser.add_argument('--test', type=bool,help='"True" will make the parser target the "test" directory for folders')
    args = parser.parse_args()
    main(args)

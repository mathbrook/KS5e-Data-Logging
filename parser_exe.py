from folder_selection_utils import select_folder_and_get_path,select_folder_and_get_path_dbc
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
            logging.warning("'dbc-files' folder was not found or failed to load dbcs.")
            logging.info("please select the folder with dbc files to use for parsing...")
            while True:
                try:
                    dbc_files_path = select_folder_and_get_path_dbc()
                except:
                    logging.error("could not open tkinter prompt to select folder")
                    logging.error("please get your dbc files in 'dbc-files' then try to run the program again")
                    break
                for file_name in os.listdir(dbc_files_path):
                    if file_name.endswith(".dbc"):
                        logging.info(f"Found DBC file: {file_name}")
                        dbc_found = True
                if dbc_files_path is not None:
                    dbc_file = get_dbc_files(dbc_files_path)
                elif dbc_files_path is None:
                    logging.warning(f"selected path was {dbc_files_path}, which means you exited or cancelled the prompt")
                    logging.warning("exiting the program in 3 secs ! byebye")
                    time.sleep(3)
                    sys.exit()
                if dbc_found and dbc_file is not None:
                    break
                else:
                    logging.warning(f"No DBCs found in {dbc_files_path}")
                    logging.warning("Please select another folder...")

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
            logging.error("could not open tkinter prompt to select folder")
    elif args.test:
        # 'test' folder includes a csv with a bit of meaningful data in it so we can test parsing against it
        # TODO: long term, host a batch of example csvs, and download them rather than storing here
        logging.info(f"Setting path to test due to 'test' arg being true: {args.test}")
        parsing_folder_path='./test'
    try:
        parse_folder(parsing_folder_path, dbc_file=dbc_file)
        logging.info("Finished CSV to CSV parsing.")
    except (TypeError,FileNotFoundError) as e:
        logging.error(f"Error ({type(e)}-{e}) when trying to parse folder {parsing_folder_path} :(")
        logging.warning("Parsing folder step failed")
    logging.info("Beginning CSV to MAT parsing...")
    create_mat_success = create_mat()
    if create_mat_success:
        logging.info("Finished CSV to MAT parsing.")
    elif not create_mat_success:
        logging.warning("CSV to MAT parsing step failed")
        
    logging.info("Parsing Complete.")
    logging.info('Program exiting in 3 seconds...')
    time.sleep(3)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='KSU Motorsports parser! \nThese args configure how the parser is run')
    parser.add_argument('--getdbc',action="store_true" , help='include this flag if you want to download the latest dbc.')
    parser.add_argument('--test',action="store_true",help='including this flag will make the parser target the "test" directory for folders')
    parser.add_argument('--gui',action="store_true",help="this flag will make the parser run in gui mode (NOT YET IMPLEMENTED)")
    parser.add_argument('-v','--verbose',action="store_true",help="will show debug prints (this will spam your console but show more info)")
    args = parser.parse_args()
    parser_logger.setup_logger(args.verbose)
    main(args)

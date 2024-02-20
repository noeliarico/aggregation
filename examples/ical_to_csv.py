from csv_ical import Convert

from ranking_aggregation.disk_operations.disk_operations import get_disk_path

path_folder = f"{get_disk_path()}/"


convert = Convert()

convert.CSV_FILE_LOCATION = f"{path_folder}manadine.csv"
convert.SAVE_LOCATION = f"{path_folder}manadine.ics"

convert.read_ical(convert.SAVE_LOCATION)
convert.make_csv()
convert.save_csv(convert.CSV_FILE_LOCATION)

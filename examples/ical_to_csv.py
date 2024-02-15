from csv_ical import Convert
convert = Convert()
convert.CSV_FILE_LOCATION = '/Users/noeliarico/Downloads/manadine.csv'
convert.SAVE_LOCATION = '/Users/noeliarico/Downloads/manadine.ics'
convert.read_ical(convert.SAVE_LOCATION)
convert.make_csv()
convert.save_csv(convert.CSV_FILE_LOCATION)
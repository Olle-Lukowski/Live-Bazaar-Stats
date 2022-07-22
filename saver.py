import time
import json
import os


class DataSaver:
    def __init__(self, file_name):
        self.file_name = file_name
        # create the file if it doesn't exist
        if not os.path.exists(file_name):
            with open(file_name, 'w') as f:
                json.dump({}, f)

        self.time_stamp = time.time()

    def save(self, data):
        self.time_stamp = time.time()
        with open(self.file_name, 'r+') as f:
            # dump the data to the file with the time stamp as the key
            old_data = json.load(f)
            # empty the file
            f.seek(0)
            f.truncate()

            old_data[str(self.time_stamp)] = data
            json.dump(old_data, f)

    def load(self):
        with open(self.file_name) as f:
            return json.load(f)

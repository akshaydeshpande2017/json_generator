import unittest
from csv_parser import json_generator
import json
import constants
import io


class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.maxDiff = None

    def test_positive(self):
        json_parsed_data = json_generator()
        json_obj = json.dumps(json_parsed_data, indent=4)
        with open(constants.test_destination_file, "w") as outfile:
            outfile.write(json_obj)
        self.assertListEqual(
            list(
                io.open(constants.test_destination_file)
            ), list(
                io.open("test_reference_data_generator.json")
            )
        )


if __name__ == "__main__":
    unittest.main()

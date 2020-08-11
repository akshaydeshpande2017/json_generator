import csv
import re
import constants
import json
import logging


def json_generator():
    """
    This function parses the csv, and converts the parsed csv into a json format.
    :return: An array of json data.
    """
    tree_source_list = []
    logging.info("Reading .csv file %s" % constants.source_file)
    with open(constants.source_file, newline="") as cf:
        reader = csv.DictReader(cf)
        for row in reader:
            logging.info("Reading row %s" % json.dumps(row))
            element_index = parse_column_for_row(row)
            if not element_index:
                continue
            data = {
                "label": row[constants.level + str(element_index) + constants.name],
                "id": row[constants.level + str(element_index) + constants.level_id],
                "link": row[constants.level + str(element_index) + constants.url],
                "children": []
            }
            level_list = data["link"].split(row["Base URL"] + "/")[1].split("/")
            if len(level_list) == 1:
                tree_source_list.append(data)
            elif len(level_list) > 1:
                parse_tree(level_list, tree_source_list, data)
            logging.info("tree_source_list %s" % json.dumps(tree_source_list))
    return tree_source_list


def parse_tree(level_list, tree_source_list, data):
    """
    It parses the tree, and appends the children node to respective parent node.
    :param level_list: It it the list of node ID's.
    :param tree_source_list: JSON formatted list to store the final result
    :param data: Child Node data dictionary
    :return: Updated tree_source_list
    """
    if len(level_list) == 1:
        return tree_source_list.append(data)
    else:
        for level in tree_source_list:
            if level["id"] == level_list[0]:
                parse_tree(level_list[1:], level["children"], data)


def parse_column_for_row(row):
    """
    It checks how many levels are there in the csv data file.
    :param row: Respective row of the csv file.
    :return: A level list indicating the number of levels.
    """
    levels = []
    r = re.compile(constants.level_regex_pattern)
    for column in row:
        match_obj = r.search(column)
        if match_obj and row[constants.level + str(match_obj.group()) + constants.url]:
            if match_obj.group() not in levels:
                levels.append(match_obj.group())
    return len(levels)


if __name__ == "__main__":
    logging.basicConfig(
        filename=constants.log_file,
        filemode="w",
        format='%(asctime)s - %(message)s',
        level=logging.INFO
    )
    logging.info("Started Executing csv_parser")
    json_parsed_data = json_generator()
    json_obj = json.dumps(json_parsed_data, indent=4)
    logging.info("Writing output file is %s" % constants.destination_file)
    with open(constants.destination_file, "w") as outfile:
        outfile.write(json_obj)
    logging.info("----------Code Execution Ended Successfully----------")

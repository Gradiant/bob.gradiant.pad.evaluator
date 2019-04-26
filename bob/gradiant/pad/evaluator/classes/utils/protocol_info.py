from tabulate import tabulate


def get_protocol_info(dict_pipeline_features, name_db, protocol):

    table = []
    database_row = [name_db, protocol, len(dict_pipeline_features['Train']['features']),
                    len(dict_pipeline_features['Dev']['features']),
                    len(dict_pipeline_features['Test']['features'])]
    table.append(database_row)

    headers = ["Database", "Protocol", "Train samples", "Dev samples", "Test Samples"]

    return tabulate(table, headers)


def save_protocol_info(filename, protocol_info_txt):
    with open(filename, "w") as f:
        f.write(protocol_info_txt)
        f.close()
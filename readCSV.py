import csv


def read_csv_file(file_path, dictionary):
    with open(file_path, newline='') as csv_file:
        reader = csv.reader(csv_file)
        points_list = []
        finalized_list = []
        next(reader)
        next(reader)
        for row in reader:
            points_list.append(row)
        for i in points_list:
            finalized_list.append(prepare_points_list(i, dictionary['site_id']))
    return finalized_list


def determine_point_type(point):
    if point.find('AI') != -1:
        return 'AI'
    elif point.find('AO') != -1:
        return 'AO'
    elif point.find('BI') != -1:
        return 'BI'
    elif point.find('BO') != -1:
        return 'BO'
    elif point.find('AV') != -1:
        return 'AV'
    elif point.find('BV') != -1:
        return 'BV'
    else:
        print("Unrecognized point type.")


def prepare_points_list(pl, device_id):
    # (DEV_ID, Object_Identifier, Object_Name, Type_Reference)
    test_list = []
    start_list = []
    pl.pop()
    start_list.append(pl)
    for i in start_list:
        object_name = i[2]
        object_identifier = i[0] + i[1]
        point_type = determine_point_type(object_identifier)
        if point_type == 'AI':
            type_reference = 'AIC' + i[3]
        elif point_type == 'AO':
            type_reference = 'AOC' + i[3]
        elif point_type == 'BI' or point_type == 'BO':
            type_reference = 'BDC' + i[3]
        inter_list = [device_id, object_identifier, object_name, type_reference]
        test_list.append(inter_list)
    return inter_list


if __name__ == '__main__':
    raw_points_list = read_csv_file()
    print(raw_points_list)
    point_type = determine_point_type(raw_points_list[0][1])
    print(point_type)

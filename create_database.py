import logging
import readCSV
from deltaconnection import make_connection
from datetime import datetime
from ahu_variables import AhuVariables


class CreateDatabase:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.information_dictionary = {}
        self.gather_information()

    def create_points(self):
        file_path = self.information_dictionary['file_path']
        time = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
        logging.basicConfig(filename='app.log', filemode='a', format='%(levelname)s - %(message)s')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.info(f"***************Points creation started for site {self.information_dictionary['site_id']}. "
                    f"{time}***************")
        # Create points
        points_list = readCSV.read_csv_file(file_path, self.information_dictionary)
        sql_list = []
        # Loop thru points list and execute sql statements
        for row in range(len(points_list)):
            try:
                point = readCSV.determine_point_type(points_list[row][1])
                sql_list = points_list[row]
                if sql_list[0] != '' and (
                        point == "AO" or point == "AI" or point == "BO" or point == "BI"):
                    sql = f"INSERT INTO OBJECT_V4_{point} (DEV_ID, Object_Identifier, Object_Name, Type_Reference, " \
                          f"SITE_ID) VALUES ({self.information_dictionary['device_id']},'{sql_list[1]}','{sql_list[2]}'" \
                          f",'{sql_list[3]}', '{self.information_dictionary['site_id']}') "
                    make_connection(sql)
                    logger.info(f"\tDevice: {self.information_dictionary['device_id']}"
                                f"\n\tPoint Instance: {sql_list[1]}"
                                f"\n\tPoint Name: {sql_list[2]}"
                                f"\n\tType Reference: {sql_list[3]}"
                                f"\n\tSite: {self.information_dictionary['site_id']}"
                                f"\n******************************")
                else:
                    sql_list.pop()
                    sql = f"INSERT INTO OBJECT_V4_{point} (DEV_ID, Object_Identifier, Object_Name, SITE_ID) " \
                          f"VALUES ({sql_list[0]},'{sql_list[1]}','{sql_list[2]}', " \
                          f"'{self.information_dictionary['site_id']}') "
                    make_connection(sql)
                    logger.info(sql_list)
            except:
                logger.info(f'\n\t!!!!!Failed to create {sql_list[1]} ,{sql_list[2]}!!!!!')


    def create_variables(self):
        if self.information_dictionary['system_type'] == 'AHU':
            logging.basicConfig(filename='app.log', filemode='a', format='%(levelname)s - %(message)s')
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            logger.info(f"----------AHU System Variables selected----------")
            ahu_vars = AhuVariables(setup_info=self.information_dictionary)
            ahu_vars.create_analog_variables()
            ahu_vars.create_binary_variable()
            ahu_vars.create_mics()
            ahu_vars.create_multistate_variables()
        elif self.information_dictionary['system_type'] == 'Chilled Water System':
            logging.basicConfig(filename='app.log', filemode='a', format='%(levelname)s - %(message)s')
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            logger.info(f"----------Chilled Water System Variables selected----------")
        elif self.information_dictionary['system_type'] == 'Hot Water System':
            logging.basicConfig(filename='app.log', filemode='a', format='%(levelname)s - %(message)s')
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            logger.info(f"----------Hot Water System Variables selected----------")
        else:
            logging.basicConfig(filename='app.log', filemode='a', format='%(levelname)s - %(message)s')
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            logger.info(f"----------No System Variable type selected----------")

    def gather_information(self):
        db_dict = {}
        for key, value in self.kwargs.items():
            db_dict[key] = value
        self.information_dictionary = db_dict

import logging
from datetime import datetime
from deltaconnection import make_connection, fetch_points


class ViewDatabase:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.information_dictionary = {}
        self.gather_information()
        self.sql_queries = [
            f"SELECT DEV_ID, Object_Identifier, Object_Name FROM OBJECT_V4_AI WHERE DEV_ID = "
            f"{self.information_dictionary['device_id']} and SITE_ID = '{self.information_dictionary['site_id']}'",
            f"SELECT DEV_ID, Object_Identifier, Object_Name FROM OBJECT_V4_AO WHERE DEV_ID = "
            f"{self.information_dictionary['device_id']} and SITE_ID = '{self.information_dictionary['site_id']}'",
            f"SELECT DEV_ID, Object_Identifier, Object_Name FROM OBJECT_V4_BI WHERE DEV_ID = "
            f"{self.information_dictionary['device_id']} and SITE_ID = '{self.information_dictionary['site_id']}'",
            f"SELECT DEV_ID, Object_Identifier, Object_Name FROM OBJECT_V4_BO WHERE DEV_ID = "
            f"{self.information_dictionary['device_id']} and SITE_ID = '{self.information_dictionary['site_id']}'",
            f"SELECT DEV_ID, Object_Identifier, Object_Name FROM OBJECT_V4_AV WHERE DEV_ID = "
            f"{self.information_dictionary['device_id']} and SITE_ID = '{self.information_dictionary['site_id']}'",
            f"SELECT DEV_ID, Object_Identifier, Object_Name FROM OBJECT_V4_BV WHERE DEV_ID = "
            f"{self.information_dictionary['device_id']} and SITE_ID = '{self.information_dictionary['site_id']}'",
            f"SELECT DEV_ID, Object_Identifier, Object_Name FROM OBJECT_V4_AIC WHERE DEV_ID = "
            f"{self.information_dictionary['device_id']} and SITE_ID = '{self.information_dictionary['site_id']}'",
            f"SELECT DEV_ID, Object_Identifier, Object_Name FROM OBJECT_V4_AOC WHERE DEV_ID = "
            f"{self.information_dictionary['device_id']} and SITE_ID = '{self.information_dictionary['site_id']}'",
            f"SELECT DEV_ID, Object_Identifier, Object_Name FROM OBJECT_V4_BDC WHERE DEV_ID = "
            f"{self.information_dictionary['device_id']} and SITE_ID = '{self.information_dictionary['site_id']}'"
        ]

    def view_controller_points(self):
        result = []
        list_of_tuples = []
        logging.basicConfig(filename='app.log', filemode='a', format='%(levelname)s - %(message)s')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        if self.information_dictionary['site_id'] != '':
            time = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
            logger.info(f"***************Points Query for site: {self.information_dictionary['site_id']} "
                        f"{time}***************")
            for i in range(len(self.sql_queries)):
                result.append(fetch_points(self.sql_queries[i]))
        for i in result:
            for j in i:
                logger.info(f"\tDevice: {j[0]}"
                            f"\n\tPoint Instance: {j[1]}"
                            f"\n\tPoint Name: {j[2]}"
                            f"\n\tSite: {self.information_dictionary['site_id']}"
                            f"\n******************************")

    def gather_information(self):
        db_dict = {}
        for key, value in self.kwargs.items():
            db_dict[key] = value
        self.information_dictionary = db_dict

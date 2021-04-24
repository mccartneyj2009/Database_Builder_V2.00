import delta_initial_actions
import os
import sys

from PyQt5 import QtWidgets

from create_database import CreateDatabase
from query_controller import ViewDatabase
from database_builder import Ui_DatabaseBuilder
from open_file_dialog import open_fd


def open_driver():
    os.startfile('C:\Windows\SysWOW64\odbcad32.exe')


def start_creation():
    site_id = ui.siteNameDropDown.currentText()
    device_id = ui.bacnetAddressInput.text()
    file_path = ui.filePath.text()
    system_type = ui.systemTypeDropDown.currentText()
    analog_variables = ui.analogVariablesCheckBox.checkState()
    binary_variables = ui.binaryVariablesCheckBox.checkState()
    alarms = ui.alarmsCheckBox.checkState()
    trend_logs = ui.trendlogsCheckBox.checkState()
    programs = ui.programsCheckBox.checkState()
    control_loops = ui.controlLoopsCheckBox.checkState()
    multistate_variables = ui.multistateVariablesCheckBox.checkState()

    # Validate if there are no System Type Variables are selected from the drop down
    if system_type == '':
        no_st_selected_popup = QtWidgets.QMessageBox()
        no_st_selected_popup.setIcon(QtWidgets.QMessageBox.Information)
        no_st_selected_popup.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        no_st_selected_popup.setWindowTitle('Database Builder')
        no_st_selected_popup.setText('No System Type was selected from the drop down. Continue?')
        cont = no_st_selected_popup.exec()
        if cont == QtWidgets.QMessageBox.Yes:
            pass
        else:
            return 0

    # check if device_id is appropriate
    try:
        device_id = int(device_id)
        while True:
            if 1 / device_id > 0:
                if isinstance(device_id, int):
                    break
            else:
                device_id / 0
    except ValueError:
        not_an_int_popup = QtWidgets.QMessageBox()
        not_an_int_popup.setIcon(QtWidgets.QMessageBox.Critical)
        not_an_int_popup.setWindowTitle('Database Builder')
        not_an_int_popup.setText('BACnet Address needs to be an integer.')
        not_an_int_popup.exec_()
        return 0
    except ZeroDivisionError:
        zero_popup = QtWidgets.QMessageBox()
        zero_popup.setIcon(QtWidgets.QMessageBox.Critical)
        zero_popup.setWindowTitle('Database Builder')
        zero_popup.setText('BACnet Address needs to be an integer greater than 0.')
        zero_popup.exec_()
        return 0

    # Check if there is a valid file path
    if file_path == '...':
        no_file_selected_popup = QtWidgets.QMessageBox()
        no_file_selected_popup.setIcon(QtWidgets.QMessageBox.Critical)
        no_file_selected_popup.setWindowTitle('Database Builder')
        no_file_selected_popup.setText('No file has been selected.')
        no_file_selected_popup.exec_()
        return 0
    else:
        db = CreateDatabase(site_id=site_id, device_id=device_id, system_type=system_type,
                            analog_variables=analog_variables, binary_variables=binary_variables,
                            multistate_variables=multistate_variables, alarms=alarms, trend_logs=trend_logs,
                            programs=programs, control_loops=control_loops, file_path=file_path)

    # Check for a site ID
    if site_id != '':
        points_created_flag = db.create_points()
        if points_created_flag == 0:
            pass
        else:
            db.create_variables()
            # Open log file for feedback. Should there be two logs? an immediate feedback and a historical one?
            os.startfile('app.log')
    else:
        no_site_selected_popup = QtWidgets.QMessageBox()
        no_site_selected_popup.setIcon(QtWidgets.QMessageBox.Critical)
        no_site_selected_popup.setWindowTitle('Database Builder')
        no_site_selected_popup.setText('No site has been selected.')
        no_site_selected_popup.exec_()
        return 0


def get_file_name():
    file_path = open_fd()
    if file_path.find('.csv') == -1:
        wrong_file_type_popup = QtWidgets.QMessageBox()
        wrong_file_type_popup.setIcon(QtWidgets.QMessageBox.Critical)
        wrong_file_type_popup.setWindowTitle('Database Builder')
        wrong_file_type_popup.setText('Incorrect file type. File must be .csv file format.')
        wrong_file_type_popup.exec_()
        return 0
    if file_path != '':
        ui.filePath.setText(file_path)
        return file_path
    else:
        return ''


def query_controller():
    site_id = ui.siteNameDropDown.currentText()
    device_id = ui.bacnetAddressInput.text()
    controller_query = ViewDatabase(site_id=site_id, device_id=device_id)

    # check if device_id is appropriate
    try:
        device_id = int(device_id)
        while True:
            if 1 / device_id > 0:
                if isinstance(device_id, int):
                    break
            else:
                device_id / 0
    except ValueError:
        not_an_int_popup = QtWidgets.QMessageBox()
        not_an_int_popup.setIcon(QtWidgets.QMessageBox.Critical)
        not_an_int_popup.setWindowTitle('Database Builder')
        not_an_int_popup.setText('BACnet Address needs to be an integer.')
        not_an_int_popup.exec_()
        return 0
    except ZeroDivisionError:
        zero_popup = QtWidgets.QMessageBox()
        zero_popup.setIcon(QtWidgets.QMessageBox.Critical)
        zero_popup.setWindowTitle('Database Builder')
        zero_popup.setText('BACnet Address needs to be an integer greater than 0.')
        zero_popup.exec_()
        return 0

    # Check for a site ID
    if site_id != '':
        controller_query.view_controller_points()
        os.startfile('app.log')
    else:
        no_site_selected_popup = QtWidgets.QMessageBox()
        no_site_selected_popup.setIcon(QtWidgets.QMessageBox.Critical)
        no_site_selected_popup.setWindowTitle('Database Builder')
        no_site_selected_popup.setText('No site has been selected.')
        no_site_selected_popup.exec_()
        return 0
    pass


if __name__ == "__main__":
    # create and initialize main app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QDialog()
    ui = Ui_DatabaseBuilder()
    ui.setupUi(MainWindow)

    dsn_source_valid = delta_initial_actions.verify_dsn_source()
    if not dsn_source_valid:  # dsn source not existing
        popup = QtWidgets.QMessageBox()
        popup.setIcon(QtWidgets.QMessageBox.Critical)
        popup.setWindowTitle('Database Builder')
        popup.setText('Invalid DSN Source.')
        popup.exec_()
    else:
        ui.siteNameDropDown.addItems(delta_initial_actions.query_for_sites())  # Get sites from ODBC driver
        systems = ['', 'AHU', 'Chilled Water System', 'Hot Water System']
        ui.systemTypeDropDown.addItems(systems)  # Populate systems combobox
        # Buttons
        ui.openFileBtn.clicked.connect(get_file_name)
        ui.createDatabaseBtn.clicked.connect(start_creation)
        ui.viewControllerBtn.clicked.connect(query_controller)
        ui.openDSNBtn.clicked.connect(open_driver)
        ui.closeBtn.clicked.connect(sys.exit)
        MainWindow.show()
        sys.exit(app.exec_())

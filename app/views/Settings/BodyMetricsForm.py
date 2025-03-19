from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QComboBox, QMessageBox, QLineEdit, QVBoxLayout, QLabel, QHBoxLayout, QDialog
)

from app.controllers.NavigationController import NavigationController
from app.controllers.StorageManager import StorageManager
from app.enums.storage import StorageKey
from app.utils import style_h2
from app.views.CustomDialog import CustomDialog
from app.views.Divider import Divider
from app.views.FormInput import FormInput


class BodyMetricsForm(QWidget):
    def __init__(self, nav_controller: NavigationController):
        super().__init__()
        regex = QRegExp("^-?\d+([.,]\d+)?$")
        validator = QRegExpValidator(regex)

        self.nav_controller = nav_controller
        
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.header = QHBoxLayout()
        self.header.setContentsMargins(20, 10, 20, 10)
        self.header.setSpacing(10)

        self.title = QLabel("Body Metrics")
        style_h2(self.title)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setStyleSheet("color: red;")
        self.reset_btn.clicked.connect(self.__reset)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.submit_data)

        self.header.addWidget(self.title, stretch=1)
        self.header.addWidget(self.reset_btn)
        self.header.addWidget(self.save_btn)


        self.layout.addLayout(self.header)
        self.layout.addWidget(Divider())

        self.form = QVBoxLayout()
        self.form.setContentsMargins(20, 15, 20, 15)
        self.form.setSpacing(10)

        # Age input
        self.age_input = FormInput(
            title="Age",
            initial_text=StorageManager.get_value(StorageKey.Age.value, "")
        )
        self.age_input.input.setValidator(validator)
        self.form.addWidget(self.age_input)

        # Height input
        self.height_input = FormInput(
            title="Height",
            initial_text=StorageManager.get_value(StorageKey.Height.value, "")
        )
        self.height_input.input.setValidator(validator)
        self.form.addWidget(self.height_input)

        # Current weight input
        self.current_weight_input = FormInput(
            title="Current Weight",
            initial_text=StorageManager.get_value(StorageKey.CurrentWeight.value, "")
        )
        self.current_weight_input.input.setValidator(validator)
        self.form.addWidget(self.current_weight_input)

        # Sex selection
        self.sex_selector = QComboBox()
        self.sex_selector.addItems(["Female", "Male"])
        self.sex_selector.setToolTip("Select your sex")
        self.sex_selector.setCurrentText(StorageManager.get_value(StorageKey.Sex.value, "Female"))
        self.form.addWidget(self.sex_selector)

        self.layout.addLayout(self.form)

        # Set the layout for the widget
        self.setLayout(self.layout)

    def __validate_data(self, data):
        """
        Validate the collected form data to ensure it is properly formatted.

        Args:
            data (dict): The form data to validate.

        Returns:
            bool: True if the data is valid, False otherwise.
        """
        try:
            # Validate numeric fields
            int(data["age"])  # Age must be a valid integer
            float(data["height"])  # Height must be a valid number
            float(data["current_weight"])  # Current weight must be a valid number
        except ValueError:
            # Show an error message for invalid numeric entries
            QMessageBox.warning(self, "Validation Error",
                                "Please enter valid numeric values for age, height, and weight.")
            return False

        return True

    def __reset(self):
        dialog = CustomDialog(
            "Would you like to reset your body metrics?",
            "",
            "Clear"
        )

        if dialog.exec_() == QDialog.Accepted:
            StorageManager.set_value(StorageKey.Age.value, "")
            StorageManager.set_value(StorageKey.Height.value, "")
            StorageManager.set_value(StorageKey.CurrentWeight.value, "")
            self.nav_controller.reload()

    def submit_data(self):
        """
        Collect, validate, and save the form data. Notify the submit callback as required.
        """
        # Gather data from input fields
        form_data = {
            "age": self.age_input.text.strip(),
            "height": self.height_input.text.strip(),
            "current_weight": self.current_weight_input.text.strip(),
            "sex": self.sex_selector.currentText(),
        }

        # Validate the collected data
        if not self.__validate_data(form_data):
            return  # Stop execution if the data is invalid

        # Save data using StorageManager
        StorageManager.set_value(StorageKey.Age.value, form_data["age"])
        StorageManager.set_value(StorageKey.Height.value, form_data["height"])
        StorageManager.set_value(StorageKey.CurrentWeight.value, form_data["current_weight"])
        StorageManager.set_value(StorageKey.Sex.value, form_data["sex"])

        # Sync the settings to make sure the data is stored
        StorageManager.sync()

        # Show a success message
        QMessageBox.information(self, "Success", "Your body metrics have been saved successfully.")


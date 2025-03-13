from PyQt5.QtWidgets import (
    QWidget, QPushButton, QComboBox, QMessageBox, QLineEdit
)

from app.controllers.StorageManager import StorageManager
from app.enums.storage import StorageKey


class BodyMetricsForm(QWidget):
    def __init__(self):
        super().__init__()

        # Age input
        self.age_input = QLineEdit()
        self.age_input.setPlaceholderText("Enter Age")
        self.layout.addWidget(self.age_input)

        # Height input
        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Enter Height (cm)")
        self.layout.addWidget(self.height_input)

        # Current weight input
        self.current_weight_input = QLineEdit()
        self.current_weight_input.setPlaceholderText("Enter Current Weight (kg)")
        self.layout.addWidget(self.current_weight_input)

        # Sex selection
        self.sex_selector = QComboBox()
        self.sex_selector.addItems(["Female", "Male"])
        self.sex_selector.setToolTip("Select your sex")
        self.layout.addWidget(self.sex_selector)

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.submit_data)
        self.layout.addWidget(self.save_button)

        # Set the layout for the widget
        self.setLayout(self.layout)

        # Load previously saved data (if any) from StorageManager
        self.__load_data()

    def __load_data(self):
        """
        Load saved body metrics from storage and populate the form fields.
        """
        # Get values from StorageManager and set them in the fields
        self.age_input.setText(StorageManager.get_value(StorageKey.Age.value, ""))
        self.height_input.setText(StorageManager.get_value(StorageKey.Height.value, ""))
        self.current_weight_input.setText(StorageManager.get_value(StorageKey.CurrentWeight.value, ""))
        self.sex_selector.setCurrentText(StorageManager.get_value(StorageKey.Sex.value, "Female"))

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

    def submit_data(self):
        """
        Collect, validate, and save the form data. Notify the submit callback as required.
        """
        # Gather data from input fields
        form_data = {
            "age": self.age_input.text().strip(),
            "height": self.height_input.text().strip(),
            "current_weight": self.current_weight_input.text().strip(),
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


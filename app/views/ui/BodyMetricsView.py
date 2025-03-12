from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QComboBox, QMessageBox, QLineEdit
)

from app.controllers.StorageManager import StorageManager



class BodyMetricsForm(QWidget):
    def __init__(self, submit_callback):
        super().__init__()

        # Store the callback function for submission events
        self.submit_callback = submit_callback

        # Create the main layout for the form
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(60, 15, 60, 15)

        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Name")
        self.layout.addWidget(self.name_input)

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

        # Goal weight input
        self.goal_weight_input = QLineEdit()
        self.goal_weight_input.setPlaceholderText("Enter Goal Weight (kg)")
        self.layout.addWidget(self.goal_weight_input)

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
        self.load_data()

    def load_data(self):
        """
        Load saved body metrics from storage and populate the form fields.
        """
        # Get values from StorageManager and set them in the fields
        self.name_input.setText(StorageManager.get_value("body_metrics/name", ""))
        self.age_input.setText(StorageManager.get_value("body_metrics/age", ""))
        self.height_input.setText(StorageManager.get_value("body_metrics/height", ""))
        self.current_weight_input.setText(StorageManager.get_value("body_metrics/current_weight", ""))
        self.goal_weight_input.setText(StorageManager.get_value("body_metrics/goal_weight", ""))
        self.sex_selector.setCurrentText(StorageManager.get_value("body_metrics/sex", "Female"))

    def validate_data(self, data):
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
            float(data["goal_weight"])  # Goal weight must be a valid number
        except ValueError:
            # Show an error message for invalid numeric entries
            QMessageBox.warning(self, "Validation Error",
                                "Please enter valid numeric values for age, height, and weights.")
            return False

        # Check if the name field is not empty
        if not data["name"]:
            QMessageBox.warning(self, "Validation Error", "Name cannot be empty.")
            return False

        return True

    def submit_data(self):
        """
        Collect, validate, and save the form data. Notify the submit callback as required.
        """
        # Gather data from input fields
        form_data = {
            "name": self.name_input.text().strip(),
            "age": self.age_input.text().strip(),
            "height": self.height_input.text().strip(),
            "current_weight": self.current_weight_input.text().strip(),
            "goal_weight": self.goal_weight_input.text().strip(),
            "sex": self.sex_selector.currentText(),
        }

        # Validate the collected data
        if not self.validate_data(form_data):
            return  # Stop execution if the data is invalid

        # Save data using StorageManager
        for key, value in form_data.items():
            StorageManager.set_value(f"body_metrics/{key}", value)

        # Sync the settings to make sure the data is stored
        StorageManager.sync()

        # Show a success message
        QMessageBox.information(self, "Success", "Your body metrics have been saved successfully.")

        # Execute the callback function with the form data
        self.submit_callback(form_data)

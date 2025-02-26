from typing import Any

from PyQt5.QtCore import QSettings

class StorageManager:
    # Static property to hold the QSettings instance
    _settings = None

    @staticmethod
    def initialize(organization_name: str, application_name: str):
        """
        Initialize the static QSettings instance with the organization and application names.

        Args:
            organization_name: The name of the organization.
            application_name: The name of the application.
        """
        StorageManager._settings = QSettings(organization_name, application_name)

    @staticmethod
    def set_value(key: str, value: Any):
        """
        Set the value for a specific key in the settings.

        Args:
            key: The key for the setting.
            value: The value to be stored.
        """
        if StorageManager._settings is None:
            raise ValueError("SettingsManager is not initialized. Call initialize() first.")

        StorageManager._settings.setValue(key, value)

    @staticmethod
    def get_value(key: str, default_value=None):
        """
        Get the value for a specific key from the settings.

        Args:
            key: The key for the setting.
            default_value: The default value to return if the key does not exist.

        Returns:
            QVariant: The value associated with the key, or the default value if the key does not exist.
        """
        if StorageManager._settings is None:
            raise ValueError("SettingsManager is not initialized. Call initialize() first.")

        return StorageManager._settings.value(key, default_value)

    @staticmethod
    def remove_value(key: str):
        """
        Remove the value for a specific key from the settings.

        Args:
            key: The key for the setting to be removed.
        """
        if StorageManager._settings is None:
            raise ValueError("SettingsManager is not initialized. Call initialize() first.")

        StorageManager._settings.remove(key)

    @staticmethod
    def sync():
        """
        Synchronize the settings to ensure all changes are written to disk.
        """
        if StorageManager._settings is None:
            raise ValueError("SettingsManager is not initialized. Call initialize() first.")

        StorageManager._settings.sync()


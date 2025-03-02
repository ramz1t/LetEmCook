from typing import Callable
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QScrollArea, QSpacerItem
from app.enums.route import Route

class NavigationController:
    """
    A navigation controller that manages page routes and history for backwards navigation.
    """
    def __init__(self, container: QWidget):
        # The container where pages are displayed
        self.container = container
        self.__setup_container()

        # A mapping of route keys to factory functions
        self.__registry: dict[any, Callable] = {}
        # A history stack for backwards navigation
        self.__history: list[tuple[Route, dict]] = []

    def __setup_container(self):
        """
        Set up the container layout and scroll area.
        """
        # Assuring that container layout exists
        if self.container.layout() is None:
            self.container.setLayout(QVBoxLayout())

        # Set the container layout to expand fully
        self.container.layout().setContentsMargins(0, 0, 0, 0)
        self.container.layout().setSpacing(0)

        # Create a QScrollArea to hold pages
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName("contentScrollArea")
        self.scroll_area.setWidgetResizable(False)
        self.scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Fill width and height
        self.scroll_area.setStyleSheet("#contentScrollArea { border: none; }")
        self.container.layout().addWidget(self.scroll_area)
        self.container.layout().setStretchFactor(self.scroll_area, 1)  # Ensures scroll area takes full space

    def register_route(self, route: Route, factory_function: Callable) -> None:
        """
        Register a route with a factory function.
        The factory function should accept any needed kwargs and return a QWidget.
        :param route: The route to register.
        :param factory_function: The factory function for view to register.
        """
        self.__registry[route] = factory_function

    def navigate(self, route: Route, **kwargs) -> None:
        """
        Creates a new page by looking up the route's factory, clears the container,
        and adds the new page.
        :param route: The route to navigate.
        :param kwargs: Route factory arguments.
        """
        # Get view factory from registry
        factory = self.__registry.get(route)
        if factory:
            # Update router history
            self.__push_history(route, kwargs)

            # Build new page
            new_page = factory(nav_controller=self, **kwargs)
            self.__set_page(new_page)
        else:
            print(f"Unknown route: {route}")

    def reload(self):
        """
        Reloads the current page
        """
        if self.__history:
            route, kwargs = self.__history[-1]
            factory = self.__registry.get(route)
            new_page = factory(nav_controller=self, **kwargs)
            self.__set_page(new_page)
        else:
            print("No current page to reload")

    def __set_page(self, new_page: QWidget):
        """
        Set the new page in the scroll area.
        :param new_page: The new page widget to display.
        """
        # Create a wrapper widget
        page_wrapper = QWidget()
        wrapper_layout = QVBoxLayout()
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)

        # Ensure new_page takes full width
        new_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        wrapper_layout.addWidget(new_page)
        wrapper_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))  # Push content up
        page_wrapper.setLayout(wrapper_layout)

        # Configure the wrapper to take full width and appropriate height
        page_wrapper.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        page_wrapper.setMinimumHeight(new_page.sizeHint().height())
        page_wrapper.setMinimumWidth(self.scroll_area.viewport().width())  # Match scroll area width

        # Set the wrapper as the scroll area's widget
        self.scroll_area.setWidget(page_wrapper)

    def pop_route(self) -> None:
        """
        Navigate to the previous route in the navigation history.
        """
        if len(self.__history) > 1:
            # Remove current Route
            self.__history.pop()
            # Get last Route (the one before current)
            route, kwargs = self.__history[-1]
            self.navigate(route, **kwargs)
        else:
            print("Can't pop root route")

    def __push_history(self, route: Route, kwargs: dict) -> None:
        """
        Updates history for backwards navigation.
        :param route: Route user is redirected to.
        :param kwargs: Kwargs used in view builder
        """
        if self.__history:
            last_route, last_kwargs = self.__history[-1]
            if last_route == route and last_kwargs == kwargs:
                return
        self.__history.append((route, kwargs))

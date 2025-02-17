from typing import Callable

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy

from app.enums.route import Route


class NavigationController:
    """
    A navigation controller that manages page routes and history for backwards navigation.
    """
    def __init__(self, container: QWidget):
        # The container where pages are displayed
        self.container = container

        # Assuring that container layout exists
        if self.container.layout() is None:
            self.container.setLayout(QVBoxLayout())

        # A mapping of route keys to factory functions
        self.__registry: dict[any, Callable] = {}
        # A history stack for backwards navigation
        self.__history: list[tuple[Route, dict]] = []

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

            # Clear the container
            layout = self.container.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            layout.addWidget(new_page)

            # Add spacer to push content up
            spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            layout.addSpacerItem(spacer)
        else:
            print(f"Unknown route: {route}")

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

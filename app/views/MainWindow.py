from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QHBoxLayout

from app.controllers.NavigationController import NavigationController
from app.controllers.StorageManager import StorageManager
from app.enums.route import Route
from app.views.Divider import Divider
from app.views.Sidebar import Sidebar
from app.views.factories import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        WIDTH = 1100
        HEIGHT = 700

        self.setWindowTitle("Let'EmCook")

        self.setGeometry(100, 100, WIDTH, HEIGHT)
        self.setMaximumSize(WIDTH, HEIGHT)
        self.setMinimumSize(WIDTH, HEIGHT)

        StorageManager.initialize("HKR", "LetEmCook")

        # Create central widget and main layout
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Area where all pages will be shown
        self.content_container = QWidget()
        self.content_container.setLayout(QVBoxLayout())
        self.content_container.layout().setContentsMargins(0, 0, 0, 0)
        self.content_container.layout().setSpacing(0)

        nav_controller = NavigationController(self.content_container)

        # Register app routes here
        nav_controller.register_route(Route.HOME, home_page_factory)
        nav_controller.register_route(Route.RECIPES, recipes_page_factory)
        nav_controller.register_route(Route.RECIPE_DETAIL, recipe_detail_page_factory)
        nav_controller.register_route(Route.RECIPE_EDIT, recipe_edit_page_factory)
        nav_controller.register_route(Route.RECIPE_CREATE, recipe_create_page_factory)
        nav_controller.register_route(Route.NOTES, notes_page_factory)
        nav_controller.register_route(Route.NOTE_DETAIL, note_detail_page_factory)
        nav_controller.register_route(Route.NOTE_EDIT, note_edit_page_factory)
        nav_controller.register_route(Route.NOTE_CREATE, note_create_page_factory)
        nav_controller.register_route(Route.RECOMMENDATIONS, recommended_recipes_page_factory)
        self.nav_controller = nav_controller

        self.sidebar = Sidebar(self.nav_controller)

        layout.addWidget(self.sidebar, 0)
        layout.addWidget(Divider(vertical=True))
        layout.addWidget(self.content_container, 1)

        self.setCentralWidget(container)

        # Set initial page
        self.nav_controller.navigate(Route.HOME)

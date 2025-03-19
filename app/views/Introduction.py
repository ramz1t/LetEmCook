from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy

from app.views.Divider import Divider


class Introduction(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(8, 60, 0, 30)
        main_layout.setSpacing(15)

        # Welcome Text
        welcome_label = QLabel('<p style="text-align: center; font-size: 30px;"><b>Welcome to</b></p>')
        main_layout.addWidget(welcome_label)

        app_name_label = QLabel('<p style="text-align: center; font-size: 60px;"><b>Let\'EmCook</b></p>')
        app_name_label.setContentsMargins(0,0,0,40)
        main_layout.addWidget(app_name_label)

        # Description Text
        description_label = QLabel(
            '<p style="font-size: 15px; text-align: center;">'
            'The goal of this app is to help you manage your diet so you can keep a better track of the nutrients and calories you eat to make you feel better.'
            '</p>'
        )
        main_layout.addWidget(description_label)

        main_layout.addWidget(Divider())

        # Features Text
        features_label = QLabel(
            '<p style="font-size: 15px;">'
            '<b>|RECIPES|</b>: Here you can create, edit and delete your recipes.<br>'
            '<b>|NOTES|</b>: Create any notes you need, talk about your recipes, how they make you feel, or experiences you have.<br>'
            '<b>|PLANNER|</b>: Get meal suggestions based on your activity to reach a recommended calorie level.<br>'
            '<b>|SETTINGS|</b>: Do not forget to update your body metrics and age as time goes by!'
            '</p>'
        )
        features_label.setWordWrap(True)
        main_layout.addWidget(features_label)
        main_layout.addWidget(Divider())

        # Remember Text
        remember_label = QLabel(
            '<p style="font-size: 15px;">'
            '<b>Remember:</b>'
            '<ul style="padding-left: 0;">'
            '<li>Having enough energy helps you stay on track with your routine. Carbohydrates offer a stable energy source while sugars may cause a fluctuation in energy levels.</li>'
            '<li>Foods rich in tryptophan (turkey, bananas, dairy) help produce serotonin, the "happiness hormone."</li>'
            '<li>Stress and Anxiety Reduction: Omega-3 fatty acids (fish, nuts) and antioxidants (fruits, vegetables) can help lower stress and improve emotional well-being.</li>'
            '<li>Tracking your mood and your feelings with recipes will help you achieve the diet you need to confront everyday plans. Looking back at your notes can give you valuable insights to improve your diet and well-being.</li>'
            '</ul>'
            '</p>'
        )
        remember_label.setWordWrap(True)
        main_layout.addWidget(remember_label)
        main_layout.addWidget(Divider())

        # Creators Text
        creators_label = QLabel(
            '<p style="font-size: 15px;"><b>This app has been created by:</b>'
            '<ul style="padding-left: 0;">'
            '<li><a href="https://github.com/ramz1t">Timur Ramazanov</a> (main repository)</li>'
            '<li><a href="https://github.com/ayahassaad">Ayah Assaad</a></li>'
            '<li><a href="https://github.com/skgmsj">Sebastian Karström</a></li>'
            '<li><a href="https://github.com/mavagoncalves">Maria Valentina Gonçalves Rojas</a></li>'
            '<li><a href="https://github.com/robrodres">Roberto Rodríguez Espejo</a></li>'
            '</ul>'
            '</p>'
        )
        creators_label.setOpenExternalLinks(True)
        creators_label.setWordWrap(True)
        main_layout.addWidget(creators_label)

        self.setLayout(main_layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
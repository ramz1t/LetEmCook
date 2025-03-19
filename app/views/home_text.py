from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QSizePolicy


def home_text():
    # Some parts have &nbsp; to make it match the left margin after a line jump.
    introduction = QLabel('''
    <div style="margin-left: 15px;">
    <br>
    <br>
    <p style="text-align: center; font-size: 30px;">
    <b>Welcome to 
    </p>
    <p style="text-align: center; font-size: 60px;">
    <b>Let'EmCook</b>
    </p>
    <br>
    <p style="font-size: 15px;">The goal of this app is to help you manage your diet so you can keep a better track of the nutrients and calories you eat to make you feel better.</p>

    <hr>
    <p style="font-size: 15px;">
    <b>|RECIPES|</b>: Here you can create, edit and delete your recipes.<br>
    <b>|NOTES|</b>: Create any notes you need, talk about your recipes, how they make you feel, or experiences you have.<br>
    <b>|PLANNER|</b>: Get meal suggestions based on your activity to reach a recommended calorie level.<br>
    <b>|SETTINGS|</b>: Do not forget to update your body metrics and age as time goes by!<br>
    </p>
    <hr>

    <p style="font-size: 15px;">
    <b>Remember:</b><br>
    - Having enough energy helps you stay on track with your routine. Carbohydrates offer a stable energy source while sugars may cause a &nbsp; &nbsp; fluctuation in energy levels.<br>
    - Foods rich in tryptophan (turkey, bananas, dairy) help produce serotonin, the "happiness hormone."<br>
    - Stress and Anxiety Reduction: Omega-3 fatty acids (fish, nuts) and antioxidants (fruits, vegetables) can help lower stress and improve &nbsp; &nbsp; &nbsp; emotional well-being.<br>
    - Tracking your mood and your feelings with recipes will help you achieve the diet you need to confront everyday plans. Looking back at &nbsp; &nbsp; &nbsp; &nbsp; your notes can give you valuable insights to improve your diet and well-being.<br>
    </p>
    <hr>
    <p style="font-size: 15px;"><b>This app has been created by:</b>
    <ul>
        <li><a href="https://github.com/ramz1t">Timur Ramazanov</a> (main repository)</li>
        <li><a href="https://github.com/ayahassaad">Ayah Assaad</a></li>
        <li><a href="https://github.com/skgmsj">Sebastian Karström</a></li>
        <li><a href="https://github.com/mavagoncalves">Maria Valentina Gonçalves Rojas</a></li>
        <li><a href="https://github.com/robrodres">Roberto Rodríguez Espejo</a></li>
    </ul>
    </p>
    <br>
    </div>
    ''')

    # Makes url's clickable
    introduction.setOpenExternalLinks(True)
    # Cuts the lines when they reach the edge
    introduction.setWordWrap(True)
    # Forces the text to extend to the specified width, otherwise will cut shorter
    introduction.setFixedWidth(930)

    return introduction
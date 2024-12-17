# interface.py
from PyQt6 import QtCore, QtWidgets
import sys
import labyrinthe
import threading

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Bouton de génération
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 70, 75, 23))
        self.pushButton.setObjectName("pushButton")

        # SpinBox pour x et y
        self.spinBox = QtWidgets.QSpinBox(parent=self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(40, 70, 42, 22))
        self.spinBox.setMinimum(5)
        self.spinBox.setMaximum(10000000)

        self.spinBox_2 = QtWidgets.QSpinBox(parent=self.centralwidget)
        self.spinBox_2.setGeometry(QtCore.QRect(110, 70, 42, 22))
        self.spinBox_2.setMinimum(5)
        self.spinBox_2.setMaximum(10000000)

        # Labels
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 50, 47, 14))
        self.label.setText("x")

        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(110, 50, 47, 14))
        self.label_2.setText("y")

        # Barre de progression
        self.progressBar = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 140, 411, 23))
        self.progressBar.setValue(0)
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Connecter le bouton pour lancer la génération
        self.pushButton.clicked.connect(self.start_generation)

    def start_generation(self):
        # Réinitialiser la barre de progression
        self.progressBar.setValue(0)
        
        # Récupérer les valeurs des SpinBoxes
        x = self.spinBox.value()
        y = self.spinBox_2.value()
        
        # Lancer la génération dans un thread
        threading.Thread(target=self.generate_maze, args=(x, y)).start()

    def generate_maze(self, x, y):
        grille = labyrinthe.creer_grille(x, y)
        
        # Fonction de rappel pour la progression
        def update_progress(value):
            # Utilisation de invokeMethod pour forcer la mise à jour de la barre de progression dans le thread principal
            QtCore.QMetaObject.invokeMethod(self.progressBar, "setValue", QtCore.Qt.ConnectionType.QueuedConnection, QtCore.Q_ARG(int, value))

        # Passer la fonction de mise à jour à la génération
        labyrinthe.generer_labyrinthe_parfait(grille, 1, 1, progress_callback=update_progress)
        
        # Sauvegarde après génération
        labyrinthe.sauvegarder_labyrinthe(grille, "labyrinthe_parfait.txt")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())

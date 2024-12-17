import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QVBoxLayout, QWidget
from multiprocessing import Process
import affichage_du_labirinthe  # Importer l'autre fichier pour démarrer l'affichage

class LabyrintheSelectionApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sélection de labyrinthe")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # Bouton pour ouvrir le fichier de labyrinthe
        self.select_file_button = QPushButton("Ouvrir un labyrinthe", self)
        self.select_file_button.clicked.connect(self.open_file_dialog)
        layout.addWidget(self.select_file_button)

        # Étiquette pour afficher le chemin du fichier sélectionné
        self.file_path_label = QLabel("Aucun fichier sélectionné", self)
        layout.addWidget(self.file_path_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_file_dialog(self):
        # Ouvrir une boîte de dialogue pour sélectionner un fichier texte
        file_path, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier de labyrinthe", "", "Text Files (*.txt)")
        
        if file_path:
            self.file_path_label.setText(f"Fichier sélectionné : {file_path}")
            self.launch_labyrinthe_display(file_path)

    def launch_labyrinthe_display(self, file_path):
        # Lancer l'affichage du labyrinthe dans un processus enfant
        p = Process(target=affichage_du_labirinthe.afficher_labyrinthe_process, args=(file_path,))
        p.start()

# Exécution de l'application PyQt
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LabyrintheSelectionApp()
    window.show()
    sys.exit(app.exec_())

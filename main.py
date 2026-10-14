import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QFileDialog, QMessageBox, QCheckBox, QLineEdit

class Analyser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_path = ""
        self.individualLines = []
        self.classified = []
        self.searchKey = ""
        height = 950
        width = 1500
        self.setWindowTitle("Log Analyser")
        self.setGeometry(200, 200, width, height)
        self.setFixedSize(width, height)
        self.initUI()

    def initUI(self):
        self.loadButton = QPushButton("Load", self)
        self.loadButton.setGeometry(10, 10, 100, 50)
        self.loadButton.setStyleSheet("font-size: 25px;background-color: darkgray;")
        self.loadButton.clicked.connect(self.open)

        self.exportButton = QPushButton("Export", self)
        self.exportButton.setGeometry(120, 10, 100, 50)
        self.exportButton.setStyleSheet("font-size: 25px;background-color: darkgray;")
        self.exportButton.clicked.connect(self.export)

        self.clearButton = QPushButton("clear", self)
        self.clearButton.setGeometry(230, 10, 100, 50)
        self.clearButton.setStyleSheet("font-size: 25px;background-color: darkgray;")
        self.clearButton.clicked.connect(self.clear)

        self.filterLabel = QLabel("Select filters:", self)
        self.filterLabel.setGeometry(450, 10, 100, 50)
        self.filterLabel.setStyleSheet("font-size: 15px;")

        self.errorCheckBox = QCheckBox("ERRORS", self)
        self.errorCheckBox.setGeometry(560, 10, 100, 50)
        self.errorCheckBox.setChecked(True)
        self.errorCheckBox.setEnabled(False)
        self.errorCheckBox.stateChanged.connect(self.updateLog)

        self.warningCheckBox = QCheckBox("WARNINGS", self)
        self.warningCheckBox.setGeometry(660, 10, 100, 50)
        self.warningCheckBox.setChecked(True)
        self.warningCheckBox.setEnabled(False)
        self.warningCheckBox.stateChanged.connect(self.updateLog)

        self.infoCheckBox = QCheckBox("INFO", self)
        self.infoCheckBox.setGeometry(780, 10, 100, 50)
        self.infoCheckBox.setChecked(True)
        self.infoCheckBox.setEnabled(False)
        self.infoCheckBox.stateChanged.connect(self.updateLog)

        self.otherCheckBox = QCheckBox("OTHER", self)
        self.otherCheckBox.setGeometry(860, 10, 100, 50)
        self.otherCheckBox.setChecked(True)
        self.otherCheckBox.setEnabled(False)
        self.otherCheckBox.stateChanged.connect(self.updateLog)

        self.searchTextBox = QLineEdit(self)
        self.searchTextBox.setPlaceholderText("Search for keyword")
        self.searchTextBox.setGeometry(940, 10, 150, 50)
        self.searchTextBox.setText("")
        self.searchTextBox.setEnabled(False)
        self.searchTextBox.textChanged.connect(self.searchUpdate)

        self.analysedLog = QTextEdit(self)
        self.analysedLog.setGeometry(10, 70, 1480, 870)
        self.analysedLog.setReadOnly(True)

    def open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open a log file", "", "Text Files (*.txt);;Log Files (*.log)")
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as file:
                readContent = file.readlines()
        except FileNotFoundError:
            QMessageBox.critical(self, "ERROR", "File not found.")
            return
        except PermissionError:
            QMessageBox.critical(self, "ERROR", "File permission denied.")
            return
        except UnicodeDecodeError:
            QMessageBox.critical(self, "ERROR", "Incorrect file encoding.")
            return
        self.file_path = path
        self.individualLines = [f"Line {n} --> {text}" for n, text in enumerate(readContent, start=1)]
        self.setWindowTitle(f"Log Analyser - {self.file_path}")
        self.calculateMatches()
        self.errorCheckBox.setEnabled(True)
        self.warningCheckBox.setEnabled(True)
        self.infoCheckBox.setEnabled(True)
        self.otherCheckBox.setEnabled(True)
        self.searchTextBox.setEnabled(True)
        self.updateLog()

    def export(self):
        if self.file_path != "":
            try:
                self.save_path, _ = QFileDialog.getSaveFileName(self, "Choose an export directory", "exported_log.txt", "Text Files (*.txt);;Log Files (*.log)")
                if self.save_path:
                    with open(self.save_path, 'w', encoding='utf-8') as saved:
                        saved.write(self.analysedLog.toPlainText())
                    QMessageBox.information(self, "Export", "Export finished successfully!")
            except PermissionError:
                QMessageBox.critical(self, "ERROR", "You don’t have permission to write in this directory!")
        elif not self.file_path:
            QMessageBox.critical(self, "ERROR", "No file to export, import a new file first!")

    def clear(self):
        self.file_path = ""
        self.individualLines = []
        self.classified = []
        self.errorCheckBox.setEnabled(False)
        self.warningCheckBox.setEnabled(False)
        self.infoCheckBox.setEnabled(False)
        self.otherCheckBox.setEnabled(False)
        self.analysedLog.clear()
        self.searchTextBox.clear()
        self.searchTextBox.setEnabled(False)
        self.setWindowTitle("Log Analyser")

    def calculateMatches(self):
        self.classified = []
        for line in self.individualLines:
            low = line.lower()
            self.classified.append((line, "error" in low, "warning" in low, "info" in low))


    def searchUpdate(self):
        self.searchKey = self.searchTextBox.text().strip()
        self.updateLog()

    def updateLog(self):
        showError = self.errorCheckBox.isChecked()
        showWarning = self.warningCheckBox.isChecked()
        showInfo = self.infoCheckBox.isChecked()
        showOther = self.otherCheckBox.isChecked()
        pattern = re.compile(re.escape(self.searchKey), re.IGNORECASE) if self.searchKey else None

        result = []
        for line, isError, isWarning, isInfo in self.classified:
            isOther = not (isError or isWarning or isInfo)
            if ((isError and showError) or (isWarning and showWarning) or
                    (isInfo and showInfo) or (isOther and showOther)):
                if pattern is None or pattern.search(line):
                    result.append(line)
        self.analysedLog.setPlainText("".join(result))
            
def main():
    app = QApplication(sys.argv)
    window = Analyser()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
import sys
import csv
import os
from PyQt6 import QtWidgets
from gui import Ui_MainWindow

class GradesApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.attemptsEdit.textChanged.connect(self.update_score_fields)
        self.ui.pushButton.clicked.connect(self.submit)
        self.csv_file = "grades.csv"
        self._ensure_csv_header()

    def _ensure_csv_header(self):
        """
	Create CSV with a descriptive header if it doesn't exist.
	"""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Student Name",
                    "Attempt 1 Score",
                    "Attempt 2 Score",
                    "Attempt 3 Score",
                    "Attempt 4 Score",
                    "Final Grade" ])

    def update_score_fields(self):
        """
	Show exactly N score fields (and hide the rest).
	"""
        text = self.ui.attemptsEdit.text()
        try:
            n = int(text)
        except ValueError:
            n = 0

        for lbl, edt in zip(self.ui.scoreLabels, self.ui.scoreEdits):
            lbl.hide()
            edt.hide()

        if 1 <= n <= 4:
            for i in range(n):
                self.ui.scoreLabels[i].show()
                self.ui.scoreEdits[i].show()

    def submit(self):
        """
	Validate inputs, write to CSV, clear UI, and show feedback.
	"""
        name = self.ui.nameEdit.text().strip()
        if not name:
            return self._show_message("Name cannot be empty.", error=True)

        try:
            attempts = int(self.ui.attemptsEdit.text())
            if not (1 <= attempts <= 4):
                raise ValueError
        except ValueError:
            return self._show_message("Attempts must be an integer between 1 and 4.", error=True)

        scores = []
        for i in range(attempts):
            txt = self.ui.scoreEdits[i].text()
            try:
                val = float(txt)
                if not (0 <= val <= 100):
                    raise ValueError
            except ValueError:
                return self._show_message(f"Score {i+1} must be a number between 0 and 100.", error=True)
            scores.append(val)

        padded = scores.copy()
        while len(padded) < 4:
            padded.append("N/A")

        final_grade = max(scores)

        with open(self.csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, *padded, final_grade])

        self.ui.nameEdit.clear()
        self.ui.attemptsEdit.clear()
        for edt in self.ui.scoreEdits:
            edt.clear()
        self.update_score_fields()

        self._show_message("Submitted.", error=False)

    def _show_message(self, text: str, error: bool):
        """
	Display message red (error) or green (success).
	"""
        self.ui.resultLabel.setText(text)
        color = "red" if error else "green"
        self.ui.resultLabel.setStyleSheet(f"color: {color};")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GradesApp()
    window.show()
    sys.exit(app.exec())


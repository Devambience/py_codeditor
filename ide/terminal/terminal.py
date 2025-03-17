"""
Terminal component for PyIDE
"""

import os
import sys
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QFont

class Terminal(QTextEdit):
    """Terminal for executing commands and displaying output"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(False)
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.onReadyReadStandardOutput)
        self.process.readyReadStandardError.connect(self.onReadyReadStandardError)
        self.setStyleSheet("QTextEdit { background-color: #1E1E1E; color: #EEEEEE; }")
        self.setupFont()
        self.current_dir = os.getcwd()
        self.prompt = f"{self.current_dir}> "
        self.appendPlainText(self.prompt)
        
    def setupFont(self):
        """Set up terminal font"""
        font = QFont("Consolas", 10)
        font.setFixedPitch(True)
        self.setFont(font)
        
    def keyPressEvent(self, event):
        """Handle key presses in the terminal"""
        if event.key() == Qt.Key.Key_Return:
            command = self.toPlainText().split(self.prompt)[-1].strip()
            if command:
                self.execute(command)
            else:
                self.appendPlainText(self.prompt)
        else:
            super().keyPressEvent(event)
            
    def appendPlainText(self, text):
        """Append text to the terminal"""
        self.append(text)
            
    def execute(self, command):
        """Execute a command in the terminal"""
        if command.startswith("cd "):
            # Handle cd command internally
            path = command[3:].strip()
            try:
                os.chdir(path)
                self.current_dir = os.getcwd()
                self.prompt = f"{self.current_dir}> "
                self.appendPlainText(self.prompt)
            except Exception as e:
                self.appendPlainText(str(e))
                self.appendPlainText(self.prompt)
        else:
            # Execute other commands using QProcess
            self.process.setWorkingDirectory(self.current_dir)
            if sys.platform == "win32":
                self.process.start("cmd.exe", ["/c", command])
            else:
                self.process.start("/bin/bash", ["-c", command])
            
    def onReadyReadStandardOutput(self):
        """Handle standard output from the process"""
        output = self.process.readAllStandardOutput().data().decode('utf-8')
        self.appendPlainText(output)
        self.appendPlainText(self.prompt)
        
    def onReadyReadStandardError(self):
        """Handle standard error from the process"""
        error = self.process.readAllStandardError().data().decode('utf-8')
        self.appendPlainText(error)
        self.appendPlainText(self.prompt)

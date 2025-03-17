"""
Code Editor component for PyIDE
"""

from PyQt6.QtWidgets import QPlainTextEdit, QTextEdit
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class CodeEditor(QPlainTextEdit):
    """Code editor with syntax highlighting and line numbering"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.setupFont()
        self.setupLineNumbers()
        self.tab_size = 4
        self.updateTabSize()
        
    def setupFont(self):
        """Set up the editor font"""
        # Set a monospace font
        font = QFont("Consolas", 10)
        font.setFixedPitch(True)
        self.setFont(font)
        
    def setupLineNumbers(self):
        """Set up editor styling"""
        self.setStyleSheet("QPlainTextEdit { background-color: #272822; color: #F8F8F2; }")
        
    def updateTabSize(self):
        """Configure tab size"""
        # Configure tab size
        metrics = self.fontMetrics()
        self.setTabStopDistance(self.tab_size * metrics.horizontalAdvance(' '))
        
    def keyPressEvent(self, event):
        """Handle special key presses"""
        # Handle special key presses
        if event.key() == Qt.Key.Key_Tab:
            self.insertPlainText(" " * self.tab_size)
        else:
            super().keyPressEvent(event)
            
    def highlightCurrentLine(self):
        """Highlight the line where the cursor is"""
        extraSelections = []
        selection = QTextEdit.ExtraSelection()
        lineColor = QColor("#2F2F2F")
        selection.format.setBackground(lineColor)
        selection.format.setProperty(QTextEdit.ExtraSelectionProperty.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

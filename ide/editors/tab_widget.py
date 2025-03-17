"""
Editor tabs component for PyIDE
"""

import os
from PyQt6.QtWidgets import QTabWidget, QMessageBox

from .code_editor import CodeEditor

class TabWidget(QTabWidget):
    """Tab widget for managing multiple open files"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.closeTab)
        self.open_files = {}
        
    def closeTab(self, index):
        """Close a tab and clean up resources"""
        widget = self.widget(index)
        if widget:
            self.removeTab(index)
            file_path = self.tabToolTip(index)
            if file_path in self.open_files:
                del self.open_files[file_path]
    
    def openFile(self, file_path):
        """Open a file in a new tab or focus existing tab if already open"""
        if file_path in self.open_files:
            self.setCurrentIndex(self.indexOf(self.open_files[file_path]))
        else:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                editor = CodeEditor()
                editor.setPlainText(content)
                
                # Try to set syntax highlighting based on file extension
                try:
                    # Import here to avoid circular imports
                    import pygments
                    from pygments.lexers import get_lexer_for_filename
                    from pygments.formatters import HtmlFormatter
                    from pygments import highlight
                    
                    lexer = get_lexer_for_filename(file_path)
                    formatter = HtmlFormatter()
                    highlighted_content = highlight(content, lexer, formatter)
                    editor.setHtml(highlighted_content)
                except Exception:
                    # If highlighting fails, just use plain text
                    editor.setPlainText(content)
                
                file_name = os.path.basename(file_path)
                index = self.addTab(editor, file_name)
                self.setTabToolTip(index, file_path)
                self.open_files[file_path] = editor
                self.setCurrentIndex(index)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")

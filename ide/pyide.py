"""
PyIDE Main Window Class
"""

import os
import json
import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QSplitter,
                           QDockWidget, QStatusBar, QFileDialog, QMessageBox)
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt

from .editors.code_editor import CodeEditor
from .editors.tab_widget import TabWidget
from .views.file_system_view import FileSystemView
from .terminal.terminal import Terminal

class PyIDE(QMainWindow):
    """Main IDE window class"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyIDE")
        self.setMinimumSize(1000, 600)
        self.settings_file = os.path.join(os.path.expanduser("~"), ".pyide", "settings.json")
        self.setupUi()
        self.loadSettings()
        
    def setupUi(self):
        """Set up the user interface"""
        # Main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for main area
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create file system view
        self.file_system_dock = QDockWidget("Explorer", self)
        self.file_system_view = FileSystemView(self)
        self.file_system_dock.setWidget(self.file_system_view)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.file_system_dock)
        
        # Create editor area
        self.editor_tabs = TabWidget(self)
        self.main_splitter.addWidget(self.editor_tabs)
        
        # Create terminal
        self.terminal_dock = QDockWidget("Terminal", self)
        self.terminal = Terminal(self)
        self.terminal_dock.setWidget(self.terminal)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.terminal_dock)
        
        # Set up main layout
        main_layout.addWidget(self.main_splitter)
        
        # Create menu bar
        self.setupMenuBar()
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
    def setupMenuBar(self):
        """Set up the menu bar and actions"""
        # Menu bar
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        # New file action
        new_action = QAction("New File", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.newFile)
        file_menu.addAction(new_action)
        
        # Open file action
        open_action = QAction("Open File", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.openFile)
        file_menu.addAction(open_action)
        
        # Open folder action
        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.openFolder)
        file_menu.addAction(open_folder_action)
        
        file_menu.addSeparator()
        
        # Save action
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.saveFile)
        file_menu.addAction(save_action)
        
        # Save as action
        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.saveFileAs)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.openSettings)
        file_menu.addAction(settings_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        # Undo action
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        # Redo action
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Cut action
        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)
        
        # Copy action
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        # Paste action
        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        # Select all action
        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.selectAll)
        edit_menu.addAction(select_all_action)
        
        # View menu
        view_menu = menu_bar.addMenu("View")
        
        # Toggle file explorer action
        toggle_explorer_action = QAction("Toggle Explorer", self)
        toggle_explorer_action.setShortcut(QKeySequence("Ctrl+B"))
        toggle_explorer_action.triggered.connect(self.toggleExplorer)
        view_menu.addAction(toggle_explorer_action)
        
        # Toggle terminal action
        toggle_terminal_action = QAction("Toggle Terminal", self)
        toggle_terminal_action.setShortcut(QKeySequence("Ctrl+`"))
        toggle_terminal_action.triggered.connect(self.toggleTerminal)
        view_menu.addAction(toggle_terminal_action)
        
        # Run menu
        run_menu = menu_bar.addMenu("Run")
        
        # Run file action
        run_file_action = QAction("Run Current File", self)
        run_file_action.setShortcut(QKeySequence("F5"))
        run_file_action.triggered.connect(self.runCurrentFile)
        run_menu.addAction(run_file_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        
        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.showAbout)
        help_menu.addAction(about_action)
    
    def newFile(self):
        """Create a new empty file"""
        editor = CodeEditor()
        index = self.editor_tabs.addTab(editor, "Untitled")
        self.editor_tabs.setCurrentIndex(index)
        self.statusBar.showMessage("New file created")
    
    def openFile(self, path=None):
        """Open a file from disk"""
        if not path:
            path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*)")
        
        if path:
            self.editor_tabs.openFile(path)
            self.statusBar.showMessage(f"Opened {path}")
    
    def openFolder(self):
        """Open a folder in the file explorer"""
        folder_path = QFileDialog.getExistingDirectory(self, "Open Folder", "")
        if folder_path:
            self.file_system_view.setRootIndex(self.file_system_view.model.index(folder_path))
            self.statusBar.showMessage(f"Opened folder: {folder_path}")
    
    def saveFile(self):
        """Save the current file"""
        current_tab = self.editor_tabs.currentIndex()
        if current_tab == -1:
            return
        
        file_path = self.editor_tabs.tabToolTip(current_tab)
        if not file_path or file_path == "":
            self.saveFileAs()
            return
        
        editor = self.editor_tabs.widget(current_tab)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(editor.toPlainText())
            self.statusBar.showMessage(f"Saved {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
    
    def saveFileAs(self):
        """Save the current file with a new name"""
        current_tab = self.editor_tabs.currentIndex()
        if current_tab == -1:
            return
        
        editor = self.editor_tabs.widget(current_tab)
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File As", "", "All Files (*)")
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(editor.toPlainText())
                
                # Update tab information
                self.editor_tabs.setTabText(current_tab, os.path.basename(file_path))
                self.editor_tabs.setTabToolTip(current_tab, file_path)
                self.editor_tabs.open_files[file_path] = editor
                
                self.statusBar.showMessage(f"Saved as {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
    
    def undo(self):
        """Undo the last action"""
        if self.editor_tabs.currentWidget():
            self.editor_tabs.currentWidget().undo()
    
    def redo(self):
        """Redo the last undone action"""
        if self.editor_tabs.currentWidget():
            self.editor_tabs.currentWidget().redo()
    
    def cut(self):
        """Cut the selected text"""
        if self.editor_tabs.currentWidget():
            self.editor_tabs.currentWidget().cut()
    
    def copy(self):
        """Copy the selected text"""
        if self.editor_tabs.currentWidget():
            self.editor_tabs.currentWidget().copy()
    
    def paste(self):
        """Paste from clipboard"""
        if self.editor_tabs.currentWidget():
            self.editor_tabs.currentWidget().paste()
    
    def selectAll(self):
        """Select all text in the current editor"""
        if self.editor_tabs.currentWidget():
            self.editor_tabs.currentWidget().selectAll()
    
    def toggleExplorer(self):
        """Toggle the visibility of the file explorer panel"""
        self.file_system_dock.setVisible(not self.file_system_dock.isVisible())
    
    def toggleTerminal(self):
        """Toggle the visibility of the terminal panel"""
        self.terminal_dock.setVisible(not self.terminal_dock.isVisible())
    
    def runCurrentFile(self):
        """Run the current Python file"""
        current_tab = self.editor_tabs.currentIndex()
        if current_tab == -1:
            return
        
        file_path = self.editor_tabs.tabToolTip(current_tab)
        if not file_path or not file_path.endswith('.py'):
            QMessageBox.warning(self, "Warning", "Only Python files can be executed.")
            return
        
        # Save file before running
        self.saveFile()
        
        # Make terminal visible
        self.terminal_dock.setVisible(True)
        
        # Execute in terminal
        self.terminal.execute(f"python {file_path}")
    
    def showAbout(self):
        """Show the about dialog"""
        QMessageBox.about(self, "About PyIDE", 
                         "PyIDE\n\nA simple Python IDE created with PyQt6\n\nVersion 1.0")
    
    def openSettings(self):
        """Open the settings dialog"""
        # TODO: Implement settings dialog
        pass
    
    def loadSettings(self):
        """Load settings from config file"""
        # Create settings directory if it doesn't exist
        os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    
                # Apply settings
                # TODO: Apply loaded settings
        except Exception as e:
            print(f"Error loading settings: {str(e)}")
    
    def saveSettings(self):
        """Save settings to config file"""
        try:
            settings = {
                "window": {
                    "width": self.width(),
                    "height": self.height(),
                    "x": self.x(),
                    "y": self.y()
                },
                "explorer_visible": self.file_system_dock.isVisible(),
                "terminal_visible": self.terminal_dock.isVisible(),
                # Add more settings here
            }
            
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {str(e)}")
    
    def closeEvent(self, event):
        """Handle window close event"""
        # Save settings before closing
        self.saveSettings()
        event.accept()

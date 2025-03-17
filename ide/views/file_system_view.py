"""
File system explorer component for PyIDE
"""

import os
import shutil
from PyQt6.QtWidgets import QTreeView, QMenu, QMessageBox
from PyQt6.QtCore import Qt, QDir, QFileSystemModel

class FileSystemView(QTreeView):
    """File system tree view for exploring directories and files"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.setModel(self.model)
        self.setRootIndex(self.model.index(QDir.homePath()))
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setIndentation(20)
        self.setAnimated(True)
        self.setSortingEnabled(True)
        self.setEditTriggers(QTreeView.EditTrigger.NoEditTriggers)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        
        # Hide unnecessary columns
        for i in range(1, self.model.columnCount()):
            self.hideColumn(i)
    
    def showContextMenu(self, position):
        """Show context menu for the selected item"""
        menu = QMenu()
        
        # Get the index at the position
        index = self.indexAt(position)
        if index.isValid():
            file_path = self.model.filePath(index)
            
            # Add actions based on the file type
            if os.path.isdir(file_path):
                menu.addAction("Open Folder", lambda: self.openFolder(file_path))
            else:
                menu.addAction("Open File", lambda: self.openFile(file_path))
                
            menu.addSeparator()
            menu.addAction("Rename", lambda: self.renameFile(index))
            menu.addAction("Delete", lambda: self.deleteFile(index))
            
            # Show the menu
            menu.exec(self.viewport().mapToGlobal(position))
    
    def openFolder(self, path):
        """Set the root of the tree view to the selected folder"""
        self.setRootIndex(self.model.index(path))
        
    def openFile(self, path):
        """Open the selected file in the editor"""
        # Access the main window through parent chain to open the file
        self.parent().parent().openFile(path)
        
    def renameFile(self, index):
        """Rename the selected file or folder"""
        self.edit(index)
        
    def deleteFile(self, index):
        """Delete the selected file or folder"""
        file_path = self.model.filePath(index)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setText(f"Are you sure you want to delete {file_path}?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        
        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)

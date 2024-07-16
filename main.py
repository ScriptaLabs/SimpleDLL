## WINtoo32 Team's SimpleDLL
# Use responsibly and enjoy cheating.

#NOTE : May not work on Anti-Cheat protected software/games because of restrictions. This injector works on the simple remote thread method.

import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QFileDialog, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import psutil
import ctypes
import win32process
import win32gui

class SimpleInjector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.selected_process = None
        self.selected_dll = None

    def initUI(self):
        self.setWindowTitle('SimpleDLL')
        self.setGeometry(300, 300, 500, 400)

        layout = QVBoxLayout()

        # lst_1
        process_layout = QHBoxLayout()
        self.process_list = QListWidget()
        self.process_list.itemClicked.connect(self.on_process_selected)
        process_layout.addWidget(self.process_list)
    
        refresh_button = QPushButton('Refresh')
        refresh_button.clicked.connect(self.refresh_process_list)
        process_layout.addWidget(refresh_button)
        layout.addLayout(process_layout)

        # sel_1
        dll_layout = QHBoxLayout()
        self.dll_path_label = QLabel('No DLL selected')
        dll_layout.addWidget(self.dll_path_label)
        
        select_dll_button = QPushButton('Select DLL')
        select_dll_button.clicked.connect(self.select_dll)
        dll_layout.addWidget(select_dll_button)
        
        layout.addLayout(dll_layout)

        # btn_1
        inject_button = QPushButton('Inject DLL')
        inject_button.clicked.connect(self.inject_dll)
        layout.addWidget(inject_button)

        self.setLayout(layout)

        self.refresh_process_list()

    def refresh_process_list(self):
        self.process_list.clear()
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                self.process_list.addItem(f"{proc.info['pid']} - {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def on_process_selected(self, item):
        self.selected_process = item.text().split(' - ')[0]

    def select_dll(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select DLL", "", "DLL Files (*.dll)", options=options)
        if fileName:
            self.selected_dll = fileName
            self.dll_path_label.setText(os.path.basename(fileName))

    def inject_dll(self):
        if not self.selected_process or not self.selected_dll:
            QMessageBox.warning(self, "Warning", "Please select both a process and a DLL.")
            return

        try:
            pid = int(self.selected_process)
            process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)
            # LoadLibraryA
            kernel32 = ctypes.windll.kernel32
            load_library = kernel32.GetProcAddress(kernel32.GetModuleHandleA(b"kernel32.dll"), b"LoadLibraryA")
            # allocate_memory
            dll_path = self.selected_dll.encode('ascii')
            remote_memory = kernel32.VirtualAllocEx(process_handle, 0, len(dll_path) + 1, 0x1000 | 0x2000, 0x40)
            # dll_path to allocated_memory
            kernel32.WriteProcessMemory(process_handle, remote_memory, dll_path, len(dll_path) + 1, 0)
            # remote_thread method
            thread_id = ctypes.c_ulong(0)
            kernel32.CreateRemoteThread(process_handle, None, 0, load_library, remote_memory, 0, ctypes.byref(thread_id))

            QMessageBox.information(self, "Success", "DLL injected successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to inject DLL: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SimpleInjector()
    ex.show()
    sys.exit(app.exec_())
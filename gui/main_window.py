"""
Main GUI window for College Scraper application
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import threading
from typing import Callable
import os

class MainWindow:
    """Main application window"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Engineering College Scraper")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Callbacks (to be set by main app)
        self.on_search_callback: Callable = None
        self.on_export_callback: Callable = None
        
        # Variables
        self.state_var = tk.StringVar()
        self.branch_var = tk.StringVar()
        self.college_type_var = tk.StringVar()
        self.max_results_var = tk.IntVar(value=20)
        
        # Status
        self.is_searching = False
        
        # Setup UI
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#366092", height=80)
        title_frame.pack(fill=tk.X, side=tk.TOP)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🎓 Engineering College Information Scraper",
            font=("Arial", 20, "bold"),
            bg="#366092",
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Main container
        main_container = tk.Frame(self.root, padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        self._create_input_section(main_container)
        
        # Progress section
        self._create_progress_section(main_container)
        
        # Results section
        self._create_results_section(main_container)
        
        # Status bar
        self._create_status_bar()
    
    def _create_input_section(self, parent):
        """Create input controls section"""
        input_frame = tk.LabelFrame(
            parent,
            text="Search Parameters",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # State selection
        state_frame = tk.Frame(input_frame)
        state_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(state_frame, text="State:", font=("Arial", 10), width=15, anchor='w').pack(side=tk.LEFT)
        self.state_combo = ttk.Combobox(
            state_frame,
            textvariable=self.state_var,
            font=("Arial", 10),
            state="readonly",
            width=40
        )
        self.state_combo.pack(side=tk.LEFT, padx=5)
        
        # Branch selection
        branch_frame = tk.Frame(input_frame)
        branch_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(branch_frame, text="Branch:", font=("Arial", 10), width=15, anchor='w').pack(side=tk.LEFT)
        self.branch_combo = ttk.Combobox(
            branch_frame,
            textvariable=self.branch_var,
            font=("Arial", 10),
            state="readonly",
            width=40
        )
        self.branch_combo.pack(side=tk.LEFT, padx=5)
        
        # College type selection
        type_frame = tk.Frame(input_frame)
        type_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(type_frame, text="College Type:", font=("Arial", 10), width=15, anchor='w').pack(side=tk.LEFT)
        self.type_combo = ttk.Combobox(
            type_frame,
            textvariable=self.college_type_var,
            font=("Arial", 10),
            state="readonly",
            width=40
        )
        self.type_combo.pack(side=tk.LEFT, padx=5)
        
        # Max results
        max_frame = tk.Frame(input_frame)
        max_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(max_frame, text="Max Results:", font=("Arial", 10), width=15, anchor='w').pack(side=tk.LEFT)
        max_spinbox = tk.Spinbox(
            max_frame,
            from_=5,
            to=50,
            textvariable=self.max_results_var,
            font=("Arial", 10),
            width=10
        )
        max_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Buttons
        button_frame = tk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=(15, 5))
        
        self.search_btn = tk.Button(
            button_frame,
            text="🔍 Start Search",
            font=("Arial", 11, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=20,
            pady=10,
            command=self._on_search_clicked,
            cursor="hand2"
        )
        self.search_btn.pack(side=tk.LEFT, padx=5)
        
        self.export_btn = tk.Button(
            button_frame,
            text="📊 Export to Excel",
            font=("Arial", 11, "bold"),
            bg="#2196F3",
            fg="white",
            padx=20,
            pady=10,
            command=self._on_export_clicked,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑️ Clear Results",
            font=("Arial", 11),
            bg="#f44336",
            fg="white",
            padx=20,
            pady=10,
            command=self._on_clear_clicked,
            cursor="hand2"
        )
        self.clear_btn.pack(side=tk.LEFT, padx=5)
    
    def _create_progress_section(self, parent):
        """Create progress indicator section"""
        progress_frame = tk.Frame(parent)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_label = tk.Label(
            progress_frame,
            text="Ready to search",
            font=("Arial", 10),
            anchor='w'
        )
        self.progress_label.pack(fill=tk.X)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=300
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
    
    def _create_results_section(self, parent):
        """Create results display section"""
        results_frame = tk.LabelFrame(
            parent,
            text="Results",
            font=("Arial", 12, "bold"),
            padx=10,
            pady=10
        )
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results text area
        self.results_text = ScrolledText(
            results_frame,
            font=("Courier New", 9),
            wrap=tk.WORD,
            height=20
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def _create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9),
            bg="#f0f0f0",
            padx=10,
            pady=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def set_states(self, states: list):
        """Set available states"""
        self.state_combo['values'] = states
        if states:
            self.state_combo.current(0)
    
    def set_branches(self, branches: list):
        """Set available branches"""
        self.branch_combo['values'] = branches
        if branches:
            self.branch_combo.current(0)
    
    def set_college_types(self, types: list):
        """Set available college types"""
        self.type_combo['values'] = types
        if types:
            self.type_combo.current(0)
    
    def _on_search_clicked(self):
        """Handle search button click"""
        if self.is_searching:
            messagebox.showwarning("Search in Progress", "A search is already running. Please wait.")
            return
        
        state = self.state_var.get()
        branch = self.branch_var.get()
        college_type = self.college_type_var.get()
        max_results = self.max_results_var.get()
        
        if not state or not branch:
            messagebox.showerror("Input Error", "Please select both State and Branch")
            return
        
        if self.on_search_callback:
            self.on_search_callback(state, branch, college_type, max_results)
    
    def _on_export_clicked(self):
        """Handle export button click"""
        if self.on_export_callback:
            self.on_export_callback()
    
    def _on_clear_clicked(self):
        """Handle clear button click"""
        self.results_text.delete(1.0, tk.END)
        self.update_status("Results cleared")
        self.export_btn.config(state=tk.DISABLED)
    
    def start_search(self):
        """Indicate search has started"""
        self.is_searching = True
        self.search_btn.config(state=tk.DISABLED, bg="#cccccc")
        self.export_btn.config(state=tk.DISABLED)
        self.progress_bar.start(10)
        self.results_text.delete(1.0, tk.END)
    
    def end_search(self, success: bool = True):
        """Indicate search has ended"""
        self.is_searching = False
        self.search_btn.config(state=tk.NORMAL, bg="#4CAF50")
        self.progress_bar.stop()
        
        if success:
            self.export_btn.config(state=tk.NORMAL)
    
    def update_progress(self, message: str):
        """Update progress message"""
        self.progress_label.config(text=message)
        self.root.update_idletasks()
    
    def update_status(self, message: str):
        """Update status bar"""
        self.status_bar.config(text=message)
        self.root.update_idletasks()
    
    def append_result(self, text: str):
        """Append text to results area"""
        self.results_text.insert(tk.END, text + "\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()
    
    def show_error(self, title: str, message: str):
        """Show error dialog"""
        messagebox.showerror(title, message)
    
    def show_info(self, title: str, message: str):
        """Show info dialog"""
        messagebox.showinfo(title, message)
    
    def ask_save_location(self, default_filename: str) -> str:
        """Ask user for save location"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialfile=default_filename
        )
        return filename

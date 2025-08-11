import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import json
from pathlib import Path

SAVE_FILE = "saved_paths.json"

class ModernPathLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_styles()
        self.paths = self.load_paths()
        self.selected_path = tk.StringVar()
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_paths)
        self.create_widgets()
        self.update_listbox()
        
    def setup_window(self):
        self.root.title("🚀 Modern Path Launcher")
        self.root.geometry("750x650")
        self.root.configure(bg="#1a1a1a")
        self.root.resizable(True, True)
        
        # Center window on screen
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (750 // 2)
        y = (self.root.winfo_screenheight() // 2) - (650 // 2)
        self.root.geometry(f"750x650+{x}+{y}")
        
        # Set minimum size
        self.root.minsize(600, 500)
        
    def setup_styles(self):
        self.colors = {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#2d2d2d',
            'bg_card': '#3d3d3d',
            'accent': '#0078d7',
            'accent_hover': '#106ebe',
            'success': '#28a745',
            'success_hover': '#218838',
            'danger': '#dc3545',
            'danger_hover': '#c82333',
            'text_primary': '#ffffff',
            'text_secondary': '#b3b3b3',
            'border': '#4a4a4a',
            'open_glow': '#4dabf7'  # Special glow effect for open button
        }
        
        # Configure ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure treeview style
        style.configure("Custom.Treeview",
                       background=self.colors['bg_card'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_card'],
                       borderwidth=0,
                       font=('Segoe UI', 10))
        
        style.configure("Custom.Treeview.Heading",
                       background=self.colors['bg_secondary'],
                       foreground=self.colors['text_primary'],
                       font=('Segoe UI', 10, 'bold'))
        
        style.map("Custom.Treeview",
                 background=[('selected', self.colors['accent'])])
        
    def get_default_paths(self):
        """Return default Windows paths"""
        user_profile = os.environ.get('USERPROFILE', 'C:\\Users\\Default')
        default_paths = [
            {
                'name': '🖥️ Desktop',
                'path': os.path.join(user_profile, 'Desktop'),
                'category': 'User Folders'
            },
            {
                'name': '📄 Documents',
                'path': os.path.join(user_profile, 'Documents'),
                'category': 'User Folders'
            },
            {
                'name': '⬇️ Downloads',
                'path': os.path.join(user_profile, 'Downloads'),
                'category': 'User Folders'
            },
            {
                'name': '🖼️ Pictures',
                'path': os.path.join(user_profile, 'Pictures'),
                'category': 'User Folders'
            },
            {
                'name': '🎵 Music',
                'path': os.path.join(user_profile, 'Music'),
                'category': 'User Folders'
            },
            {
                'name': '🎥 Videos',
                'path': os.path.join(user_profile, 'Videos'),
                'category': 'User Folders'
            },
            {
                'name': '⚙️ System32',
                'path': 'C:\\Windows\\System32',
                'category': 'System Folders'
            },
            {
                'name': '📦 Program Files',
                'path': 'C:\\Program Files',
                'category': 'System Folders'
            },
            {
                'name': '📦 Program Files (x86)',
                'path': 'C:\\Program Files (x86)',
                'category': 'System Folders'
            },
            {
                'name': '🪟 Windows',
                'path': 'C:\\Windows',
                'category': 'System Folders'
            },
            {
                'name': '🗂️ Temp',
                'path': 'C:\\Windows\\Temp',
                'category': 'System Folders'
            },
            {
                'name': '🚀 Startup',
                'path': os.path.join(user_profile, 'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'),
                'category': 'Special Folders'
            },
            {
                'name': '🏃 Run',
                'path': os.path.join(user_profile, 'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs'),
                'category': 'Special Folders'
            }
        ]
        return default_paths
        
    def load_paths(self):
        """Load paths from file, merge with defaults"""
        default_paths = self.get_default_paths()
        
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r", encoding='utf-8') as f:
                    saved_data = json.load(f)
                    custom_paths = saved_data.get('custom_paths', [])
                    
                    # Add custom paths
                    for path_info in custom_paths:
                        if isinstance(path_info, str):
                            # Convert old format
                            default_paths.append({
                                'name': os.path.basename(path_info) or path_info,
                                'path': path_info,
                                'category': 'Custom Paths'
                            })
                        else:
                            default_paths.append(path_info)
                            
            except (json.JSONDecodeError, FileNotFoundError):
                pass
                
        return default_paths
    
    def save_paths(self):
        """Save custom paths to file"""
        custom_paths = [path for path in self.paths if path.get('category') == 'Custom Paths']
        data = {'custom_paths': custom_paths}
        
        try:
            with open(SAVE_FILE, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save paths:\n{str(e)}")
    
    def create_widgets(self):
        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Search section
        self.create_search_section(main_frame)
        
        # Path list section
        self.create_path_list_section(main_frame)
        
        # Selected path section
        self.create_selected_path_section(main_frame)
        
        # Button section
        self.create_button_section(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
        
    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="🚀 Modern Path Launcher",
            font=('Segoe UI', 24, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_primary']
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Quick access to your favorite Windows locations",
            font=('Segoe UI', 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        )
        subtitle_label.pack()
        
    def create_search_section(self, parent):
        search_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        search_frame.pack(fill=tk.X, pady=(0, 15))
        search_frame.configure(relief=tk.RAISED, bd=1)
        
        tk.Label(
            search_frame,
            text="🔍 Search Paths:",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            bg=self.colors['bg_card'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            relief=tk.FLAT,
            bd=5
        )
        search_entry.pack(fill=tk.X, padx=15, pady=(0, 10))
        
    def create_path_list_section(self, parent):
        list_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        list_frame.configure(relief=tk.RAISED, bd=1)
        
        tk.Label(
            list_frame,
            text="📂 Available Paths:",
            font=('Segoe UI', 10, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        # Create treeview for better organization
        tree_frame = tk.Frame(list_frame, bg=self.colors['bg_secondary'])
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))
        
        # Treeview with scrollbar
        self.tree = ttk.Treeview(tree_frame, style="Custom.Treeview", height=12)
        self.tree['columns'] = ('path', 'status')
        self.tree['show'] = 'tree headings'
        
        self.tree.heading('#0', text='Name', anchor=tk.W)
        self.tree.heading('path', text='Path', anchor=tk.W)
        self.tree.heading('status', text='Status', anchor=tk.CENTER)
        
        self.tree.column('#0', width=200, minwidth=150)
        self.tree.column('path', width=300, minwidth=200)
        self.tree.column('status', width=80, minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Double-1>', lambda e: self.open_selected())
        
    def create_selected_path_section(self, parent):
        selected_frame = tk.Frame(parent, bg=self.colors['bg_secondary'])
        selected_frame.pack(fill=tk.X, pady=(0, 15))
        selected_frame.configure(relief=tk.RAISED, bd=1)
        
        tk.Label(
            selected_frame,
            text="📍 Selected Path:",
            font=('Segoe UI', 16, 'bold'),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        ).pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        self.selected_label = tk.Label(
            selected_frame,
            textvariable=self.selected_path,
            font=('Segoe UI', 16),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_card'],
            relief=tk.FLAT,
            bd=5,
            anchor=tk.W
        )
        self.selected_label.pack(fill=tk.X, padx=15, pady=(0, 10))
        self.selected_path.set("No path selected")
        
    def create_button_section(self, parent):
        # Main button container
        main_button_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        main_button_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Big Open button (main action)
        open_frame = tk.Frame(main_button_frame, bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=2)
        open_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.open_btn = tk.Button(
            open_frame,
            text="🚀 OPEN SELECTED PATH",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['accent'],
            fg=self.colors['text_primary'],
            command=self.open_selected,
            relief=tk.FLAT,
            bd=0,
            cursor='hand2',
            height=3,
            activebackground=self.colors['accent_hover'],
            activeforeground=self.colors['text_primary']
        )
        self.open_btn.pack(fill=tk.BOTH, padx=15, pady=15)
        
        # Secondary buttons row
        secondary_frame = tk.Frame(main_button_frame, bg=self.colors['bg_primary'])
        secondary_frame.pack(fill=tk.X)
        
        # Secondary button style
        secondary_btn_style = {
            'font': ('Segoe UI', 12, 'bold'),
            'relief': tk.FLAT,
            'bd': 0,
            'cursor': 'hand2',
            'height': 2
        }
        
        self.add_btn = tk.Button(
            secondary_frame,
            text="➕ Add Custom Path",
            bg=self.colors['success'],
            fg=self.colors['text_primary'],
            command=self.add_path,
            activebackground=self.colors['success_hover'],
            activeforeground=self.colors['text_primary'],
            **secondary_btn_style
        )
        self.add_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.remove_btn = tk.Button(
            secondary_frame,
            text="❌ Remove Path",
            bg=self.colors['danger'],
            fg=self.colors['text_primary'],
            command=self.remove_selected,
            activebackground=self.colors['danger_hover'],
            activeforeground=self.colors['text_primary'],
            **secondary_btn_style
        )
        self.remove_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Bind hover effects
        self.bind_hover_effects()
        
    def create_status_bar(self, parent):
        status_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text=f"📊 Total paths: {len(self.paths)}",
            font=('Segoe UI', 9),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_secondary']
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
    def bind_hover_effects(self):
        def on_enter(e, color):
            e.widget.config(bg=color)
        
        def on_leave(e, color):
            e.widget.config(bg=color)
            
        def on_enter_open(e):
            e.widget.config(bg=self.colors['accent_hover'])
            e.widget.config(font=('Segoe UI', 19, 'bold'))  # Slightly bigger on hover
        
        def on_leave_open(e):
            e.widget.config(bg=self.colors['accent'])
            e.widget.config(font=('Segoe UI', 18, 'bold'))  # Back to normal
        
        # Big open button special effects
        self.open_btn.bind('<Enter>', on_enter_open)
        self.open_btn.bind('<Leave>', on_leave_open)
        
        # Secondary buttons
        self.add_btn.bind('<Enter>', lambda e: on_enter(e, self.colors['success_hover']))
        self.add_btn.bind('<Leave>', lambda e: on_leave(e, self.colors['success']))
        
        self.remove_btn.bind('<Enter>', lambda e: on_enter(e, self.colors['danger_hover']))
        self.remove_btn.bind('<Leave>', lambda e: on_leave(e, self.colors['danger']))
        
    def update_listbox(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Group paths by category
        categories = {}
        for path_info in self.paths:
            category = path_info.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append(path_info)
        
        # Add items to treeview
        for category, paths in categories.items():
            category_id = self.tree.insert('', tk.END, text=f"📁 {category}", values=('', ''), open=True)
            
            for path_info in paths:
                status = "✅" if os.path.exists(path_info['path']) else "❌"
                self.tree.insert(
                    category_id, tk.END,
                    text=path_info['name'],
                    values=(path_info['path'], status)
                )
        
        # Update status
        self.status_label.config(text=f"📊 Total paths: {len(self.paths)}")
        
    def filter_paths(self, *args):
        search_term = self.search_var.get().lower()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not search_term:
            self.update_listbox()
            return
        
        # Filter and display matching paths
        filtered_paths = [p for p in self.paths if search_term in p['name'].lower() or search_term in p['path'].lower()]
        
        if filtered_paths:
            search_id = self.tree.insert('', tk.END, text="🔍 Search Results", values=('', ''), open=True)
            for path_info in filtered_paths:
                status = "✅" if os.path.exists(path_info['path']) else "❌"
                self.tree.insert(
                    search_id, tk.END,
                    text=path_info['name'],
                    values=(path_info['path'], status)
                )
        
    def on_tree_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item, 'values')
            if values and values[0]:  # Has a path value
                self.selected_path.set(values[0])
            else:
                self.selected_path.set("No path selected")
        
    def add_path(self):
        folder = filedialog.askdirectory(title="Select Folder to Add")
        if folder:
            # Check if path already exists
            existing_paths = [p['path'] for p in self.paths]
            if folder not in existing_paths:
                path_info = {
                    'name': f"📁 {os.path.basename(folder) or folder}",
                    'path': folder,
                    'category': 'Custom Paths'
                }
                self.paths.append(path_info)
                self.update_listbox()
                self.save_paths()
                messagebox.showinfo("Success", f"Path added successfully:\n{folder}")
            else:
                messagebox.showwarning("Duplicate", "This path already exists in the list.")
    
    def open_selected(self):
        current_path = self.selected_path.get()
        if current_path == "No path selected":
            messagebox.showwarning("No Selection", "Please select a path from the list.")
            # Flash the open button to draw attention
            self.flash_open_button()
            return
        
        if os.path.exists(current_path):
            try:
                # Visual feedback - button press effect
                self.open_btn.config(bg=self.colors['accent_hover'])
                self.root.update()
                
                subprocess.Popen(f'explorer "{current_path}"', shell=True)
                self.status_label.config(text=f"📂 Opened: {os.path.basename(current_path)}")
                
                # Success flash effect
                self.root.after(100, lambda: self.open_btn.config(bg=self.colors['accent']))
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open path:\n{str(e)}")
        else:
            messagebox.showerror("Error", f"Path does not exist:\n{current_path}")
            
    def flash_open_button(self):
        """Flash the open button to draw user attention"""
        original_color = self.open_btn.cget('bg')
        flash_color = self.colors['danger']
        
        def flash_cycle(count=0):
            if count < 6:  # Flash 3 times
                color = flash_color if count % 2 == 0 else original_color
                self.open_btn.config(bg=color)
                self.root.after(200, lambda: flash_cycle(count + 1))
            else:
                self.open_btn.config(bg=original_color)
    
    def remove_selected(self):
        current_path = self.selected_path.get()
        if current_path == "No path selected":
            messagebox.showwarning("No Selection", "Please select a path to remove.")
            return
        
        # Find and remove the path
        for i, path_info in enumerate(self.paths):
            if path_info['path'] == current_path and path_info.get('category') == 'Custom Paths':
                if messagebox.askyesno("Confirm Removal", f"Remove this path?\n{current_path}"):
                    del self.paths[i]
                    self.update_listbox()
                    self.save_paths()
                    self.selected_path.set("No path selected")
                    messagebox.showinfo("Success", "Path removed successfully.")
                return
        
        messagebox.showwarning("Cannot Remove", "Only custom paths can be removed.")
    
    def run(self):
        # Bind keyboard shortcuts
        self.root.bind('<Return>', lambda e: self.open_selected())
        self.root.bind('<Delete>', lambda e: self.remove_selected())
        self.root.bind('<Control-o>', lambda e: self.add_path())
        
        # Start the application
        self.root.mainloop()

def main():
    app = ModernPathLauncher()
    app.run()

if __name__ == "__main__":
    main()
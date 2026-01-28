import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import sys
import os
import json
from datetime import datetime

# Import from existing youdork.py
from youdork import (
    HEADER, DATABASE_FILE, LOG_DIR, CATEGORY_MAPPING,
    load_database, insert_smartly, save_to_log, scrape_exploitdb,
    show_help, show_support, LOGGING
)

class YouDorkGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("You-Dork GUI")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e1e")
        
        self.logging_enabled = LOGGING
        
        # Header
        header_frame = tk.Frame(root, bg="#1e1e1e")
        header_frame.pack(pady=10, padx=10, fill=tk.X)
        
        header_label = tk.Label(
            header_frame,
            text="YOU-DORK\nGoogle Dorks Generator for OSINT",
            font=("Courier", 16, "bold"),
            fg="#88DDFF",
            bg="#1e1e1e"
        )
        header_label.pack()
        
        disclaimer = tk.Label(
            header_frame,
            text="by: OtterBot | v1.0.0 | Use at your own risk",
            font=("Courier", 9),
            fg="#FF6B6B",
            bg="#1e1e1e"
        )
        disclaimer.pack()
        
        # Main content frame
        content_frame = tk.Frame(root, bg="#1e1e1e")
        content_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Left panel - Controls
        left_panel = tk.Frame(content_frame, bg="#2d2d2d", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        
        controls_label = tk.Label(
            left_panel,
            text="CONTROLS",
            font=("Courier", 12, "bold"),
            fg="#77DD77",
            bg="#2d2d2d"
        )
        controls_label.pack(pady=10)
        
        # Buttons
        btn_style = {
            "font": ("Courier", 10),
            "bg": "#3d3d3d",
            "fg": "#ffffff",
            "activebackground": "#4d4d4d",
            "activeforeground": "#88DDFF",
            "relief": tk.FLAT,
            "cursor": "hand2",
            "width": 20,
            "pady": 8
        }
        
        self.generate_btn = tk.Button(
            left_panel,
            text="Generate Dorks",
            command=self.open_input_form,
            **btn_style
        )
        self.generate_btn.pack(pady=5, padx=10)
        
        self.logging_btn = tk.Button(
            left_panel,
            text=f"Logging: {'ON' if self.logging_enabled else 'OFF'}",
            command=self.toggle_logging,
            **btn_style
        )
        self.logging_btn.pack(pady=5, padx=10)
        
        tk.Button(
            left_panel,
            text="Update Database",
            command=self.update_database,
            **btn_style
        ).pack(pady=5, padx=10)
        
        tk.Button(
            left_panel,
            text="Help",
            command=self.show_help_dialog,
            **btn_style
        ).pack(pady=5, padx=10)
        
        tk.Button(
            left_panel,
            text="Support Author",
            command=self.show_support_dialog,
            **btn_style
        ).pack(pady=5, padx=10)
        
        tk.Button(
            left_panel,
            text="Exit",
            command=self.root.quit,
            bg="#FF6B6B",
            fg="#ffffff",
            font=("Courier", 10, "bold"),
            activebackground="#FF5555",
            relief=tk.FLAT,
            cursor="hand2",
            width=20,
            pady=8
        ).pack(pady=20, padx=10, side=tk.BOTTOM)
        
        # Right panel - Output
        right_panel = tk.Frame(content_frame, bg="#2d2d2d", relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        output_label = tk.Label(
            right_panel,
            text="OUTPUT",
            font=("Courier", 12, "bold"),
            fg="#77DD77",
            bg="#2d2d2d"
        )
        output_label.pack(pady=10)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(
            right_panel,
            font=("Courier", 9),
            bg="#1a1a1a",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.output_text.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_bar = tk.Label(
            root,
            text="Ready",
            font=("Courier", 9),
            fg="#88DDFF",
            bg="#1e1e1e",
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        
        self.write_output("Welcome to You-Dork GUI!\n")
        self.write_output("Click 'Generate Dorks' to begin.\n\n")
    
    def write_output(self, text, color=None):
        """Write text to output area"""
        self.output_text.insert(tk.END, text)
        if color:
            # Tag-based coloring (optional enhancement)
            pass
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_output(self):
        """Clear output text area"""
        self.output_text.delete(1.0, tk.END)
    
    def update_status(self, text):
        """Update status bar"""
        self.status_bar.config(text=text)
        self.root.update_idletasks()
    
    def toggle_logging(self):
        """Toggle logging state"""
        global LOGGING
        self.logging_enabled = not self.logging_enabled
        self.logging_btn.config(text=f"Logging: {'ON' if self.logging_enabled else 'OFF'}")
        self.write_output(f"\n[✔] Logging {'enabled' if self.logging_enabled else 'disabled'}\n\n")
    
    def open_input_form(self):
        """Open input form window"""
        form_window = tk.Toplevel(self.root)
        form_window.title("Enter Information")
        form_window.geometry("500x600")
        form_window.configure(bg="#2d2d2d")
        form_window.transient(self.root)
        form_window.grab_set()
        
        # Title
        title_label = tk.Label(
            form_window,
            text="Enter Information for Dork Generation",
            font=("Courier", 12, "bold"),
            fg="#77DD77",
            bg="#2d2d2d"
        )
        title_label.pack(pady=10)
        
        # Scrollable frame for inputs
        canvas = tk.Canvas(form_window, bg="#2d2d2d", highlightthickness=0)
        scrollbar = ttk.Scrollbar(form_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2d2d2d")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Input fields
        input_fields = {}
        field_specs = [
            ("Name", "name"),
            ("Username", "username"),
            ("Email", "email"),
            ("Phone Number", "phone"),
            ("File Type", "filetype"),
            ("IP Address", "ip"),
            ("Domain/Website", "domain"),
            ("Cryptocurrency Wallet", "crypto"),
            ("Social Media Handle", "social"),
            ("Technology Stack", "tech"),
            ("Physical Address", "address"),
            ("CVE/Vulnerability", "cve")
        ]
        
        for label_text, field_key in field_specs:
            frame = tk.Frame(scrollable_frame, bg="#2d2d2d")
            frame.pack(pady=5, padx=20, fill=tk.X)
            
            label = tk.Label(
                frame,
                text=f"{label_text}:",
                font=("Courier", 10),
                fg="#88DDFF",
                bg="#2d2d2d",
                width=20,
                anchor=tk.W
            )
            label.pack(side=tk.LEFT)
            
            entry = tk.Entry(
                frame,
                font=("Courier", 10),
                bg="#1a1a1a",
                fg="#ffffff",
                insertbackground="#ffffff",
                relief=tk.FLAT
            )
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            input_fields[field_key] = entry
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Buttons
        button_frame = tk.Frame(form_window, bg="#2d2d2d")
        button_frame.pack(pady=10)
        
        def on_generate():
            user_inputs = {key: entry.get().strip() for key, entry in input_fields.items()}
            form_window.destroy()
            self.generate_dorks(user_inputs)
        
        tk.Button(
            button_frame,
            text="Generate",
            command=on_generate,
            font=("Courier", 10, "bold"),
            bg="#77DD77",
            fg="#000000",
            activebackground="#66CC66",
            relief=tk.FLAT,
            cursor="hand2",
            width=15,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="Cancel",
            command=form_window.destroy,
            font=("Courier", 10),
            bg="#FF6B6B",
            fg="#ffffff",
            activebackground="#FF5555",
            relief=tk.FLAT,
            cursor="hand2",
            width=15,
            pady=5
        ).pack(side=tk.LEFT, padx=5)
    
    def generate_dorks(self, user_inputs):
        """Generate dorks based on user inputs"""
        self.clear_output()
        self.update_status("Loading database...")
        
        def generate_thread():
            try:
                database = load_database()
                self.write_output("[*] Generating Google Dorks...\n\n")
                
                generated_dorks = {}
                
                for input_type, user_value in user_inputs.items():
                    if user_value:
                        if input_type not in generated_dorks:
                            generated_dorks[input_type] = {}
                        
                        for category in CATEGORY_MAPPING.get(input_type, []):
                            if category in database:
                                if category not in generated_dorks[input_type]:
                                    generated_dorks[input_type][category] = []
                                
                                dorks_list = insert_smartly(database[category], user_value)
                                best_dorks = dorks_list[:min(len(dorks_list), 10)]
                                generated_dorks[input_type][category].extend(best_dorks)
                
                self.write_output("[✔] Google Dorks Generated:\n\n")
                
                if not generated_dorks:
                    self.write_output("[!] No Google Dorks found for the provided inputs.\n\n")
                else:
                    for input_type, categories in generated_dorks.items():
                        self.write_output(f"═══ {input_type.upper()} ═══\n")
                        for category, dorks in categories.items():
                            self.write_output(f"  ┌─ [{category}]\n")
                            for dork in dorks:
                                self.write_output(f"  │   {dork}\n")
                            self.write_output(f"  └─\n\n")
                
                # Handle logging
                if self.logging_enabled:
                    save_to_log(generated_dorks)
                    log_file = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.txt")
                    self.write_output(f"[✔] Saved to {log_file}\n")
                else:
                    self.write_output("[i] Logging is OFF. Enable it to auto-save results.\n")
                
                self.update_status("Generation complete")
                
            except Exception as e:
                self.write_output(f"\n[!] Error: {str(e)}\n")
                self.update_status("Error during generation")
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def update_database(self):
        """Update database from Exploit-DB"""
        response = messagebox.askyesno(
            "Update Database",
            "This will scrape the entire Exploit-DB GHDB (7,950+ dorks).\n"
            "This may take several minutes.\n\nContinue?"
        )
        
        if not response:
            return
        
        self.clear_output()
        self.write_output("[*] Starting database update...\n")
        self.write_output("[*] This may take 5-10 minutes. Please wait...\n\n")
        self.update_status("Updating database...")
        
        def update_thread():
            try:
                result = scrape_exploitdb()
                if result is not False:
                    self.write_output("[✔] Database updated successfully!\n")
                    self.update_status("Database updated")
                else:
                    self.write_output("[!] Database update failed.\n")
                    self.update_status("Update failed")
            except Exception as e:
                self.write_output(f"[!] Error updating database: {str(e)}\n")
                self.update_status("Update error")
        
        threading.Thread(target=update_thread, daemon=True).start()
    
    def show_help_dialog(self):
        """Show help information"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        help_window.geometry("700x600")
        help_window.configure(bg="#2d2d2d")
        help_window.transient(self.root)
        
        help_text = scrolledtext.ScrolledText(
            help_window,
            font=("Courier", 9),
            bg="#1a1a1a",
            fg="#ffffff",
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        help_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Load help from assets/README.txt
        help_file = os.path.join("assets", "README.txt")
        if os.path.exists(help_file):
            with open(help_file, "r", encoding="utf-8") as f:
                help_text.insert(tk.END, f.read())
        else:
            help_text.insert(tk.END, "Help file not found.")
        
        help_text.config(state=tk.DISABLED)
        
        tk.Button(
            help_window,
            text="Close",
            command=help_window.destroy,
            font=("Courier", 10),
            bg="#3d3d3d",
            fg="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            pady=5
        ).pack(pady=5)
    
    def show_support_dialog(self):
        """Show support information"""
        support_window = tk.Toplevel(self.root)
        support_window.title("Support Author")
        support_window.geometry("600x400")
        support_window.configure(bg="#2d2d2d")
        support_window.transient(self.root)
        
        support_text = scrolledtext.ScrolledText(
            support_window,
            font=("Courier", 9),
            bg="#1a1a1a",
            fg="#ffffff",
            wrap=tk.WORD,
            relief=tk.FLAT
        )
        support_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Load support from assets/SUPPORT.txt
        support_file = os.path.join("assets", "SUPPORT.txt")
        if os.path.exists(support_file):
            with open(support_file, "r", encoding="utf-8") as f:
                support_text.insert(tk.END, f.read())
        else:
            support_text.insert(tk.END, "Support file not found.")
        
        support_text.config(state=tk.DISABLED)
        
        tk.Button(
            support_window,
            text="Close",
            command=support_window.destroy,
            font=("Courier", 10),
            bg="#3d3d3d",
            fg="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            pady=5
        ).pack(pady=5)


def main():
    root = tk.Tk()
    app = YouDorkGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

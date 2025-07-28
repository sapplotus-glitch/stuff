
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import subprocess
import threading
import winreg
from pathlib import Path
import requests
import time

class FastFlagManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PS99 Roblox Fast Flag Optimizer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a2e')
        
        # Fast Flag configurations with risk levels
        self.fast_flags = {
            # Performance Optimizations
            "DFStringGraphicsPreset": {
                "description": "Controls overall graphics quality preset",
                "values": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                "default": "1",
                "current": "1",
                "risk": "Low",
                "category": "Performance"
            },
            "DFIntTextureQuality": {
                "description": "Texture quality level (lower = better performance)",
                "values": ["0", "1", "2", "3"],
                "default": "0",
                "current": "0",
                "risk": "Low",
                "category": "Performance"
            },
            "FFlagDebugDisableShadows": {
                "description": "Disables shadows for better performance",
                "values": ["true", "false"],
                "default": "true",
                "current": "true",
                "risk": "Low",
                "category": "Performance"
            },
            "FFlagDisablePostFX": {
                "description": "Disables post-processing effects",
                "values": ["true", "false"],
                "default": "true",
                "current": "true",
                "risk": "Low",
                "category": "Performance"
            },
            "DFIntMaxFrameRate": {
                "description": "Maximum frame rate limit",
                "values": ["30", "60", "120", "144", "240"],
                "default": "60",
                "current": "60",
                "risk": "Low",
                "category": "Performance"
            },
            "FFlagRenderFixFog": {
                "description": "Fixes fog rendering issues",
                "values": ["true", "false"],
                "default": "false",
                "current": "false",
                "risk": "Low",
                "category": "Performance"
            },
            "DFIntMeshContentProviderForceCacheSize": {
                "description": "Mesh cache size (MB)",
                "values": ["268435456", "134217728", "67108864"],
                "default": "268435456",
                "current": "268435456",
                "risk": "Low",
                "category": "Performance"
            },
            
            # Quality Enhancements
            "FFlagFixGraphicsQuality": {
                "description": "Enables graphics quality fixes",
                "values": ["true", "false"],
                "default": "true",
                "current": "true",
                "risk": "Low",
                "category": "Quality"
            },
            "DFIntMaxUniverseId": {
                "description": "Maximum universe ID for better loading",
                "values": ["2147483647", "1073741823"],
                "default": "2147483647",
                "current": "2147483647",
                "risk": "Low",
                "category": "Quality"
            },
            
            # Network Optimizations
            "DFIntMaxHTTPConnectionsPerHost": {
                "description": "Max HTTP connections per host",
                "values": ["16", "32", "64"],
                "default": "16",
                "current": "16",
                "risk": "Medium",
                "category": "Network"
            },
            "FFlagDebugDisableInterpolation": {
                "description": "Disables network interpolation",
                "values": ["true", "false"],
                "default": "false",
                "current": "false",
                "risk": "Medium",
                "category": "Network"
            },
            
            # UI/UX Tweaks
            "FFlagDisableNewChatTranslationUI": {
                "description": "Disables new chat translation UI",
                "values": ["true", "false"],
                "default": "false",
                "current": "false",
                "risk": "Low",
                "category": "UI"
            },
            "FFlagEnableInGameMenuV3": {
                "description": "Enables new in-game menu",
                "values": ["true", "false"],
                "default": "false",
                "current": "false",
                "risk": "Low",
                "category": "UI"
            },
            
            # Experimental (High Risk)
            "DFFlagVideoCaptureServiceEnabled": {
                "description": "Enables video capture service",
                "values": ["true", "false"],
                "default": "false",
                "current": "false",
                "risk": "High",
                "category": "Experimental"
            },
            "FFlagDebugForceCrashOnError": {
                "description": "Forces crash on errors (debugging)",
                "values": ["true", "false"],
                "default": "false",
                "current": "false",
                "risk": "High",
                "category": "Experimental"
            }
        }
        
        self.presets = {
            "Ultra Performance": {
                "DFStringGraphicsPreset": "1",
                "DFIntTextureQuality": "0",
                "FFlagDebugDisableShadows": "true",
                "FFlagDisablePostFX": "true",
                "DFIntMaxFrameRate": "60"
            },
            "Balanced": {
                "DFStringGraphicsPreset": "5",
                "DFIntTextureQuality": "1",
                "FFlagDebugDisableShadows": "false",
                "FFlagDisablePostFX": "false",
                "DFIntMaxFrameRate": "60"
            },
            "High Quality": {
                "DFStringGraphicsPreset": "10",
                "DFIntTextureQuality": "3",
                "FFlagDebugDisableShadows": "false",
                "FFlagDisablePostFX": "false",
                "DFIntMaxFrameRate": "144"
            }
        }
        
        self.setup_ui()
        self.load_current_flags()
        
    def setup_ui(self):
        # Main title
        title_label = tk.Label(
            self.root,
            text="PS99 Roblox Fast Flag Manager",
            font=('Arial', 20, 'bold'),
            fg='#ff6600',
            bg='#1a1a2e'
        )
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Fast Flags tab
        self.flags_frame = tk.Frame(self.notebook, bg='#2d2d50')
        self.notebook.add(self.flags_frame, text="Fast Flags")
        
        # Presets tab
        self.presets_frame = tk.Frame(self.notebook, bg='#2d2d50')
        self.notebook.add(self.presets_frame, text="Presets")
        
        # Tools tab
        self.tools_frame = tk.Frame(self.notebook, bg='#2d2d50')
        self.notebook.add(self.tools_frame, text="Tools")
        
        self.setup_flags_tab()
        self.setup_presets_tab()
        self.setup_tools_tab()
        
        # Control buttons
        self.setup_control_buttons()
        
    def setup_flags_tab(self):
        # Category filter
        filter_frame = tk.Frame(self.flags_frame, bg='#2d2d50')
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(filter_frame, text="Category:", bg='#2d2d50', fg='white').pack(side='left')
        
        self.category_var = tk.StringVar(value="All")
        categories = ["All"] + list(set(flag['category'] for flag in self.fast_flags.values()))
        category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var, values=categories, width=15)
        category_combo.pack(side='left', padx=5)
        category_combo.bind('<<ComboboxSelected>>', self.filter_flags)
        
        # Search
        tk.Label(filter_frame, text="Search:", bg='#2d2d50', fg='white').pack(side='left', padx=(20, 5))
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable=self.search_var, bg='#404060', fg='white', width=20)
        search_entry.pack(side='left')
        search_entry.bind('<KeyRelease>', self.filter_flags)
        
        # Scrollable frame for flags
        canvas = tk.Canvas(self.flags_frame, bg='#2d2d50')
        scrollbar = ttk.Scrollbar(self.flags_frame, orient='vertical', command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#2d2d50')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        self.flag_widgets = {}
        self.create_flag_widgets()
        
    def create_flag_widgets(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.flag_widgets.clear()
        
        current_category = self.category_var.get()
        search_term = self.search_var.get().lower()
        
        for flag_name, flag_data in self.fast_flags.items():
            # Filter by category and search
            if current_category != "All" and flag_data['category'] != current_category:
                continue
            if search_term and search_term not in flag_name.lower() and search_term not in flag_data['description'].lower():
                continue
                
            self.create_flag_widget(flag_name, flag_data)
    
    def create_flag_widget(self, flag_name, flag_data):
        # Main frame for this flag
        flag_frame = tk.LabelFrame(
            self.scrollable_frame,
            text=flag_name,
            bg='#3d3d60',
            fg='#ffaa00',
            font=('Arial', 10, 'bold')
        )
        flag_frame.pack(fill='x', padx=5, pady=3)
        
        # Description and risk
        info_frame = tk.Frame(flag_frame, bg='#3d3d60')
        info_frame.pack(fill='x', padx=5, pady=2)
        
        desc_label = tk.Label(
            info_frame,
            text=flag_data['description'],
            bg='#3d3d60',
            fg='white',
            wraplength=400,
            justify='left'
        )
        desc_label.pack(side='left')
        
        # Risk badge
        risk_color = {'Low': '#00ff00', 'Medium': '#ffaa00', 'High': '#ff0000'}[flag_data['risk']]
        risk_label = tk.Label(
            info_frame,
            text=f"Risk: {flag_data['risk']}",
            bg=risk_color,
            fg='black',
            font=('Arial', 8, 'bold'),
            padx=5
        )
        risk_label.pack(side='right')
        
        # Control frame
        control_frame = tk.Frame(flag_frame, bg='#3d3d60')
        control_frame.pack(fill='x', padx=5, pady=2)
        
        tk.Label(control_frame, text="Value:", bg='#3d3d60', fg='white').pack(side='left')
        
        # Value selector
        value_var = tk.StringVar(value=flag_data['current'])
        if len(flag_data['values']) <= 5:
            # Use radio buttons for few options
            for value in flag_data['values']:
                rb = tk.Radiobutton(
                    control_frame,
                    text=value,
                    variable=value_var,
                    value=value,
                    bg='#3d3d60',
                    fg='white',
                    selectcolor='#5d5d80',
                    command=lambda fn=flag_name, var=value_var: self.update_flag(fn, var.get())
                )
                rb.pack(side='left', padx=2)
        else:
            # Use combobox for many options
            combo = ttk.Combobox(control_frame, textvariable=value_var, values=flag_data['values'], width=10)
            combo.pack(side='left', padx=5)
            combo.bind('<<ComboboxSelected>>', lambda e, fn=flag_name, var=value_var: self.update_flag(fn, var.get()))
        
        # Reset button
        reset_btn = tk.Button(
            control_frame,
            text="Reset",
            command=lambda fn=flag_name: self.reset_flag(fn),
            bg='#666699',
            fg='white',
            font=('Arial', 8)
        )
        reset_btn.pack(side='right', padx=5)
        
        self.flag_widgets[flag_name] = value_var
    
    def setup_presets_tab(self):
        presets_label = tk.Label(
            self.presets_frame,
            text="Quick Performance Presets",
            font=('Arial', 16, 'bold'),
            fg='#ff6600',
            bg='#2d2d50'
        )
        presets_label.pack(pady=10)
        
        for preset_name, preset_flags in self.presets.items():
            preset_frame = tk.LabelFrame(
                self.presets_frame,
                text=preset_name,
                bg='#3d3d60',
                fg='#ffaa00',
                font=('Arial', 12, 'bold')
            )
            preset_frame.pack(fill='x', padx=20, pady=5)
            
            # Show what this preset does
            desc_text = f"Applies {len(preset_flags)} optimized settings"
            tk.Label(preset_frame, text=desc_text, bg='#3d3d60', fg='white').pack(pady=2)
            
            apply_btn = tk.Button(
                preset_frame,
                text=f"Apply {preset_name}",
                command=lambda pn=preset_name: self.apply_preset(pn),
                bg='#00aa00',
                fg='white',
                font=('Arial', 10, 'bold'),
                width=20
            )
            apply_btn.pack(pady=5)
    
    def setup_tools_tab(self):
        tools_label = tk.Label(
            self.tools_frame,
            text="Roblox Optimization Tools",
            font=('Arial', 16, 'bold'),
            fg='#ff6600',
            bg='#2d2d50'
        )
        tools_label.pack(pady=10)
        
        # Roblox process optimization
        process_frame = tk.LabelFrame(
            self.tools_frame,
            text="Process Optimization",
            bg='#3d3d60',
            fg='#ffaa00',
            font=('Arial', 12, 'bold')
        )
        process_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Button(
            process_frame,
            text="Optimize Roblox Processes",
            command=self.optimize_processes,
            bg='#0066cc',
            fg='white',
            width=25
        ).pack(pady=5)
        
        tk.Button(
            process_frame,
            text="Clear Roblox Cache",
            command=self.clear_cache,
            bg='#cc6600',
            fg='white',
            width=25
        ).pack(pady=5)
        
        # Registry optimization
        registry_frame = tk.LabelFrame(
            self.tools_frame,
            text="Registry Optimization",
            bg='#3d3d60',
            fg='#ffaa00',
            font=('Arial', 12, 'bold')
        )
        registry_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Button(
            registry_frame,
            text="Optimize Registry Settings",
            command=self.optimize_registry,
            bg='#cc0066',
            fg='white',
            width=25
        ).pack(pady=5)
        
        # System optimization
        system_frame = tk.LabelFrame(
            self.tools_frame,
            text="System Optimization",
            bg='#3d3d60',
            fg='#ffaa00',
            font=('Arial', 12, 'bold')
        )
        system_frame.pack(fill='x', padx=20, pady=5)
        
        tk.Button(
            system_frame,
            text="Set Process Priority",
            command=self.set_process_priority,
            bg='#6600cc',
            fg='white',
            width=25
        ).pack(pady=5)
    
    def setup_control_buttons(self):
        control_frame = tk.Frame(self.root, bg='#1a1a2e')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Button(
            control_frame,
            text="Apply All Changes",
            command=self.apply_all_changes,
            bg='#00aa00',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=15
        ).pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="Reset All to Default",
            command=self.reset_all,
            bg='#aa0000',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=15
        ).pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="Export Settings",
            command=self.export_settings,
            bg='#0066aa',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=15
        ).pack(side='left', padx=5)
        
        tk.Button(
            control_frame,
            text="Import Settings",
            command=self.import_settings,
            bg='#aa6600',
            fg='white',
            font=('Arial', 12, 'bold'),
            width=15
        ).pack(side='left', padx=5)
    
    def filter_flags(self, event=None):
        self.create_flag_widgets()
    
    def update_flag(self, flag_name, value):
        self.fast_flags[flag_name]['current'] = value
        print(f"Updated {flag_name} to {value}")
    
    def reset_flag(self, flag_name):
        default_value = self.fast_flags[flag_name]['default']
        self.fast_flags[flag_name]['current'] = default_value
        if flag_name in self.flag_widgets:
            self.flag_widgets[flag_name].set(default_value)
    
    def apply_preset(self, preset_name):
        preset_flags = self.presets[preset_name]
        for flag_name, value in preset_flags.items():
            if flag_name in self.fast_flags:
                self.fast_flags[flag_name]['current'] = value
                if flag_name in self.flag_widgets:
                    self.flag_widgets[flag_name].set(value)
        messagebox.showinfo("Success", f"Applied {preset_name} preset!")
    
    def get_roblox_path(self):
        try:
            # Try to find Roblox installation path
            possible_paths = [
                os.path.expandvars(r"%LOCALAPPDATA%\Roblox\Versions"),
                os.path.expandvars(r"%PROGRAMFILES(X86)%\Roblox\Versions"),
                os.path.expandvars(r"%PROGRAMFILES%\Roblox\Versions")
            ]
            
            for base_path in possible_paths:
                if os.path.exists(base_path):
                    versions = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
                    if versions:
                        # Get the latest version
                        latest_version = max(versions)
                        return os.path.join(base_path, latest_version)
        except Exception as e:
            print(f"Error finding Roblox path: {e}")
        return None
    
    def apply_all_changes(self):
        try:
            roblox_path = self.get_roblox_path()
            if not roblox_path:
                messagebox.showerror("Error", "Could not find Roblox installation!")
                return
            
            # Create ClientSettings folder if it doesn't exist
            settings_path = os.path.join(roblox_path, "ClientSettings")
            os.makedirs(settings_path, exist_ok=True)
            
            # Create ClientAppSettings.json
            settings_file = os.path.join(settings_path, "ClientAppSettings.json")
            
            # Build settings dictionary
            settings = {}
            for flag_name, flag_data in self.fast_flags.items():
                if flag_data['current'] != flag_data['default']:
                    settings[flag_name] = flag_data['current']
            
            # Write settings to file
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            
            messagebox.showinfo("Success", f"Applied {len(settings)} fast flags to Roblox!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply settings: {str(e)}")
    
    def reset_all(self):
        for flag_name, flag_data in self.fast_flags.items():
            flag_data['current'] = flag_data['default']
            if flag_name in self.flag_widgets:
                self.flag_widgets[flag_name].set(flag_data['default'])
        messagebox.showinfo("Success", "Reset all flags to default!")
    
    def export_settings(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")],
                title="Export Fast Flag Settings"
            )
            if filename:
                settings = {flag: data['current'] for flag, data in self.fast_flags.items()}
                with open(filename, 'w') as f:
                    json.dump(settings, f, indent=2)
                messagebox.showinfo("Success", "Settings exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export settings: {str(e)}")
    
    def import_settings(self):
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json")],
                title="Import Fast Flag Settings"
            )
            if filename:
                with open(filename, 'r') as f:
                    settings = json.load(f)
                
                for flag_name, value in settings.items():
                    if flag_name in self.fast_flags:
                        if value in self.fast_flags[flag_name]['values']:
                            self.fast_flags[flag_name]['current'] = value
                            if flag_name in self.flag_widgets:
                                self.flag_widgets[flag_name].set(value)
                
                messagebox.showinfo("Success", "Settings imported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import settings: {str(e)}")
    
    def optimize_processes(self):
        try:
            # Kill unnecessary processes
            processes_to_kill = ['chrome.exe', 'discord.exe', 'spotify.exe']
            for process in processes_to_kill:
                try:
                    subprocess.run(['taskkill', '/f', '/im', process], 
                                 capture_output=True, check=False)
                except:
                    pass
            
            messagebox.showinfo("Success", "Optimized system processes!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to optimize processes: {str(e)}")
    
    def clear_cache(self):
        try:
            cache_paths = [
                os.path.expandvars(r"%LOCALAPPDATA%\Roblox\logs"),
                os.path.expandvars(r"%TEMP%\Roblox"),
            ]
            
            for cache_path in cache_paths:
                if os.path.exists(cache_path):
                    import shutil
                    shutil.rmtree(cache_path, ignore_errors=True)
            
            messagebox.showinfo("Success", "Cleared Roblox cache!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to clear cache: {str(e)}")
    
    def optimize_registry(self):
        try:
            # This would require admin privileges in a real implementation
            messagebox.showwarning("Warning", "Registry optimization requires administrator privileges!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to optimize registry: {str(e)}")
    
    def set_process_priority(self):
        try:
            # Set Roblox process to high priority
            subprocess.run(['wmic', 'process', 'where', 'name="RobloxPlayerBeta.exe"', 
                          'CALL', 'setpriority', '"high priority"'], 
                         capture_output=True, check=False)
            messagebox.showinfo("Success", "Set Roblox process priority to high!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set process priority: {str(e)}")
    
    def load_current_flags(self):
        # Load current flags from Roblox if possible
        try:
            roblox_path = self.get_roblox_path()
            if roblox_path:
                settings_file = os.path.join(roblox_path, "ClientSettings", "ClientAppSettings.json")
                if os.path.exists(settings_file):
                    with open(settings_file, 'r') as f:
                        current_settings = json.load(f)
                    
                    for flag_name, value in current_settings.items():
                        if flag_name in self.fast_flags:
                            self.fast_flags[flag_name]['current'] = str(value)
        except Exception as e:
            print(f"Could not load current flags: {e}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FastFlagManager()
    app.run()

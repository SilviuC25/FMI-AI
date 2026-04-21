"""
Tkinter GUI for the Penguins lab.

Features:
- Load CSV (anywhere) + basic counts + random fact + ASCII penguin
- Available Data (print available_data): list all .csv in predefined directory
- Augment (augument): duplicate/create + save to auto-named file in predefined directory
- Filter: simple + advanced (filter <attribute> <value>)
- Statistics: stats, describe <attribute>, unique <attribute>
- Plots: scatter, histogram, boxplot
- Sorting: 6 algorithms
- Help: show commands and usage indications
"""

import csv
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional, List

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from repository.penguin_repository import PenguinRepository
from service.penguin_service import PenguinService, ServiceError

from exceptions.app_exceptions import (
    AppError,
    DataNotLoadedError,
    InvalidInputError,
    GUIActionError,
)

NUMERIC_FIELDS = ["culmen_length_mm", "culmen_depth_mm", "flipper_length_mm", "body_mass_g"]
TEXT_FIELDS = ["species", "island", "sex", "individual_id"]
SORT_ALGORITHMS = ["bubble", "selection", "insertion", "merge", "quick", "heap"]

DATA_DIR = "data"


def try_apply_style():
    try:
        import seaborn as sns
        sns.set(style="whitegrid")
    except Exception:
        plt.style.use("ggplot")


class PenguinGUI(tk.Frame):
    """
    Main Tkinter GUI class for the Penguins lab.
    """

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.__repo: Optional[PenguinRepository] = None
        self.__svc: Optional[PenguinService] = None
        self.__canvas = None
        self.__last_advanced_filter: Optional[List] = None
        try_apply_style()
        self.create_widgets()

    def create_widgets(self):
        """
        Builds the main widgets and tabs for the GUI.
        """
        self.master.title("Penguins Lab - Complete Analysis")
        self.pack(fill=tk.BOTH, expand=True)

        self.__notebook = ttk.Notebook(self)
        self.__notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.__tab_load = ttk.Frame(self.__notebook)
        self.__tab_available = ttk.Frame(self.__notebook)
        self.__tab_augment = ttk.Frame(self.__notebook)
        self.__tab_plots = ttk.Frame(self.__notebook)
        self.__tab_sort = ttk.Frame(self.__notebook)
        self.__tab_filter = ttk.Frame(self.__notebook)
        self.__tab_stats = ttk.Frame(self.__notebook)
        self.__tab_random = ttk.Frame(self.__notebook)
        self.__tab_research = ttk.Frame(self.__notebook)
        self.__tab_split = ttk.Frame(self.__notebook)
        self.__tab_help = ttk.Frame(self.__notebook)

        self.__notebook.add(self.__tab_load, text="Load & Info")
        self.__notebook.add(self.__tab_available, text="Available Data")
        self.__notebook.add(self.__tab_augment, text="Augment")
        self.__notebook.add(self.__tab_plots, text="Plots")
        self.__notebook.add(self.__tab_sort, text="Sorting")
        self.__notebook.add(self.__tab_filter, text="Filter")
        self.__notebook.add(self.__tab_stats, text="Statistics")
        self.__notebook.add(self.__tab_random, text="Save Random")
        self.__notebook.add(self.__tab_research, text="Research Groups")
        self.__notebook.add(self.__tab_split, text="Split Into Groups")
        self.__notebook.add(self.__tab_help, text="Help")

        self.__create_load_tab()
        self.__create_available_tab()
        self.__create_augment_tab()
        self.__create_plots_tab()
        self.__create_sort_tab()
        self.__create_filter_tab()
        self.__create_stats_tab()
        self.__create_random_tab()
        self.__create_research_tab()
        self.__create_split_tab()
        self.__create_help_tab()

    def __create_load_tab(self):
        frame = ttk.Frame(self.__tab_load, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Load CSV", command=self.__on_load).pack(pady=10)

        self.__file_label = ttk.Label(frame, text="No file loaded", foreground="gray")
        self.__file_label.pack(pady=5)

        self.__info_label = ttk.Label(frame, text="", foreground="blue")
        self.__info_label.pack(pady=10)

        self.__counts_text = tk.Text(frame, height=15, width=60)
        self.__counts_text.pack(fill=tk.BOTH, expand=True, pady=10)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Show Counts by Species", command=self.__show_counts_species).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Show Counts by Island", command=self.__show_counts_island).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Random fact", command=self.__show_random_fact).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Draw penguin", command=self.__draw_penguin).pack(side=tk.LEFT, padx=5)

    def __create_available_tab(self):
        frame = ttk.Frame(self.__tab_available, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(frame)
        top.pack(fill=tk.X)

        ttk.Label(top, text=f"Directory: {DATA_DIR}").pack(side=tk.LEFT)
        ttk.Button(top, text="Refresh", command=self.__refresh_available_data).pack(side=tk.RIGHT)

        mid = ttk.Frame(frame)
        mid.pack(fill=tk.BOTH, expand=True, pady=10)

        self.__available_list = tk.Listbox(mid, height=12)
        self.__available_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sb = ttk.Scrollbar(mid, orient=tk.VERTICAL, command=self.__available_list.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.__available_list.config(yscrollcommand=sb.set)

        bottom = ttk.Frame(frame)
        bottom.pack(fill=tk.X)

        ttk.Button(bottom, text="Load Selected", command=self.__load_selected_available).pack(side=tk.LEFT, padx=5)
        self.__available_status = ttk.Label(bottom, text="", foreground="blue")
        self.__available_status.pack(side=tk.LEFT, padx=10)

        self.__refresh_available_data()

    def __create_augment_tab(self):
        frame = ttk.Frame(self.__tab_augment, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ctrl = ttk.LabelFrame(frame, text="Augument <percent> <duplicate | create>", padding=8)
        ctrl.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(ctrl, text="Percent:").grid(row=0, column=0, padx=4, pady=4, sticky=tk.W)
        self.__augment_percent_var = tk.IntVar(value=20)
        tk.Spinbox(ctrl, from_=0, to=500, textvariable=self.__augment_percent_var, width=8).grid(
            row=0, column=1, padx=4, pady=4, sticky=tk.W
        )

        ttk.Label(ctrl, text="Mode:").grid(row=0, column=2, padx=4, pady=4, sticky=tk.W)
        self.__augment_mode_var = tk.StringVar(value="duplicate")
        ttk.Combobox(ctrl, values=["duplicate", "create"], textvariable=self.__augment_mode_var, width=12, state="readonly").grid(
            row=0, column=3, padx=4, pady=4, sticky=tk.W
        )

        ttk.Button(ctrl, text="Run Augment", command=self.__run_augment).grid(row=0, column=4, padx=10, pady=4)

        self.__augment_text = tk.Text(frame, height=14, width=90)
        self.__augment_text.pack(fill=tk.BOTH, expand=True, pady=10)

        self.__augment_status = ttk.Label(frame, text="", foreground="blue")
        self.__augment_status.pack()

    def __create_plots_tab(self):
        frame = ttk.Frame(self.__tab_plots, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ctrl_frame = ttk.LabelFrame(frame, text="Plot Controls", padding=5)
        ctrl_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(ctrl_frame, text="Scatter: X=").grid(row=0, column=0, padx=2, sticky=tk.W)
        self.__scatter_x_var = tk.StringVar(value=NUMERIC_FIELDS[0])
        ttk.Combobox(ctrl_frame, values=NUMERIC_FIELDS, textvariable=self.__scatter_x_var, width=15, state="readonly").grid(
            row=0, column=1, padx=2
        )

        ttk.Label(ctrl_frame, text="Y=").grid(row=0, column=2, padx=2, sticky=tk.W)
        self.__scatter_y_var = tk.StringVar(value=NUMERIC_FIELDS[1])
        ttk.Combobox(ctrl_frame, values=NUMERIC_FIELDS, textvariable=self.__scatter_y_var, width=15, state="readonly").grid(
            row=0, column=3, padx=2
        )

        ttk.Button(ctrl_frame, text="Plot Scatter", command=self.__plot_scatter).grid(row=0, column=4, padx=5)

        ttk.Label(ctrl_frame, text="Histogram: Field=").grid(row=1, column=0, padx=2, sticky=tk.W, pady=5)
        self.__hist_field_var = tk.StringVar(value=NUMERIC_FIELDS[3])
        ttk.Combobox(ctrl_frame, values=NUMERIC_FIELDS, textvariable=self.__hist_field_var, width=15, state="readonly").grid(
            row=1, column=1, padx=2
        )

        ttk.Label(ctrl_frame, text="Bins=").grid(row=1, column=2, padx=2, sticky=tk.W)
        self.__hist_bins_var = tk.IntVar(value=20)
        tk.Spinbox(ctrl_frame, from_=1, to=100, textvariable=self.__hist_bins_var, width=6).grid(row=1, column=3, padx=2)

        ttk.Button(ctrl_frame, text="Plot Histogram", command=self.__plot_histogram).grid(row=1, column=4, padx=5)

        ttk.Label(ctrl_frame, text="Boxplot: Field=").grid(row=2, column=0, padx=2, sticky=tk.W, pady=5)
        self.__boxplot_field_var = tk.StringVar(value=NUMERIC_FIELDS[0])
        ttk.Combobox(ctrl_frame, values=NUMERIC_FIELDS, textvariable=self.__boxplot_field_var, width=15, state="readonly").grid(
            row=2, column=1, padx=2
        )

        ttk.Label(ctrl_frame, text="Group by=").grid(row=2, column=2, padx=2, sticky=tk.W)
        self.__boxplot_group_var = tk.StringVar(value="species")
        ttk.Combobox(ctrl_frame, values=TEXT_FIELDS, textvariable=self.__boxplot_group_var, width=12, state="readonly").grid(
            row=2, column=3, padx=2
        )

        ttk.Button(ctrl_frame, text="Plot Boxplot", command=self.__plot_boxplot).grid(row=2, column=4, padx=5)

        self.__plot_frame = ttk.Frame(frame)
        self.__plot_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.__plot_status = ttk.Label(frame, text="Ready", foreground="blue")
        self.__plot_status.pack()

    def __create_sort_tab(self):
        frame = ttk.Frame(self.__tab_sort, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ctrl = ttk.LabelFrame(frame, text="Sorting Options", padding=5)
        ctrl.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(ctrl, text="Field:").pack(side=tk.LEFT, padx=2)
        self.__sort_field_var = tk.StringVar(value=NUMERIC_FIELDS[0])
        ttk.Combobox(ctrl, values=NUMERIC_FIELDS + TEXT_FIELDS, textvariable=self.__sort_field_var, width=18, state="readonly").pack(
            side=tk.LEFT, padx=2
        )

        ttk.Label(ctrl, text="Algorithm:").pack(side=tk.LEFT, padx=2)
        self.__sort_algo_var = tk.StringVar(value="quick")
        ttk.Combobox(ctrl, values=SORT_ALGORITHMS, textvariable=self.__sort_algo_var, width=12, state="readonly").pack(
            side=tk.LEFT, padx=2
        )

        self.__sort_reverse_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(ctrl, text="Descending", variable=self.__sort_reverse_var).pack(side=tk.LEFT, padx=5)

        ttk.Button(ctrl, text="Sort & Show", command=self.__do_sort).pack(side=tk.LEFT, padx=5)

        self.__sort_frame = ttk.Frame(frame)
        self.__sort_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def __create_filter_tab(self):
        frame = ttk.Frame(self.__tab_filter, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        simple = ttk.LabelFrame(frame, text="Simple Filter (species / island / sex)", padding=5)
        simple.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(simple, text="Species:").grid(row=0, column=0, padx=2, pady=3, sticky=tk.W)
        self.__filter_species_var = tk.StringVar(value="")
        ttk.Entry(simple, textvariable=self.__filter_species_var, width=20).grid(row=0, column=1, padx=2)

        ttk.Label(simple, text="Island:").grid(row=0, column=2, padx=2, sticky=tk.W)
        self.__filter_island_var = tk.StringVar(value="")
        ttk.Entry(simple, textvariable=self.__filter_island_var, width=20).grid(row=0, column=3, padx=2)

        ttk.Label(simple, text="Sex:").grid(row=1, column=0, padx=2, pady=3, sticky=tk.W)
        self.__filter_sex_var = tk.StringVar(value="")
        ttk.Entry(simple, textvariable=self.__filter_sex_var, width=20).grid(row=1, column=1, padx=2)

        ttk.Button(simple, text="Apply Simple Filter", command=self.__do_filter_simple).grid(row=1, column=3, padx=5, pady=5)

        adv = ttk.LabelFrame(frame, text="Advanced Filter (filter <attribute> <value>)", padding=5)
        adv.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(adv, text="Attribute:").grid(row=0, column=0, padx=2, pady=3, sticky=tk.W)
        self.__adv_field_var = tk.StringVar(value=NUMERIC_FIELDS[0])
        ttk.Combobox(adv, values=NUMERIC_FIELDS + TEXT_FIELDS, textvariable=self.__adv_field_var, width=18, state="readonly").grid(
            row=0, column=1, padx=2
        )

        ttk.Label(adv, text="Value:").grid(row=0, column=2, padx=2, pady=3, sticky=tk.W)
        self.__adv_value_var = tk.StringVar(value="")
        ttk.Entry(adv, textvariable=self.__adv_value_var, width=20).grid(row=0, column=3, padx=2)

        ttk.Button(adv, text="Apply Advanced Filter", command=self.__do_filter_advanced).grid(row=0, column=4, padx=5)
        ttk.Button(adv, text="Save Advanced Result as CSV", command=self.__save_advanced_filter).grid(row=0, column=5, padx=5)

        self.__filter_text = tk.Text(frame, height=18, width=80)
        self.__filter_text.pack(fill=tk.BOTH, expand=True, pady=10)

        self.__filter_info = ttk.Label(frame, text="", foreground="blue")
        self.__filter_info.pack()

    def __create_stats_tab(self):
        frame = ttk.Frame(self.__tab_stats, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ctrl = ttk.LabelFrame(frame, text="Statistics & Describe", padding=5)
        ctrl.pack(fill=tk.X, padx=5, pady=5)

        self.__stats_species_var = tk.StringVar(value="")
        ttk.Label(ctrl, text="Restrict to Species:").grid(row=0, column=0, padx=2, sticky=tk.W)
        ttk.Entry(ctrl, textvariable=self.__stats_species_var, width=18).grid(row=0, column=1, padx=2)

        ttk.Button(ctrl, text="Show Stats (all numeric)", command=self.__show_stats).grid(row=0, column=2, padx=5)
        ttk.Button(ctrl, text="Average by Species", command=self.__show_avg_by_species).grid(row=0, column=3, padx=5)

        ttk.Label(ctrl, text="Describe field:").grid(row=1, column=0, padx=2, pady=5, sticky=tk.W)
        self.__describe_field_var = tk.StringVar(value=NUMERIC_FIELDS[0])
        ttk.Combobox(ctrl, values=NUMERIC_FIELDS, textvariable=self.__describe_field_var, width=18, state="readonly").grid(
            row=1, column=1, padx=2
        )
        ttk.Button(ctrl, text="Describe", command=self.__describe_field).grid(row=1, column=2, padx=5)

        ttk.Label(ctrl, text="Unique values for:").grid(row=2, column=0, padx=2, pady=5, sticky=tk.W)
        self.__unique_field_var = tk.StringVar(value="species")
        ttk.Combobox(ctrl, values=TEXT_FIELDS + NUMERIC_FIELDS, textvariable=self.__unique_field_var, width=18, state="readonly").grid(
            row=2, column=1, padx=2
        )
        ttk.Button(ctrl, text="Show Unique", command=self.__show_unique).grid(row=2, column=2, padx=5)

        self.__stats_text = tk.Text(frame, height=20, width=80)
        self.__stats_text.pack(fill=tk.BOTH, expand=True, pady=10)

    def __create_random_tab(self):
        frame = ttk.Frame(self.__tab_random, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ctrl = ttk.LabelFrame(frame, text="Save Random Penguins", padding=5)
        ctrl.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(ctrl, text="Number of Penguins:").grid(row=0, column=0, padx=2, pady=3, sticky=tk.W)
        self.__random_count_var = tk.IntVar(value=10)
        tk.Spinbox(ctrl, from_=1, to=1000, textvariable=self.__random_count_var, width=8).grid(row=0, column=1, padx=2)

        ttk.Button(ctrl, text="Save Random Penguins to CSV", command=self.__save_random_penguins).grid(row=0, column=2, padx=5)

        self.__random_status = ttk.Label(frame, text="", foreground="blue")
        self.__random_status.pack(pady=10)


    def __create_research_tab(self):
        """
        generate research groups <k>
        for this command, make sure  the loaded set contains at most 10 penguins. 
        generate and display all possible research groups of size k (k >= 3) in which there is at least
        one penguin from each species. penguins in a research group must be distinct.
        display an error messafe if no group can be generated.
        Solve using backtracking, no combinations.
        """
        frame = ttk.Frame(self.__tab_research, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ctrl = ttk.LabelFrame(frame, text="Generate Research Groups", padding=5)
        ctrl.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(ctrl, text="Group Size (k >= 3):").grid(row=0, column=0, padx=2, pady=3, sticky=tk.W)
        self.__research_size_var = tk.IntVar(value=3)
        tk.Spinbox(ctrl, from_=3, to=10, textvariable=self.__research_size_var, width=8).grid(row=0, column=1, padx=2)

        ttk.Button(ctrl, text="Generate Research Groups", command=self.__generate_research_groups).grid(row=0, column=2, padx=5)

        self.__research_text = tk.Text(frame, height=20, width=80)
        self.__research_text.pack(fill=tk.BOTH, expand=True, pady=10)

    def __create_split_tab(self):
        """
        split_into_groups <body mass threshold>

        For this command:
        - make sure the loaded file contains at most 10 penguins
        - generate all possible ways to split ALL penguins into two groups (different sizes allowed) such that:
            - each group has at least 2 penguins
            - total body_mass_g in each group <= threshold
        - display an error message if no split can be identified
        """
        frame = ttk.Frame(self.__tab_split, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ctrl = ttk.LabelFrame(frame, text="Split Into Two Groups (Body Mass Threshold)", padding=5)
        ctrl.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(ctrl, text="Body mass threshold:").grid(row=0, column=0, padx=2, pady=3, sticky=tk.W)

        self.__split_threshold_var = tk.StringVar(value="10000")
        ttk.Entry(ctrl, textvariable=self.__split_threshold_var, width=12).grid(row=0, column=1, padx=2, pady=3, sticky=tk.W)

        ttk.Button(ctrl, text="Generate Splits", command=self.__split_into_groups).grid(row=0, column=2, padx=5)

        self.__split_text = tk.Text(frame, height=20, width=80)
        self.__split_text.pack(fill=tk.BOTH, expand=True, pady=10)


    def __create_help_tab(self):
        frame = ttk.Frame(self.__tab_help, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(frame)
        top.pack(fill=tk.X)

        ttk.Button(top, text="Show Help", command=self.__show_help_text).pack(side=tk.LEFT)
        ttk.Button(top, text="Copy Help to Clipboard", command=self.__copy_help_text).pack(side=tk.LEFT, padx=8)

        self.__help_text = tk.Text(frame, height=25, width=90)
        self.__help_text.pack(fill=tk.BOTH, expand=True, pady=10)

        self.__show_help_text()

    def __ensure_service(self) -> bool:
        if not self.__svc:
            messagebox.showinfo("No data", str(DataNotLoadedError()))
            return False
        return True

    def __on_load(self):
        path = filedialog.askopenfilename(
            title="Open penguins CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            self.__repo = PenguinRepository.load_from_csv_file(path)
            self.__svc = PenguinService(self.__repo, data_dir=DATA_DIR)
            self.__file_label.config(text=path, foreground="green")
            self.__info_label.config(text=f"Loaded {len(self.__repo)} penguins successfully", foreground="green")
            self.__available_status.config(text="(refresh available data to see new files)")
        except Exception as e:
            messagebox.showerror("Load error", str(GUIActionError(f"Could not load CSV: {e}")))
            self.__info_label.config(text="Load failed", foreground="red")

    def __show_counts_species(self):
        if not self.__ensure_service():
            return
        try:
            counts = self.__svc.unique_values("species")
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not compute counts: {e}")))
            return

        self.__counts_text.delete(1.0, tk.END)
        self.__counts_text.insert(tk.END, "Counts by Species:\n\n")
        for k, v in sorted(counts.items()):
            self.__counts_text.insert(tk.END, f"{k}: {v}\n")

    def __show_counts_island(self):
        if not self.__ensure_service():
            return
        try:
            counts = self.__svc.unique_values("island")
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not compute counts: {e}")))
            return

        self.__counts_text.delete(1.0, tk.END)
        self.__counts_text.insert(tk.END, "Counts by Island:\n\n")
        for k, v in sorted(counts.items()):
            self.__counts_text.insert(tk.END, f"{k}: {v}\n")

    def __show_random_fact(self):
        try:
            messagebox.showinfo("Random penguin fact", PenguinService.random_fact())
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not show random fact: {e}")))

    def __draw_penguin(self):
        try:
            art = PenguinService.ascii_penguin()
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not draw penguin: {e}")))
            return

        self.__counts_text.delete(1.0, tk.END)
        self.__counts_text.insert(tk.END, art)

    def __refresh_available_data(self):
        if not self.__svc:
            try:
                if not os.path.isdir(DATA_DIR):
                    os.makedirs(DATA_DIR, exist_ok=True)
                self.__available_list.delete(0, tk.END)
                for fn in sorted([f for f in os.listdir(DATA_DIR) if f.lower().endswith(".csv")]):
                    self.__available_list.insert(tk.END, fn)
                self.__available_status.config(text="Loaded without service (no CSV loaded yet).")
            except Exception as e:
                messagebox.showerror("Error", str(GUIActionError(f"Could not refresh available data: {e}")))
            return

        try:
            files = self.__svc.list_available_data()
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not list available data: {e}")))
            return

        self.__available_list.delete(0, tk.END)
        for fn in files:
            self.__available_list.insert(tk.END, fn)
        self.__available_status.config(text=f"Found {len(files)} CSV file(s).")

    def __load_selected_available(self):
        sel = self.__available_list.curselection()
        if not sel:
            messagebox.showinfo("No selection", str(InvalidInputError("Select a CSV from the list.")))
            return

        filename = self.__available_list.get(sel[0])
        full_path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(full_path):
            messagebox.showerror("Error", str(GUIActionError(f"File not found: {full_path}")))
            return

        try:
            self.__repo = PenguinRepository.load_from_csv_file(full_path)
            self.__svc = PenguinService(self.__repo, data_dir=DATA_DIR)
            self.__file_label.config(text=full_path, foreground="green")
            self.__info_label.config(text=f"Loaded {len(self.__repo)} penguins successfully", foreground="green")
            self.__available_status.config(text=f"Loaded: {filename}")
        except Exception as e:
            messagebox.showerror("Load error", str(GUIActionError(f"Could not load selected file: {e}")))

    def __run_augment(self):
        if not self.__ensure_service():
            return

        try:
            percent = int(self.__augment_percent_var.get())
            if percent < 0:
                raise InvalidInputError("Percent must be >= 0.")
        except InvalidInputError as e:
            messagebox.showerror("Invalid input", str(e))
            return
        except Exception:
            messagebox.showerror("Invalid input", str(InvalidInputError("Percent must be an integer.")))
            return

        mode = self.__augment_mode_var.get().strip().lower()

        try:
            out_path = self.__svc.augment(percent, mode)
        except ServiceError as e:
            messagebox.showerror("Augment error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Augment error", str(GUIActionError(f"Augment failed: {e}")))
            return

        self.__augment_text.delete(1.0, tk.END)
        self.__augment_text.insert(tk.END, "Augment completed.\n\n")
        self.__augment_text.insert(tk.END, f"Mode: {mode}\n")
        self.__augment_text.insert(tk.END, f"Percent: {percent}\n")
        self.__augment_text.insert(tk.END, f"Saved to:\n{out_path}\n")
        self.__augment_status.config(text="Augment saved successfully.", foreground="green")
        self.__refresh_available_data()
        messagebox.showinfo("Augment", "The dataset was augumented and saved to a new file.")

    def __plot_scatter(self):
        if not self.__ensure_service():
            return
        x = self.__scatter_x_var.get()
        y = self.__scatter_y_var.get()

        try:
            xs, ys = self.__svc.measurement_pairs_for_scatter(x, y)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Scatter plot failed: {e}")))
            return

        if not xs:
            messagebox.showinfo("No data", str(GUIActionError("No valid pairs.")))
            return

        self.__clear_plot()
        fig = plt.Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.scatter(xs, ys, alpha=0.6, s=50, edgecolors="black", linewidth=0.5)
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(f"{y} vs {x}")
        ax.grid(True, alpha=0.3)

        canvas = FigureCanvasTkAgg(fig, master=self.__plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.__plot_status.config(text=f"Scatter plotted ({len(xs)} points)", foreground="green")

    def __plot_histogram(self):
        if not self.__ensure_service():
            return

        field = self.__hist_field_var.get()
        vals: List[float] = []

        try:
            for p in self.__svc.get_all():
                method = getattr(p, "get_" + field, None)
                if method:
                    v = method()
                    if v is not None:
                        vals.append(float(v))
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not build histogram values: {e}")))
            return

        if not vals:
            messagebox.showinfo("No data", str(GUIActionError("No values.")))
            return

        try:
            bins = int(self.__hist_bins_var.get())
            if bins <= 0:
                raise InvalidInputError("Bins must be > 0.")
        except InvalidInputError:
            bins = 20
        except Exception:
            bins = 20

        self.__clear_plot()
        fig = plt.Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.hist(vals, bins=bins, alpha=0.75, edgecolor="black")
        ax.set_xlabel(field)
        ax.set_ylabel("Frequency")
        ax.set_title(f"Histogram: {field}")
        ax.grid(True, alpha=0.3, axis="y")

        canvas = FigureCanvasTkAgg(fig, master=self.__plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.__plot_status.config(text=f"Histogram plotted ({len(vals)} values, bins={bins})", foreground="green")

    def __plot_boxplot(self):
        if not self.__ensure_service():
            return
        field = self.__boxplot_field_var.get()
        group_by = self.__boxplot_group_var.get()

        try:
            groups = self.__svc.group_by(group_by)
            getter = self.__svc._normalize_numeric_getter(field)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not prepare boxplot: {e}")))
            return

        data_dict = {}
        for key, penguins in groups.items():
            vals = []
            for p in penguins:
                v = getter(p)
                if v is not None:
                    vals.append(float(v))
            if vals:
                data_dict[str(key)] = vals

        if not data_dict:
            messagebox.showinfo("No data", str(GUIActionError("No valid data for boxplot.")))
            return

        self.__clear_plot()
        fig = plt.Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        labels = sorted(data_dict.keys())
        data = [data_dict[l] for l in labels]
        ax.boxplot(data, labels=labels, patch_artist=True)
        ax.set_ylabel(field)
        ax.set_title(f"{field} by {group_by}")
        ax.grid(True, alpha=0.3, axis="y")

        canvas = FigureCanvasTkAgg(fig, master=self.__plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.__plot_status.config(text="Boxplot created", foreground="green")

    def __do_sort(self):
        if not self.__ensure_service():
            return
        field = self.__sort_field_var.get()
        algo = self.__sort_algo_var.get()
        reverse = self.__sort_reverse_var.get()

        try:
            result = self.__svc.sort_by_algorithm(field, algo, reverse=reverse)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Sorting failed: {e}")))
            return

        self.__display_table(result, self.__sort_frame, f"Top 50 - {field} ({algo})")

    def __do_filter_simple(self):
        if not self.__ensure_service():
            return
        species = self.__filter_species_var.get().strip()
        island = self.__filter_island_var.get().strip()
        sex = self.__filter_sex_var.get().strip()

        try:
            result = self.__svc.get_all()
            if species:
                result = self.__svc.filter_by_species(species)
            if island:
                result = [p for p in result if p.get_island() and island.lower() in p.get_island().lower()]
            if sex:
                result = [p for p in result if p.get_sex() and p.get_sex().strip().lower() == sex.lower()]
        except ServiceError as e:
            messagebox.showerror("Filter error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Filter error", str(GUIActionError(f"Simple filtering failed: {e}")))
            return

        self.__filter_text.delete(1.0, tk.END)
        self.__filter_text.insert(
            tk.END,
            f"SIMPLE FILTER: Species={species or 'any'}, Island={island or 'any'}, Sex={sex or 'any'}\n\n"
        )
        self.__filter_text.insert(tk.END, f"Results: {len(result)} rows\n\n")
        for i, p in enumerate(result[:100], 1):
            self.__filter_text.insert(
                tk.END,
                f"{i}. {p.get_species() or 'N/A'} | {p.get_island() or 'N/A'} | {p.get_sex() or 'N/A'}\n"
            )
        self.__filter_info.config(text=f"Showing {min(len(result), 100)} of {len(result)} results")

    def __do_filter_advanced(self):
        if not self.__ensure_service():
            return
        field = self.__adv_field_var.get().strip()
        value = self.__adv_value_var.get().strip()

        try:
            if not field or not value:
                raise InvalidInputError("Choose both attribute and value.")
            result = self.__svc.filter_attribute(field, value)
        except InvalidInputError as e:
            messagebox.showinfo("Missing data", str(e))
            return
        except ServiceError as e:
            messagebox.showerror("Filter error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Filter error", str(GUIActionError(f"Advanced filtering failed: {e}")))
            return

        self.__last_advanced_filter = result
        self.__filter_text.delete(1.0, tk.END)
        self.__filter_text.insert(tk.END, f"ADVANCED FILTER: {field} with value '{value}'\n\n")
        self.__filter_text.insert(tk.END, f"Results: {len(result)} rows\n\n")
        for i, p in enumerate(result[:100], 1):
            self.__filter_text.insert(
                tk.END,
                f"{i}. {p.get_species() or 'N/A'} | {p.get_island() or 'N/A'} | {p.get_sex() or 'N/A'}\n"
            )
        self.__filter_info.config(text=f"Showing {min(len(result), 100)} of {len(result)} results (advanced filter)")

    def __save_advanced_filter(self):
        if not self.__last_advanced_filter:
            messagebox.showinfo("No data", str(GUIActionError("Run an advanced filter first.")))
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return

        headers = ["species", "island", "culmen_length_mm", "culmen_depth_mm", "flipper_length_mm", "body_mass_g", "sex"]
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                for p in self.__last_advanced_filter:
                    writer.writerow({
                        "species": p.get_species() or "",
                        "island": p.get_island() or "",
                        "culmen_length_mm": p.get_culmen_length_mm() or "",
                        "culmen_depth_mm": p.get_culmen_depth_mm() or "",
                        "flipper_length_mm": p.get_flipper_length_mm() or "",
                        "body_mass_g": p.get_body_mass_g() or "",
                        "sex": p.get_sex() or "",
                    })
            messagebox.showinfo("Saved", f"Advanced filter exported to {path}")
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not save CSV: {e}")))

    def __save_random_penguins(self):
        if not self.__ensure_service():
            return
        try:
            count = int(self.__random_count_var.get())
            if count <= 0:
                raise InvalidInputError("Count must be > 0.")
        except InvalidInputError as e:
            messagebox.showerror("Invalid input", str(e))
            return
        except Exception:
            messagebox.showerror("Invalid input", str(InvalidInputError("Count must be an integer.")))
            return

        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return

        try:
            self.__svc.save_random_penguins(count, path)
            self.__random_status.config(text=f"Saved {count} random penguins to {path}", foreground="green")
            messagebox.showinfo("Saved", f"Saved {count} random penguins to {path}")
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not save random penguins: {e}")))

    def __generate_research_groups(self):
        if not self.__ensure_service():
            return

        try:
            k = int(self.__research_size_var.get())
            if k < 3:
                raise InvalidInputError("Group size k must be >= 3.")
        except InvalidInputError as e:
            messagebox.showerror("Invalid input", str(e))
            return
        except Exception:
            messagebox.showerror("Invalid input", str(InvalidInputError("Group size k must be an integer.")))
            return

        try:
            groups = self.__svc.generate_research_groups(k)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            self.__research_text.delete(1.0, tk.END)
            return
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not generate research groups: {e}")))
            self.__research_text.delete(1.0, tk.END)
            return

        self.__research_text.delete(1.0, tk.END)

        self.__research_text.insert(tk.END, f"Generated {len(groups)} research group(s) of size k={k}\n")
        self.__research_text.insert(tk.END, "-" * 70 + "\n\n")

        for idx, grp in enumerate(groups, 1):
            species_set = sorted({p.get_species() or "N/A" for p in grp})
            self.__research_text.insert(tk.END, f"Group #{idx} | species: {', '.join(species_set)}\n")
            for p in grp:
                self.__research_text.insert(
                    tk.END,
                    f"  - {p.get_individual_id() or 'N/A'} | {p.get_species() or 'N/A'} | "
                    f"{p.get_island() or 'N/A'} | {p.get_sex() or 'N/A'}\n"
                )
            self.__research_text.insert(tk.END, "\n")
        
    def __split_into_groups(self):
        if not self.__ensure_service():
            return

        try:
            raw = self.__split_threshold_var.get().strip()
            if not raw:
                raise InvalidInputError("Threshold is required.")
            threshold = float(raw)
            if threshold <= 0:
                raise InvalidInputError("Threshold must be > 0.")
        except InvalidInputError as e:
            messagebox.showerror("Invalid input", str(e))
            return
        except Exception:
            messagebox.showerror("Invalid input", str(InvalidInputError("Threshold must be a number (e.g., 10000 or 9500.5).")))
            return

        try:
            splits = self.__svc.split_into_groups(threshold)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            self.__split_text.delete(1.0, tk.END)
            return
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not generate splits: {e}")))
            self.__split_text.delete(1.0, tk.END)
            return

        self.__split_text.delete(1.0, tk.END)
        self.__split_text.insert(tk.END, f"Found {len(splits)} valid split(s) with threshold={threshold}\n")
        self.__split_text.insert(tk.END, "-" * 70 + "\n\n")

        for idx, (g1, g2, s1, s2) in enumerate(splits, 1):
            self.__split_text.insert(tk.END, f"Split #{idx}\n")
            self.__split_text.insert(tk.END, f"  Group 1: size={len(g1)}, total_mass={s1:.2f}\n")
            for p in g1:
                self.__split_text.insert(
                    tk.END,
                    f"    - {p.get_individual_id() or 'N/A'} | {p.get_species() or 'N/A'} | mass={p.get_body_mass_g()}\n"
                )

            self.__split_text.insert(tk.END, f"  Group 2: size={len(g2)}, total_mass={s2:.2f}\n")
            for p in g2:
                self.__split_text.insert(
                    tk.END,
                    f"    - {p.get_individual_id() or 'N/A'} | {p.get_species() or 'N/A'} | mass={p.get_body_mass_g()}\n"
                )
            self.__split_text.insert(tk.END, "\n")


    def __show_stats(self):
        if not self.__ensure_service():
            return
        species = self.__stats_species_var.get().strip() or None

        try:
            self.__stats_text.delete(1.0, tk.END)
            for field in NUMERIC_FIELDS:
                stats = self.__svc.stats_for_field(field, species)
                self.__stats_text.insert(tk.END, f"\n{field}:\n")
                for k, v in stats.items():
                    self.__stats_text.insert(tk.END, f"  {k}: {v:.2f}\n" if v is not None else f"  {k}: N/A\n")
        except ServiceError as e:
            messagebox.showerror("Stats error", str(e))
        except Exception as e:
            messagebox.showerror("Stats error", str(GUIActionError(f"Could not compute stats: {e}")))

    def __show_avg_by_species(self):
        if not self.__ensure_service():
            return
        try:
            self.__stats_text.delete(1.0, tk.END)
            avg = self.__svc.average_measurements_by_species()
            for species_name, fields in sorted(avg.items()):
                self.__stats_text.insert(tk.END, f"\n{species_name}:\n")
                for field, val in fields.items():
                    if val is not None:
                        self.__stats_text.insert(tk.END, f"  {field}: {val:.2f}\n")
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not compute average by species: {e}")))

    def __describe_field(self):
        if not self.__ensure_service():
            return
        field = self.__describe_field_var.get()

        try:
            mn, mx, avg = self.__svc.describe_attribute(field)
        except ServiceError as e:
            messagebox.showerror("Describe error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Describe error", str(GUIActionError(f"Describe failed: {e}")))
            return

        self.__stats_text.delete(1.0, tk.END)
        self.__stats_text.insert(tk.END, f"describe {field}\n\nmin   = {mn:.2f}\nmax   = {mx:.2f}\nmean  = {avg:.2f}\n")

    def __show_unique(self):
        if not self.__ensure_service():
            return
        field = self.__unique_field_var.get()

        try:
            counts = self.__svc.unique_values(field)
        except ServiceError as e:
            messagebox.showerror("Unique error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Unique error", str(GUIActionError(f"Unique failed: {e}")))
            return

        self.__stats_text.delete(1.0, tk.END)
        self.__stats_text.insert(tk.END, f"unique {field}\n\n")
        for val, cnt in sorted(counts.items()):
            self.__stats_text.insert(tk.END, f"{val}: {cnt}\n")

    def __show_help_text(self):
        try:
            if self.__svc:
                txt = self.__svc.help_text()
            else:
                tmp = PenguinService(PenguinRepository(), data_dir=DATA_DIR)
                txt = tmp.help_text()
            self.__help_text.delete(1.0, tk.END)
            self.__help_text.insert(tk.END, txt)
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not build help text: {e}")))

    def __copy_help_text(self):
        try:
            txt = self.__help_text.get(1.0, tk.END)
            self.master.clipboard_clear()
            self.master.clipboard_append(txt)
            messagebox.showinfo("Help", "Help text copied to clipboard.")
        except Exception as e:
            messagebox.showerror("Error", str(GUIActionError(f"Could not copy help text: {e}")))

    def __clear_plot(self):
        for child in self.__plot_frame.winfo_children():
            child.destroy()

    def __display_table(self, penguins: List, parent, title: str):
        for child in parent.winfo_children():
            child.destroy()

        ttk.Label(parent, text=title, font=("TkDefaultFont", 10, "bold")).pack(pady=5)

        table_frame = ttk.Frame(parent)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        columns = ("species", "island", "sex", "culmen_length", "culmen_depth", "flipper_length", "body_mass")
        tree = ttk.Treeview(table_frame, columns=columns, height=15, yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        vsb.config(command=tree.yview)
        hsb.config(command=tree.xview)

        tree.column("#0", width=40)
        tree.heading("#0", text="#")
        tree.column("species", width=18, anchor=tk.CENTER)
        tree.heading("species", text="Species")
        tree.column("island", width=12, anchor=tk.CENTER)
        tree.heading("island", text="Island")
        tree.column("sex", width=8, anchor=tk.CENTER)
        tree.heading("sex", text="Sex")
        tree.column("culmen_length", width=14, anchor=tk.E)
        tree.heading("culmen_length", text="Culmen L")
        tree.column("culmen_depth", width=14, anchor=tk.E)
        tree.heading("culmen_depth", text="Culmen D")
        tree.column("flipper_length", width=14, anchor=tk.E)
        tree.heading("flipper_length", text="Flipper")
        tree.column("body_mass", width=12, anchor=tk.E)
        tree.heading("body_mass", text="Mass")

        for idx, p in enumerate(penguins[:50], 1):
            values = (
                p.get_species() or "",
                p.get_island() or "",
                p.get_sex() or "",
                f"{p.get_culmen_length_mm():.1f}" if p.get_culmen_length_mm() is not None else "",
                f"{p.get_culmen_depth_mm():.1f}" if p.get_culmen_depth_mm() is not None else "",
                f"{p.get_flipper_length_mm():.1f}" if p.get_flipper_length_mm() is not None else "",
                f"{p.get_body_mass_g():.0f}" if p.get_body_mass_g() is not None else "",
            )
            tree.insert("", tk.END, text=str(idx), values=values)

        tree.pack(fill=tk.BOTH, expand=True)
        ttk.Label(
            parent,
            text=f"Showing {min(len(penguins), 50)} of {len(penguins)} rows",
            font=("TkDefaultFont", 9, "italic")
        ).pack(pady=4)

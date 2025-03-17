import tkinter as tk
from datetime import datetime
from tkinter import ttk

from core.users.users import PersonsDB

class PersonsDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PersonsDB Manager")
        self.root.geometry("1200x800")

        self.db = PersonsDB()
        self.current_user = None

        # Create main frame with a notebook (tabbed interface)
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create left panel for user list and search
        self.left_panel = ttk.Frame(self.main_frame, width=300)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # Create search frame
        self.search_frame = ttk.LabelFrame(self.left_panel, text="Search", padding="5")
        self.search_frame.pack(fill=tk.X, padx=5, pady=5)

        # Name search
        self.name_search_var = tk.StringVar()
        ttk.Label(self.search_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_search_entry = ttk.Entry(
            self.search_frame, textvariable=self.name_search_var
        )
        self.name_search_entry.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        ttk.Button(self.search_frame, text="Search", command=self.search_by_name).grid(
            row=0, column=2
        )

        # Tag search
        self.tag_search_var = tk.StringVar()
        ttk.Label(self.search_frame, text="Tag:").grid(row=1, column=0, sticky=tk.W)
        self.tag_search_entry = ttk.Entry(
            self.search_frame, textvariable=self.tag_search_var
        )
        self.tag_search_entry.grid(row=1, column=1, sticky=tk.EW, padx=5, pady=2)

        self.tag_condition_var = tk.StringVar(value=">:0")
        ttk.Label(self.search_frame, text="Condition:").grid(
            row=2, column=0, sticky=tk.W
        )
        self.tag_condition_entry = ttk.Entry(
            self.search_frame, textvariable=self.tag_condition_var
        )
        self.tag_condition_entry.grid(row=2, column=1, sticky=tk.EW, padx=5, pady=2)
        ttk.Button(self.search_frame, text="Search", command=self.search_by_tags).grid(
            row=2, column=2
        )

        # Create user list
        self.user_list_frame = ttk.LabelFrame(
            self.left_panel, text="Users", padding="5"
        )
        self.user_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # User list with scrollbars
        self.list_scrollbar = ttk.Scrollbar(self.user_list_frame)
        self.list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.user_listbox = tk.Listbox(
            self.user_list_frame, yscrollcommand=self.list_scrollbar.set
        )
        self.user_listbox.pack(fill=tk.BOTH, expand=True)
        self.list_scrollbar.config(command=self.user_listbox.yview)

        # Bind selection event
        self.user_listbox.bind("<<ListboxSelect>>", self.on_user_select)

        # Create action buttons
        self.action_frame = ttk.Frame(self.left_panel)
        self.action_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(
            self.action_frame, text="New User", command=self.create_new_user
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            self.action_frame, text="Delete User", command=self.delete_user
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(self.action_frame, text="Save", command=self.save_user).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(
            self.action_frame, text="Refresh", command=self.refresh_user_list
        ).pack(side=tk.LEFT, padx=2)

        # Create right panel with notebook tabs
        self.right_panel = ttk.Frame(self.main_frame)
        self.right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(self.right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create tabs
        self.basic_info_tab = ttk.Frame(self.notebook, padding="10")
        self.contact_info_tab = ttk.Frame(self.notebook, padding="10")
        self.medical_info_tab = ttk.Frame(self.notebook, padding="10")
        self.employment_tab = ttk.Frame(self.notebook, padding="10")
        self.social_tab = ttk.Frame(self.notebook, padding="10")
        self.preferences_tab = ttk.Frame(self.notebook, padding="10")
        self.tags_tab = ttk.Frame(self.notebook, padding="10")
        self.utilities_tab = ttk.Frame(self.notebook, padding="10")

        self.notebook.add(self.basic_info_tab, text="Basic Info")
        self.notebook.add(self.contact_info_tab, text="Contact")
        self.notebook.add(self.medical_info_tab, text="Medical")
        self.notebook.add(self.employment_tab, text="Employment")
        self.notebook.add(self.social_tab, text="Social")
        self.notebook.add(self.preferences_tab, text="Preferences")
        self.notebook.add(self.tags_tab, text="Tags")
        self.notebook.add(self.utilities_tab, text="Utilities")

        # Set up the content for each tab
        self.setup_basic_info_tab()
        self.setup_contact_info_tab()
        self.setup_medical_info_tab()
        self.setup_employment_tab()
        self.setup_social_tab()
        self.setup_preferences_tab()
        self.setup_tags_tab()
        self.setup_utilities_tab()

        # Status bar at the bottom
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(
            self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Initially populate the user list
        self.refresh_user_list()
        self.update_status("Database loaded successfully")

    def setup_basic_info_tab(self):
        # Variables
        self.name_var = tk.StringVar()
        self.gender_var = tk.StringVar(value="M")
        self.age_var = tk.IntVar(value=25)
        self.height_var = tk.IntVar(value=170)
        self.weight_var = tk.IntVar(value=70)
        self.birth_year_var = tk.IntVar(value=datetime.now().year - 25)
        self.birth_month_var = tk.IntVar(value=1)
        self.birth_day_var = tk.IntVar(value=1)
        self.nationality_var = tk.StringVar()

        # Create form
        frame = ttk.Frame(self.basic_info_tab)
        frame.pack(fill=tk.BOTH, expand=True)

        # Name
        row = 0
        ttk.Label(frame, text="Full Name:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Entry(frame, textvariable=self.name_var, width=40).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        # Gender
        row += 1
        ttk.Label(frame, text="Gender:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Radiobutton(frame, text="Male", variable=self.gender_var, value="M").grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )
        ttk.Radiobutton(frame, text="Female", variable=self.gender_var, value="F").grid(
            row=row, column=1, sticky=tk.E, padx=5, pady=5
        )

        # Physical attributes
        row += 1
        ttk.Label(frame, text="Age:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Spinbox(frame, from_=0, to=120, textvariable=self.age_var, width=5).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        row += 1
        ttk.Label(frame, text="Height (cm):").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Spinbox(frame, from_=0, to=300, textvariable=self.height_var, width=5).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        row += 1
        ttk.Label(frame, text="Weight (kg):").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Spinbox(frame, from_=0, to=500, textvariable=self.weight_var, width=5).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        # Birth date
        row += 1
        birth_frame = ttk.Frame(frame)
        birth_frame.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        ttk.Label(frame, text="Birth Date:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Spinbox(
            birth_frame,
            from_=1900,
            to=datetime.now().year,
            textvariable=self.birth_year_var,
            width=6,
        ).pack(side=tk.LEFT, padx=2)
        ttk.Spinbox(
            birth_frame, from_=1, to=12, textvariable=self.birth_month_var, width=3
        ).pack(side=tk.LEFT, padx=2)
        ttk.Spinbox(
            birth_frame, from_=1, to=31, textvariable=self.birth_day_var, width=3
        ).pack(side=tk.LEFT, padx=2)

        # Nationality
        row += 1
        ttk.Label(frame, text="Nationality:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Entry(frame, textvariable=self.nationality_var).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        # ID and creation info
        row += 1
        self.id_label = ttk.Label(frame, text="ID: ")
        self.id_label.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        row += 1
        self.creation_date_label = ttk.Label(frame, text="Created: ")
        self.creation_date_label.grid(
            row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5
        )

        row += 1
        self.last_updated_label = ttk.Label(frame, text="Last Updated: ")
        self.last_updated_label.grid(
            row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5
        )

    def setup_contact_info_tab(self):
        # Variables
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.address_var = tk.StringVar()
        self.city_var = tk.StringVar()
        self.state_var = tk.StringVar()
        self.postal_code_var = tk.StringVar()
        self.country_var = tk.StringVar()
        self.emergency_name_var = tk.StringVar()
        self.emergency_phone_var = tk.StringVar()

        # Create form
        frame = ttk.Frame(self.contact_info_tab)
        frame.pack(fill=tk.BOTH, expand=True)

        # Contact info
        row = 0
        ttk.Label(frame, text="Email:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Entry(frame, textvariable=self.email_var, width=40).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        row += 1
        ttk.Label(frame, text="Phone:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Entry(frame, textvariable=self.phone_var, width=20).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        row += 1
        ttk.Label(frame, text="Address:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Entry(frame, textvariable=self.address_var, width=40).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        row += 1
        ttk.Label(frame, text="City:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        ttk.Entry(frame, textvariable=self.city_var, width=20).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        row += 1
        row += 1
        ttk.Label(frame, text="State:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.state_var, width=20).grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        row += 1
        ttk.Label(frame, text="Postal Code:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.postal_code_var, width=10).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        row += 1
        ttk.Label(frame, text="Country:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.country_var, width=20).grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        # Emergency contact
        row += 1
        ttk.Label(frame, text="Emergency Contact:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=10)

        row += 1
        ttk.Label(frame, text="Name:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.emergency_name_var, width=40).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        row += 1
        ttk.Label(frame, text="Phone:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.emergency_phone_var, width=20).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        # Buttons for contact actions
        row += 1
        ttk.Button(frame, text="Export Contact Card", command=self.export_contact_card).grid(
            row=row, column=0, padx=5, pady=10
        )
        ttk.Button(frame, text="Get Full Address", command=self.show_full_address).grid(
            row=row, column=1, padx=5, pady=10
        )

    def setup_medical_info_tab(self):
        # Variables
        self.blood_type_var = tk.StringVar()
        self.insurance_provider_var = tk.StringVar()
        self.insurance_policy_var = tk.StringVar()
        self.last_physical_var = tk.StringVar()

        # Lists for allergies, medications, and conditions
        self.allergies_list = []
        self.medications_list = []
        self.conditions_list = []
        self.vaccinations_dict = {}

        # Create form
        frame = ttk.Frame(self.medical_info_tab)
        frame.pack(fill=tk.BOTH, expand=True)

        # Blood type
        row = 0
        ttk.Label(frame, text="Blood Type:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        blood_types = [bt.value for bt in BloodType]
        self.blood_type_combo = ttk.Combobox(
            frame, textvariable=self.blood_type_var, values=blood_types, state="readonly"
        )
        self.blood_type_combo.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        # Insurance information
        row += 1
        ttk.Label(frame, text="Insurance Provider:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.insurance_provider_var, width=30).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        row += 1
        ttk.Label(frame, text="Policy Number:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.insurance_policy_var, width=20).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )

        row += 1
        ttk.Label(frame, text="Last Physical Exam:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.last_physical_var, width=10).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )
        ttk.Label(frame, text="(YYYY-MM-DD)").grid(row=row, column=1, sticky=tk.E, padx=5, pady=5)

        # Lists with buttons to add/remove
        row += 1
        list_frame = ttk.Frame(frame)
        list_frame.grid(row=row, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=10)

        # Allergies
        allergies_frame = ttk.LabelFrame(list_frame, text="Allergies")
        allergies_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.allergies_listbox = tk.Listbox(allergies_frame, height=6)
        self.allergies_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        allergies_btn_frame = ttk.Frame(allergies_frame)
        allergies_btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(allergies_btn_frame, text="Add", command=lambda: self.add_list_item("allergy")).pack(side=tk.LEFT)
        ttk.Button(allergies_btn_frame, text="Remove", command=lambda: self.remove_list_item("allergy")).pack(
            side=tk.LEFT
        )
        ttk.Button(allergies_btn_frame, text="Check", command=self.check_allergy).pack(side=tk.LEFT)

        # Medications
        medications_frame = ttk.LabelFrame(list_frame, text="Medications")
        medications_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.medications_listbox = tk.Listbox(medications_frame, height=6)
        self.medications_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        medications_btn_frame = ttk.Frame(medications_frame)
        medications_btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(medications_btn_frame, text="Add", command=lambda: self.add_list_item("medication")).pack(
            side=tk.LEFT
        )
        ttk.Button(medications_btn_frame, text="Remove", command=lambda: self.remove_list_item("medication")).pack(
            side=tk.LEFT
        )

        # Medical Conditions
        conditions_frame = ttk.LabelFrame(list_frame, text="Medical Conditions")
        conditions_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.conditions_listbox = tk.Listbox(conditions_frame, height=6)
        self.conditions_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        conditions_btn_frame = ttk.Frame(conditions_frame)
        conditions_btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(conditions_btn_frame, text="Add", command=lambda: self.add_list_item("condition")).pack(side=tk.LEFT)
        ttk.Button(conditions_btn_frame, text="Remove", command=lambda: self.remove_list_item("condition")).pack(
            side=tk.LEFT
        )

        # Vaccinations
        row += 1
        vaccinations_frame = ttk.LabelFrame(frame, text="Vaccinations")
        vaccinations_frame.grid(row=row, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=10)

        self.vaccinations_tree = ttk.Treeview(
            vaccinations_frame, columns=("vaccine", "date"), show="headings", height=5
        )
        self.vaccinations_tree.heading("vaccine", text="Vaccine")
        self.vaccinations_tree.heading("date", text="Date")
        self.vaccinations_tree.column("vaccine", width=150)
        self.vaccinations_tree.column("date", width=100)
        self.vaccinations_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        vacc_btn_frame = ttk.Frame(vaccinations_frame)
        vacc_btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(vacc_btn_frame, text="Add Vaccination", command=self.add_vaccination).pack(side=tk.LEFT)
        ttk.Button(vacc_btn_frame, text="Remove Vaccination", command=self.remove_vaccination).pack(side=tk.LEFT)

    def setup_employment_tab(self):
        # Variables
        self.employment_status_var = tk.StringVar()
        self.employer_var = tk.StringVar()
        self.job_title_var = tk.StringVar()
        self.start_date_var = tk.StringVar()
        self.salary_var = tk.DoubleVar(value=0.0)

        # Work history list
        self.work_history = []

        # Create form
        frame = ttk.Frame(self.employment_tab)
        frame.pack(fill=tk.BOTH, expand=True)

        # Current employment
        row = 0
        ttk.Label(frame, text="Employment Status:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        status_values = [status.value for status in EmploymentStatus]
        self.status_combo = ttk.Combobox(
            frame, textvariable=self.employment_status_var, values=status_values, state="readonly"
        )
        self.status_combo.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        row += 1
        ttk.Label(frame, text="Current Employer:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.employer_var, width=30).grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        row += 1
        ttk.Label(frame, text="Job Title:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.job_title_var, width=30).grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        row += 1
        ttk.Label(frame, text="Start Date:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.start_date_var, width=10).grid(
            row=row, column=1, sticky=tk.W, padx=5, pady=5
        )
        ttk.Label(frame, text="(YYYY-MM-DD)").grid(row=row, column=1, sticky=tk.E, padx=5, pady=5)

        row += 1
        ttk.Label(frame, text="Salary:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(frame, textvariable=self.salary_var, width=15).grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        # Work history
        row += 1
        history_frame = ttk.LabelFrame(frame, text="Work History")
        history_frame.grid(row=row, column=0, columnspan=2, sticky=tk.NSEW, padx=5, pady=10)

        self.work_history_tree = ttk.Treeview(
            history_frame, columns=("employer", "title", "start", "end"), show="headings", height=5
        )
        self.work_history_tree.heading("employer", text="Employer")
        self.work_history_tree.heading("title", text="Job Title")
        self.work_history_tree.heading("start", text="Start Date")
        self.work_history_tree.heading("end", text="End Date")
        self.work_history_tree.column("employer", width=150)
        self.work_history_tree.column("title", width=150)
        self.work_history_tree.column("start", width=100)
        self.work_history_tree.column("end", width=100)
        self.work_history_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        wh_btn_frame = ttk.Frame(history_frame)
        wh_btn_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(wh_btn_frame, text="Add Job", command=self.add_work_history).pack(side=tk.LEFT)
        ttk.Button(wh_btn_frame, text="Remove Job", command=self.remove_work_history).pack(side=tk.LEFT)

        # Experience calculation
        row += 1
        exp_frame = ttk.Frame(frame)
        exp_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=10)

        ttk.Button(exp_frame, text="Calculate Years of Experience", command=self.calculate_experience).pack(
            side=tk.LEFT
        )
        self.experience_label = ttk.Label(exp_frame, text="")
        self.experience_label.pack(side=tk.LEFT, padx=10)

    def setup_social_tab(self):
        # Variables
        self.marital_status_var = tk.StringVar()

        # Lists/Dicts for relationships and social media
        self.relationships = []
        self.social_media = {}

        # Create form
        frame = ttk.Frame(self.social_tab)
        frame.pack(fill=tk.BOTH, expand=True)

        # Marital status
        row = 0
        ttk.Label(frame, text="Marital Status:").grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        status_values = [status.value for status in MaritalStatus]
        self.marital_combo = ttk.Combobox(
            frame, textvariable=self.marital_status_var, values=status_values, state="readonly"
        )

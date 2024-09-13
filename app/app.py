import json
import shutil
import tkinter
import warnings
from collections import OrderedDict
from tkinter import filedialog, messagebox

import serial
from customtkinter import *
from PIL import Image, ImageTk
import subprocess

def start_kbd():
    subprocess.Popen(['bash', 'keyboardstart.sh'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stop_kbd():
    subprocess.Popen(['bash', 'keyboardstop.sh'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)





class App(CTk):
    
    def __init__(self):
        super().__init__()
        self.selected_ingredients = {}
        self.selected_pipes = {}
        self.option_menus = {}
        self.pb8_exists = False
        self.products = []
        self.load_products_from_json()
        self.selected_pr_ingredients = {}
        self.ingredient_id_to_name = {}
        self.selected_image_path = ""
        self.pipe_options = {
            "Pipe1": "PI1",
            "Pipe2": "PI2",
            "Pipe3": "PI3",
            "Pipe4": "PI4",
            "Pipe5": "PI5",
            "Pipe6": "PI6",
            "Pipe7": "PI7",
            "Pipe8": "PI8",
            "Pipe9": "PI9",
            "Pipe10": "PI10",
            "Pipe11": "PI11",
            "Pipe12": "PI12",
        }
        self.frame1 = CTkFrame(
            master=self,
            width=780,
            height=150,
            corner_radius=10,
            fg_color=("#111111", "#111111"),
            bg_color="transparent",
        )
        self.frame1.pack_propagate(False)
        self.frame1.pack(padx=(10, 10), pady=(10, 0), fill="x")
        self.logo = CTkLabel(
            master=self.frame1,
            text="",
            width=0,
            height=0,
            image=CTkImage(Image.open(r"new-logo.png"), size=(300, 150)),
        )
        self.logo.pack(padx=(0, 0), pady=(0, 0))
        self.frame2 = CTkFrame(
            master=self,
            bg_color=("#1f1f1f", "#1f1f1f"),
            fg_color=("#111111", "#111111"),
            height=345,
            width=225,
            corner_radius=6,
        )
        self.frame2.pack_propagate(False)
        self.frame2.pack(padx=(10, 0), pady=(10, 10), side="left", fill="both")
        self.tab1 = CTkButton(
            master=self.frame2,
            text="Find Cocktail",
            width=200,
            height=50,
            fg_color=("#8f0c04", "#8f0c04"),
            bg_color=("#111111", "#111111"),
            hover_color=("#e8000f", "#e8000f"),
            border_spacing=0,
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.show_find_cocktail_frame,
        )
        self.tab1.pack(pady=(15, 0))
        self.tab2 = CTkButton(
            master=self.frame2,
            text="All Cocktail",
            width=200,
            height=50,
            fg_color=("#111111", "#111111"),
            bg_color=("#111111", "#111111"),
            hover_color=("#e8000f", "#e8000f"),
            border_spacing=0,
            text_color=("#747474", "#747474"),
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.show_all_products_frame,
        )
        self.tab2.pack(pady=(8, 0))
        self.tab3 = CTkButton(
            master=self.frame2,
            text="Add Ingredients",
            width=200,
            height=50,
            fg_color=("#111111", "#111111"),
            bg_color=("#111111", "#111111"),
            hover_color=("#e8000f", "#e8000f"),
            border_spacing=0,
            text_color=("#747474", "#747474"),
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.show_add_ing_frame,
        )
        self.tab3.pack(pady=(8, 0))
        self.tab4 = CTkButton(
            master=self.frame2,
            text="Add Cocktail",
            width=200,
            height=50,
            fg_color=("#111111", "#111111"),
            bg_color=("#111111", "#111111"),
            hover_color=("#e8000f", "#e8000f"),
            border_spacing=0,
            text_color=("#747474", "#747474"),
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.show_product_frame,
        )
        self.tab4.pack(pady=(8, 0))
        self.frame3 = CTkFrame(
            master=self,
            bg_color=("#1f1f1f", "#1f1f1f"),
            fg_color=("#111111", "#111111"),
            height=345,
            width=635,
            corner_radius=6,
        )
        self.frame3.pack_propagate(False)
        self.frame3.pack(
            padx=(10, 10), pady=(10, 10), side="left", fill="both", expand=True
        )
        self.box1 = CTkFrame(
            master=self.frame3,
            width=615,
            height=60,
            bg_color="transparent",
            fg_color="transparent",
        )
        self.box1.pack_propagate(False)
        self.box1.pack(padx=(10, 10), pady=(10, 0), fill="x")
        self.search_ingredients = CTkEntry(
            master=self.box1,
            placeholder_text="Search Ingredients",
            width=400,
            height=50,
            border_width=0,
            fg_color=("#1f1f1f", "#1f1f1f"),
            text_color=("#ffffff", "#ffffff"),
            font=CTkFont(family="Nunito", size=15, weight="bold"),
        )
        self.search_ingredients.pack(padx=(0, 10), side="left", fill="x", expand=True)
        self.search_ingredients.bind("<KeyRelease>", self.update_ingredient_list)
        self.search_selected = CTkLabel(
            master=self.box1,
            text="Selected Ingredients : 0 / 10",
            height=0,
            bg_color="transparent",
            font=CTkFont(family="Nunito", weight="normal", size=15),
            text_color=("#ffffff", "#ffffff"),
        )
        self.search_selected.pack(padx=(10, 10), side="right")
        self.box2 = CTkFrame(
            master=self.frame3,
            width=615,
            height=24,
            bg_color="transparent",
            fg_color="transparent",
        )
        self.box2.pack_propagate(False)
        self.box2.pack(padx=(10, 10), pady=(10, 10), fill="x")
        self.serch_title = CTkLabel(
            master=self.box2,
            text="All Ingredients",
            height=0,
            bg_color="transparent",
            text_color=("#e8000f", "#e8000f"),
            font=CTkFont(family="Nunito", weight="bold", size=15),
        )
        self.serch_title.pack(padx=(5, 35), side="left")
        self.box3 = CTkScrollableFrame(
            master=self.frame3,
            orientation="vertical",
            width=593,
            height=181,
            fg_color=("#1f1f1f", "#1f1f1f"),
        )
        self.box3.pack(padx=(10, 10), pady=(0, 0), fill="both", expand=True)
        self.box3.grid_rowconfigure(0, weight=1)
        for col in range(6):
            self.box3.grid_columnconfigure(col, weight=1)
        self.load_data_from_json()
        self.box4 = CTkFrame(
            master=self.frame3,
            width=615,
            height=50,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.box4.pack_propagate(False)
        self.box4.pack(padx=(10, 10), pady=(10, 10), fill="x")
        self.box4.grid_columnconfigure(0, weight=1)
        self.box4.grid_columnconfigure(1, weight=0)
        self.box4.grid_columnconfigure(2, weight=0)
        self.add_new_ingredient = CTkButton(
            master=self.box4,
            text="Add New",
            width=200,
            height=44,
            border_spacing=0,
            fg_color=("#8f0c0e", "#8f0c0e"),
            hover_color=("#e8000f", "#e8000f"),
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.show_add_ing_frame,
        )
        self.add_new_ingredient.grid(row=0, column=0, padx=(0, 10), sticky="e")
        self.clear_button = CTkButton(
            master=self.box4,
            text="Clear All",
            width=200,
            height=44,
            border_spacing=0,
            fg_color=("#8f0c0e", "#8f0c0e"),
            hover_color=("#e8000f", "#e8000f"),
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.clear_all_selections,
        )
        self.clear_button.grid(row=0, column=1, padx=(0, 10), sticky="e")
        self.search_button = CTkButton(
            master=self.box4,
            text="Search",
            width=200,
            height=44,
            border_spacing=0,
            fg_color=("#8f0c0e", "#8f0c0e"),
            hover_color=("#e8000f", "#e8000f"),
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.show_search_product_frame,
        )
        self.search_button.grid(row=0, column=2, sticky="e")
        self.ing_frame = CTkScrollableFrame(
            master=self.frame3,
            orientation="vertical",
            width=593,
            height=310,
            bg_color=("#111111", "#111111"),
            fg_color=("#1f1f1f", "#1f1f1f"),
            corner_radius=8,
        )
        self.ing_frame.pack(padx=(10, 10), pady=(10, 10), fill="both", expand=True)
        self.ing_frame.pack_forget()
        self.ing_box1 = CTkFrame(
            master=self.ing_frame,
            width=570,
            height=50,
            corner_radius=0,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.ing_box1.pack_propagate(False)
        self.ing_box1.pack(padx=(10, 10), pady=(10, 0), fill="x")
        self.ing_id = CTkLabel(
            master=self.ing_box1,
            text="Ingredient ID : ",
            width=200,
            justify="center",
            compound="top",
            anchor="w",
            font=CTkFont(family="Nunito", size=16, weight="normal"),
            text_color=("#ffffff", "#ffffff"),
        )
        self.ing_id.pack(side="left", padx=(0, 10), pady=(0, 0))
        self.db_ing_id = CTkLabel(
            master=self.ing_box1,
            text="ID",
            width=200,
            justify="center",
            compound="top",
            anchor="w",
            font=CTkFont(family="Nunito", size=16, weight="normal"),
            text_color=("#ffffff", "#ffffff"),
        )
        self.db_ing_id.pack(
            side="left", padx=(0, 10), pady=(0, 0), fill="x", expand=True
        )
        self.ing_box2 = CTkFrame(
            master=self.ing_frame,
            width=570,
            height=50,
            corner_radius=0,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.ing_box2.pack_propagate(False)
        self.ing_box2.pack(padx=(10, 10), pady=(10, 0), fill="x")
        self.ing_name = CTkLabel(
            master=self.ing_box2,
            text="Ingredient Name : ",
            width=200,
            justify="center",
            compound="top",
            anchor="w",
            font=CTkFont(family="Nunito", size=16, weight="normal"),
            text_color=("#ffffff", "#ffffff"),
        )
        self.ing_name.pack(side="left", padx=(0, 10), pady=(0, 0))
        self.db_ing_name = CTkEntry(
            master=self.ing_box2,
            placeholder_text="Enter Name",
            width=200,
            height=46,
            border_width=1,
            text_color=("#ffffff", "#ffffff"),
            fg_color="transparent",
            bg_color="transparent",
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.db_ing_name.pack(
            side="left", padx=(0, 10), pady=(0, 0), fill="x", expand=True
        )
        self.ing_box3 = CTkFrame(
            master=self.ing_frame,
            width=570,
            height=50,
            corner_radius=0,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.ing_box3.pack_propagate(False)
        self.ing_box3.pack(padx=(10, 10), pady=(10, 0), fill="x")
        self.ing_type = CTkLabel(
            master=self.ing_box3,
            text="Ingredient Type : ",
            width=200,
            justify="center",
            compound="top",
            anchor="w",
            font=CTkFont(family="Nunito", size=16, weight="normal"),
            text_color=("#ffffff", "#ffffff"),
        )
        self.ing_type.pack(side="left")
        self.db_ing_type1 = CTkCheckBox(
            master=self.ing_box3,
            text="Liquid",
            width=0,
            height=44,
            checkbox_width=26,
            checkbox_height=26,
            border_width=1,
            corner_radius=3,
            hover_color=("#8f0c04", "#8f0c04"),
            fg_color=("#e8000f", "#e8000f"),
            command=self.type1,
            text_color=("#ffffff", "#ffffff"),
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.db_ing_type1.pack(side="left", padx=(10, 0))
        self.db_ing_type2 = CTkCheckBox(
            master=self.ing_box3,
            text="Liqueur",
            width=0,
            height=44,
            checkbox_width=26,
            checkbox_height=26,
            border_width=1,
            corner_radius=3,
            hover_color=("#8f0c04", "#8f0c04"),
            fg_color=("#e8000f", "#e8000f"),
            command=self.type2,
            text_color=("#ffffff", "#ffffff"),
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.db_ing_type2.pack(padx=(20, 0), side="left")
        self.db_ing_type3 = CTkCheckBox(
            master=self.ing_box3,
            text="Garnish",
            width=0,
            height=44,
            checkbox_width=26,
            checkbox_height=26,
            border_width=1,
            corner_radius=3,
            hover_color=("#8f0c04", "#8f0c04"),
            fg_color=("#e8000f", "#e8000f"),
            command=self.type3,
            text_color=("#ffffff", "#ffffff"),
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.db_ing_type3.pack(padx=(20, 0), side="left")
        self.ing_box4 = CTkFrame(
            master=self.ing_frame,
            width=570,
            height=50,
            corner_radius=0,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.ing_box4.pack_propagate(False)
        self.ing_box4.pack(padx=(10, 10), pady=(50, 10), fill="x", expand=True)
        self.db_ing_save = CTkButton(
            master=self.ing_box4,
            text="Save",
            width=200,
            height=44,
            fg_color=("#8f0c04", "#8f0c04"),
            bg_color="transparent",
            hover_color=("#e8000f", "#e8000f"),
            border_spacing=0,
            anchor="center",
            compound="top",
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.save_new_ingredient,
        )
        self.db_ing_save.pack(side="left")
        self.product_frame = CTkScrollableFrame(
            master=self.frame3,
            orientation="vertical",
            width=598,
            height=310,
            bg_color=("#111111", "#111111"),
            fg_color=("#1f1f1f", "#1f1f1f"),
        )
        self.product_frame.pack(padx=(10, 10), pady=(10, 10), fill="both", expand=True)
        self.product_frame.pack_forget()
        self.pf_left = CTkFrame(
            master=self.product_frame,
            width=400,
            height=820,
            bg_color=("#1f1f1f", "#1f1f1f"),
            fg_color=("#111111", "#111111"),
            corner_radius=6,
        )
        self.pf_left.pack_propagate(False)
        self.pf_left.pack(
            side="left", padx=(5, 5), pady=(5, 5), fill="both", expand=True
        )
        self.pl_box1 = CTkFrame(
            master=self.pf_left,
            width=400,
            height=50,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.pl_box1.pack_propagate(False)
        self.pl_box1.pack(padx=(10, 10), pady=(10, 10), fill="x")
        self.pl_id = CTkLabel(
            master=self.pl_box1,
            text="Product ID : ",
            width=200,
            anchor="w",
            padx=0,
            text_color=("#ffffff", "#ffffff"),
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.pl_id.pack(padx=(0, 0), side="left")
        self.db_pl_id = CTkLabel(
            master=self.pl_box1,
            text="ID",
            width=200,
            anchor="w",
            padx=0,
            text_color=("#ffffff", "#ffffff"),
            fg_color="transparent",
            bg_color="transparent",
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.db_pl_id.pack(side="left", padx=(10, 10), pady=(0, 0), fill="x")
        self.pl_box2 = CTkFrame(
            master=self.pf_left,
            width=400,
            height=50,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.pl_box2.pack_propagate(False)
        self.pl_box2.pack(padx=(10, 10), pady=(0, 10), fill="x")
        self.pl_name = CTkLabel(
            master=self.pl_box2,
            text="Product Name : ",
            width=200,
            anchor="w",
            padx=0,
            text_color=("#ffffff", "#ffffff"),
            fg_color="transparent",
            bg_color="transparent",
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.pl_name.pack(padx=(0, 0), side="left")
        self.db_pl_name = CTkEntry(
            master=self.pl_box2,
            placeholder_text="Enter Name",
            width=200,
            height=46,
            border_width=1,
            text_color=("#ffffff", "#ffffff"),
            fg_color="transparent",
            bg_color="transparent",
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.db_pl_name.pack(
            side="left", padx=(10, 10), pady=(0, 0), fill="x", expand=True
        )
        self.pl_box3 = CTkFrame(
            master=self.pf_left,
            width=400,
            height=50,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.pl_box3.pack_propagate(False)
        self.pl_box3.pack(padx=(10, 10), pady=(0, 10), fill="x")
        self.pl_img = CTkLabel(
            master=self.pl_box3,
            text="Product Image : ",
            width=200,
            anchor="w",
            padx=0,
            text_color=("#ffffff", "#ffffff"),
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.pl_img.pack(padx=(0, 0), side="left")
        self.pl_img_btn = CTkButton(
            master=self.pl_box3,
            text="Select Image",
            width=200,
            height=46,
            fg_color=("#8f0c04", "#8f0c04"),
            bg_color="transparent",
            hover_color=("#e8000f", "#e8000f"),
            border_spacing=0,
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.select_image,
        )
        self.pl_img_btn.pack(side="left", padx=(10, 0), pady=(0, 0), fill="x")
        self.db_pl_img = CTkLabel(
            master=self.pl_box3, text="", width=48, height=48, corner_radius=3
        )
        self.db_pl_img.pack(side="left", padx=(10, 10), pady=(0, 0), fill="x")
        self.pl_box4 = CTkFrame(
            master=self.pf_left,
            width=400,
            height=50,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.pl_box4.pack_propagate(False)
        self.pl_box4.pack(padx=(10, 10), pady=(0, 10), fill="x")
        self.pl_cat = CTkLabel(
            master=self.pl_box4,
            text="Product Category : ",
            width=200,
            anchor="w",
            padx=0,
            text_color=("#ffffff", "#ffffff"),
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.pl_cat.pack(padx=(0, 0), side="left")
        self.db_pl_cat = CTkComboBox(
            master=self.pl_box4,
            width=200,
            height=46,
            corner_radius=6,
            values=["Cocktail"],
            border_width=1,
            text_color=("#ffffff", "#ffffff"),
            fg_color=("#1f1f1f", "#1f1f1f"),
            bg_color=("#111111", "#111111"),
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.db_pl_cat.pack(side="left", padx=(10, 10), pady=(0, 0), fill="x")
        self.pl_box5 = CTkFrame(
            master=self.pf_left,
            width=400,
            height=125,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.pl_box5.pack_propagate(False)
        self.pl_box5.pack(padx=(10, 10), pady=(0, 10), fill="x")
        self.pl_desc = CTkLabel(
            master=self.pl_box5,
            text="Product Description : ",
            width=200,
            anchor="nw",
            padx=0,
            height=100,
            text_color=("#ffffff", "#ffffff"),
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.pl_desc.pack(side="left", padx=(0, 0), pady=(0, 0))
        self.db_pl_desc = CTkTextbox(
            master=self.pl_box5,
            width=200,
            height=100,
            border_width=1,
            text_color=("#ffffff", "#ffffff"),
            fg_color="transparent",
            bg_color="transparent",
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.db_pl_desc.pack(
            side="left", padx=(10, 10), pady=(0, 0), fill="x", expand=True
        )
        self.pl_box6 = CTkFrame(
            master=self.pf_left,
            width=400,
            height=125,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.pl_box6.pack_propagate(False)
        self.pl_box6.pack(padx=(10, 10), pady=(0, 10), fill="x")
        self.pl_htm = CTkLabel(
            master=self.pl_box6,
            text="Product How To Make : ",
            width=200,
            anchor="nw",
            padx=0,
            height=100,
            text_color=("#ffffff", "#ffffff"),
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.pl_htm.pack(side="left", padx=(0, 0), pady=(0, 0))
        self.db_pl_htm = CTkTextbox(
            master=self.pl_box6,
            width=200,
            height=100,
            border_width=1,
            text_color=("#ffffff", "#ffffff"),
            fg_color="transparent",
            bg_color="transparent",
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.db_pl_htm.pack(
            side="left", padx=(10, 10), pady=(0, 0), fill="x", expand=True
        )
        self.pl_box7 = CTkFrame(
            master=self.pf_left,
            width=400,
            height=50,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.pl_box7.pack_propagate(False)
        self.pl_box7.pack(padx=(10, 10), pady=(0, 10), fill="x", side="bottom")
        self.pl_save = CTkButton(
            master=self.pl_box7,
            text="Save",
            width=200,
            height=44,
            fg_color=("#8f0c04", "#8f0c04"),
            bg_color="transparent",
            hover_color=("#e8000f", "#e8000f"),
            border_spacing=0,
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.save_product,
        )
        self.pl_save.pack(side="left", padx=(0, 20), pady=(0, 0), fill="x")
        self.pl_clear_all = CTkButton(
            master=self.pl_box7,
            text="Clear All",
            width=200,
            height=44,
            fg_color=("#8f0c04", "#8f0c04"),
            bg_color="transparent",
            hover_color=("#e8000f", "#e8000f"),
            border_spacing=0,
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.clear_pr_checkbox_selection,
        )
        self.pl_clear_all.pack(side="left", padx=(0, 20), pady=(0, 0), fill="x")
        self.pf_right = CTkFrame(
            master=self.product_frame,
            width=180,
            height=820,
            bg_color=("#1f1f1f", "#1f1f1f"),
            fg_color=("#111111", "#111111"),
        )
        self.pf_right.pack_propagate(False)
        self.pf_right.pack(
            side="left", padx=(5, 10), pady=(5, 5), fill="both", expand=True
        )
        self.pr_box1 = CTkFrame(
            master=self.pf_right,
            width=170,
            height=30,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.pr_box1.pack_propagate(False)
        self.pr_box1.pack(padx=(10, 10), pady=(10, 0), fill="x")
        self.pr_select_ing = CTkLabel(
            master=self.pr_box1,
            text="Select Ingredients : 0 / 10",
            anchor="w",
            width=160,
            text_color=("#ffffff", "#ffffff"),
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.pr_select_ing.pack(padx=(0, 0), pady=(0, 0), fill="x")
        self.pr_box2 = CTkFrame(
            master=self.pf_right,
            width=170,
            height=50,
            fg_color="transparent",
            bg_color="transparent",
        )
        self.pr_box2.pack_propagate(False)
        self.pr_box2.pack(padx=(10, 10), pady=(0, 10), fill="x")
        self.pr_search_ing = CTkEntry(
            master=self.pr_box2,
            placeholder_text="Search Ingredient",
            border_width=1,
            width=160,
            height=46,
            text_color=("#ffffff", "#ffffff"),
            fg_color="transparent",
            bg_color="transparent",
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        self.pr_search_ing.pack(padx=(0, 0), pady=(0, 0), fill="x", expand=True)
        self.pr_search_ing.bind("<KeyRelease>", self.update_pr_ingredient_list)
        self.pr_box3 = CTkScrollableFrame(
            master=self.pf_right,
            orientation="vertical",
            width=140,
            height=220,
            fg_color=("#1f1f1f", "#1f1f1f"),
            bg_color="transparent",
        )
        self.pr_box3.pack(padx=(10, 10), pady=(0, 10), fill="both", expand=True)
        self.load_pr_data_from_json()

        self.search_product_frame = CTkScrollableFrame(
            master=self.frame3,
            orientation="vertical",
            width=600,
            height=308,
            bg_color=("#111111", "#111111"),
            fg_color=("#111111", "#111111"),
            corner_radius=8,
        )
        self.search_product_frame.pack(
            padx=(0, 0), pady=(0, 10), fill="both", expand=True
        )
        self.search_product_frame.pack_forget()
        self.btn_x = CTkFrame(
            master=self.frame3,
            width=180,
            bg_color=("#111111", "#111111"),
            fg_color=("#111111", "#111111"),
            height=60,
        )
        self.btn_x.pack_propagate(False)
        self.btn_x.pack(padx=(10, 10), pady=(10, 10), fill="x", side="bottom")
        self.btn_x.pack_forget()
        self.pd_btn1 = CTkButton(
            master=self.btn_x,
            text="Assign Pipeline",
            width=200,
            height=50,
            fg_color=("#8f0c04", "#8f0c04"),
            hover_color=("#e8000f", "#e8000f"),
            font=CTkFont(family="Nunito", size=15, slant="roman", weight="bold"),
            command=self.show_pipe,
        )
        self.pd_btn1.pack(padx=(0, 10), pady=(0, 0), side="right")
        self.pd_btn2 = CTkButton(
            master=self.btn_x,
            text="Back",
            width=200,
            height=50,
            fg_color=("#3c3c3c", "#3c3c3c"),
            hover_color=("#000000", "#000000"),
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.show_find_cocktail_frame,
        )
        self.pd_btn2.pack(padx=(10, 10), pady=(0, 0), side="right")

        self.all_products_frame = CTkScrollableFrame(
            master=self.frame3,
            orientation="vertical",
            width=600,
            height=308,
            bg_color=("#111111", "#111111"),
            fg_color=("#111111", "#111111"),
            corner_radius=8,
        )
        self.all_products_frame.pack(
            padx=(0, 0), pady=(0, 10), fill="both", expand=True
        )
        self.all_products_frame.pack_forget()
        self.all_btn_x = CTkFrame(
            master=self.frame3,
            width=180,
            bg_color=("#111111", "#111111"),
            fg_color=("#111111", "#111111"),
            height=60,
        )
        self.all_btn_x.pack_propagate(False)
        self.all_btn_x.pack(padx=(10, 10), pady=(10, 10), fill="x", side="bottom")
        self.all_btn_x.pack_forget()
        self.pd_btn1 = CTkButton(
            master=self.all_btn_x,
            text="Assign Pipeline",
            width=200,
            height=50,
            fg_color=("#8f0c04", "#8f0c04"),
            hover_color=("#e8000f", "#e8000f"),
            font=CTkFont(family="Nunito", size=15, slant="roman", weight="bold"),
            command=self.show_pipe,
        )
        self.pd_btn1.pack(padx=(0, 10), pady=(0, 0), side="right")
        self.pd_btn2 = CTkButton(
            master=self.all_btn_x,
            text="Back",
            width=200,
            height=50,
            fg_color=("#3c3c3c", "#3c3c3c"),
            hover_color=("#000000", "#000000"),
            font=CTkFont(family="Nunito", size=15, weight="bold"),
            command=self.show_find_cocktail_frame,
        )
        self.pd_btn2.pack(padx=(10, 10), pady=(0, 0), side="right")

        self.select_pipe = CTkFrame(
            master=self.frame3,
            width=620,
            height=820,
            fg_color=("#1f1f1f", "#1f1f1f"),
            bg_color=("#111111", "#111111"),
        )
        self.select_pipe.pack_propagate(False)
        self.select_pipe.pack(padx=(10, 10), pady=(10, 10), fill="both", expand=True)
        self.select_pipe.pack_forget()
        self.pipe_box = CTkFrame(
            master=self.select_pipe,
            fg_color=("#111111", "#111111"),
            bg_color=("#111111", "#111111"),
            height=400,
            width=608,
        )
        self.pipe_box.pack_propagate(False)
        self.pipe_box.pack(
            side="left", padx=(10, 10), pady=(10, 10), fill="both", expand=True
        )
        self.pb1 = CTkFrame(
            master=self.pipe_box, width=597, height=50, fg_color="transparent"
        )
        self.pb1.pack_propagate(False)
        self.pb1.pack(padx=(10, 10), pady=(10, 10), fill="x")
        self.pb_title = CTkLabel(
            master=self.pb1,
            text="Select Pipeline For Selected Ingredients",
            anchor="w",
            text_color=("#e8000f", "#e8000f"),
            bg_color="transparent",
            fg_color="transparent",
            font=CTkFont(family="Nunito", size=18, weight="bold"),
        )
        self.pb_title.pack(side="left")

    # Bind focus events for this specific entry
        self.search_ingredients.bind("<FocusIn>", self.check_focus)
        self.search_ingredients.bind("<FocusOut>", self.check_focus)

    def check_focus(self, event=None):
        if self.search_ingredients.focus_get() == self.search_ingredients:
            start_kbd()
        else:
            stop_kbd()

    def load_products_from_json(self):
        with open("products.json", "r") as file:
            self.products = json.load(file)

    def find_matching_products(self):
        # Get the IDs of the selected ingredients
        selected_ids = {
            ing_id for ing_id, selected in self.selected_ingredients.items() if selected
        }

        matching_products = []
        for product in self.products:
            # Extract main ingredient IDs for the product
            product_main_ing_ids = {
                ingredient["ING_ID"]
                for ingredient in product["PIng"]
                if ingredient["ING_Type"] == "Main"
            }

            # Check if all main ingredients are selected
            if product_main_ing_ids.issubset(selected_ids):
                matching_products.append(product)

        return matching_products

    def load_all_products(self):
        with open("products.json", "r") as file:
            self.products = json.load(file)

        for widget in self.all_products_frame.winfo_children():
            widget.destroy()

        for col in range(7):
            self.all_products_frame.grid_columnconfigure(col, weight=0)

        row = 0
        col = 0
        for product in self.products:
            product_btn = CTkButton(
                master=self.all_products_frame,
                text=product["PName"],
                image=CTkImage(Image.open(product["PImage"]), size=(200, 200)),
                compound="top",
                width=215,
                height=250,
                border_width=0,
                border_spacing=0,
                fg_color=("#000000", "#000000"),
                bg_color=("#111111", "#111111"),
                hover_color=("#8f0c04", "#8f0c04"),
                font=CTkFont(family="Nunito", size=16, weight="normal"),
                command=lambda p=product: self.send_product_serial_data(p),
            )
            product_btn.grid(row=row, column=col, padx=7, pady=7, sticky="nsew")
            col += 1
            if col >= 7:
                col = 0
                row += 1

    def display_matching_products(self):
        for widget in self.search_product_frame.winfo_children():
            widget.destroy()
        matching_products = self.find_matching_products()
        if not matching_products:
            messagebox.showerror(
                "No Match Found", "No products match the selected ingredients."
            )
            return
        for col in range(7):
            self.search_product_frame.grid_columnconfigure(col, weight=0)
        row = 0
        col = 0
        for product in matching_products:
            product_btn = CTkButton(
                master=self.search_product_frame,
                text=product["PName"],
                image=CTkImage(Image.open(product["PImage"]), size=(200, 200)),
                compound="top",
                width=215,
                height=250,
                border_width=0,
                border_spacing=0,
                fg_color=("#000000", "#000000"),
                bg_color=("#111111", "#111111"),
                hover_color=("#8f0c04", "#8f0c04"),
                font=CTkFont(family="Nunito", size=16, weight="normal"),
                command=lambda p=product: self.send_product_serial_data(p),
            )
            product_btn.grid(row=row, column=col, padx=7, pady=7, sticky="nsew")
            col += 1
            if col >= 7:
                col = 0
                row += 1

    def load_data_from_json(self):
        with open("db.json", "r") as file:
            data = json.load(file)
            self.ingredients = data[0]["data"]
            self.ingredients.sort(key=lambda ingredient: ingredient["ING_Name"].lower())
        self.display_ingredients()

    def display_ingredients(self, filter_text=""):
        for widget in self.box3.winfo_children():
            widget.destroy()
        filtered_ingredients = [
            ing
            for ing in self.ingredients
            if filter_text.lower() in ing["ING_Name"].lower()
        ]
        self.checkboxes = []
        row = 0
        col = 0
        for ing in filtered_ingredients:
            ing_id = ing["ING_ID"]
            ing_name = ing["ING_Name"]
            state = self.selected_ingredients.get(ing_id, False)
            checkbox = CTkCheckBox(
                master=self.box3,
                text=ing_name,
                width=200,
                height=40,
                checkbox_width=26,
                checkbox_height=26,
                corner_radius=3,
                border_width=1,
                hover_color=("#8f0c04", "#8f0c04"),
                fg_color=("#e8000f", "#e8000f"),
                font=CTkFont(family="Nunito", size=16, weight="normal"),
                command=self.update_selected_count,
                text_color=("#ffffff", "#ffffff"),
            )
            checkbox.grid(row=row, column=col, padx=5, pady=5)
            if state:
                checkbox.select()
            else:
                checkbox.deselect()
            self.checkboxes.append((ing_id, checkbox))
            col += 1
            if col == 5:
                col = 0
                row += 1

    def update_selected_count(self):
        selected_count = sum(self.selected_ingredients.values())
        if selected_count > 9:
            for ing_id, checkbox in self.checkboxes:
                if checkbox.get() and not self.selected_ingredients.get(ing_id, False):
                    checkbox.deselect()
                    break
            selected_count -= 1
        for ing_id, checkbox in self.checkboxes:
            self.selected_ingredients[ing_id] = checkbox.get()
        selected_count = sum(self.selected_ingredients.values())
        self.search_selected.configure(
            text=f"Selected Ingredients : {selected_count} / 10"
        )

    def update_ingredient_list(self, event):
        filter_text = self.search_ingredients.get()
        self.display_ingredients(filter_text)
        self.restore_checkbox_states()

    def restore_checkbox_states(self):
        for ing_id, checkbox in self.checkboxes:
            if self.selected_ingredients.get(ing_id, False):
                checkbox.select()
            else:
                checkbox.deselect()
        selected_count = sum(self.selected_ingredients.values())
        self.search_selected.configure(
            text=f"Selected Ingredients : {selected_count} / 10"
        )

    def clear_all_selections(self):
        for ing_id, checkbox in self.checkboxes:
            checkbox.deselect()
        self.selected_ingredients.clear()
        self.update_selected_count()

    def generate_next_id(self):
        if self.ingredients:
            last_id = max(int(ing["ING_ID"]) for ing in self.ingredients)
            return str(last_id + 1)
        else:
            return "1"

    def update_id_label(self):
        new_id = self.generate_next_id()
        self.db_ing_id.configure(text=new_id)

    def save_new_ingredient(self):
        ing_name = self.db_ing_name.get().strip()
        if not ing_name:
            messagebox.showwarning(
                "Warning", "Please enter the name of the ingredient."
            )
            return
        ing_id = self.generate_next_id()
        ing_type_liquid = self.db_ing_type1.get()
        ing_type_liqueur = self.db_ing_type2.get()
        ing_type_garnish = self.db_ing_type3.get()
        if ing_type_liquid:
            ing_type = "Liquid"
            self.db_ing_type1.select()
            self.db_ing_type2.deselect()
            self.db_ing_type3.deselect()
        elif ing_type_liqueur:
            ing_type = "Liqueur"
            self.db_ing_type1.deselect()
            self.db_ing_type2.select()
            self.db_ing_type3.deselect()
        elif ing_type_garnish:
            ing_type = "Garnish"
            self.db_ing_type1.deselect()
            self.db_ing_type2.deselect()
            self.db_ing_type3.select()
        else:
            ing_type = "Liquid"
            self.db_ing_type1.select()
            self.db_ing_type2.deselect()
            self.db_ing_type3.deselect()
        new_ingredient = {"ING_ID": ing_id, "ING_Name": ing_name, "ING_Type": ing_type}
        self.ingredients.append(new_ingredient)
        self.ingredients.sort(key=lambda ingredient: int(ingredient["ING_ID"]))
        data_to_save = [{"data": self.ingredients}]
        with open("db.json", "w") as file:
            json.dump(data_to_save, file, indent=4)
        messagebox.showinfo(
            "Success", f"Ingredient '{ing_name}' has been added successfully."
        )
        self.db_ing_name.delete(0, "end")
        self.db_ing_type1.deselect()
        self.db_ing_type2.deselect()
        self.db_ing_type3.deselect()
        ing_id1 = self.generate_next_id()
        self.db_ing_id.configure(text=ing_id1)
        self.db_ing_type1.select()

    def show_search_product_frame(self, reset_search=True):
        selected_count = sum(self.selected_ingredients.values())
        if reset_search and selected_count == 0:
            messagebox.showerror(
                "Error", "Please select at least one ingredient before searching."
            )
            return
        matching_products = (
            self.find_matching_products()
            if reset_search
            else self.find_matching_products()
        )
        if reset_search and not matching_products:
            messagebox.showerror(
                "No Match Found", "No products match the selected ingredients."
            )
            return
        self.search_product_frame.pack(
            padx=(10, 10), pady=(0, 0), fill="both", expand=True
        )
        self.btn_x.pack(padx=(10, 10), pady=(10, 10), fill="x", side="bottom")
        self.ing_frame.pack_forget()
        self.product_frame.pack_forget()
        self.all_products_frame.pack_forget()
        self.all_btn_x.pack_forget()
        self.box1.pack_forget()
        self.select_pipe.pack_forget()
        self.box2.pack_forget()
        self.box3.pack_forget()
        self.box4.pack_forget()
        self.display_matching_products()

    def show_product_frame(self):
        self.product_frame.pack(padx=(10, 10), pady=(10, 10), fill="both", expand=True)
        self.search_product_frame.pack_forget()
        self.ing_frame.pack_forget()
        self.box1.pack_forget()
        self.all_products_frame.pack_forget()
        self.all_btn_x.pack_forget()
        self.btn_x.pack_forget()
        self.select_pipe.pack_forget()
        self.box2.pack_forget()
        self.box3.pack_forget()
        self.box4.pack_forget()
        self.tab4.configure(fg_color=("#8f0c04", "#8f0c04"), text_color="white")
        self.tab1.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )
        self.tab2.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )
        self.tab3.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )
        ing_id = self.generate_next_id()
        self.db_ing_id.configure(text=ing_id)
        self.update_id_label()
        self.db_ing_type1.select()
        self.generate_product_id()

    def show_add_ing_frame(self):
        self.ing_frame.pack(padx=(10, 10), pady=(10, 10), fill="both", expand=True)
        self.search_product_frame.pack_forget()
        self.product_frame.pack_forget()
        self.box1.pack_forget()
        self.all_products_frame.pack_forget()
        self.all_btn_x.pack_forget()
        self.box2.pack_forget()
        self.btn_x.pack_forget()
        self.select_pipe.pack_forget()
        self.box3.pack_forget()
        self.box4.pack_forget()
        self.tab3.configure(fg_color=("#8f0c04", "#8f0c04"), text_color="white")
        self.tab1.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )
        self.tab2.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )
        self.tab4.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )
        ing_id = self.generate_next_id()
        self.db_ing_id.configure(text=ing_id)
        self.update_id_label()
        self.db_ing_type1.select()

    def show_find_cocktail_frame(self):
        self.product_frame.pack_forget()
        self.search_product_frame.pack_forget()
        self.select_pipe.pack_forget()
        self.all_products_frame.pack_forget()
        self.all_btn_x.pack_forget()
        self.btn_x.pack_forget()
        self.ing_frame.pack_forget()
        self.box1.pack(padx=(10, 10), pady=(10, 0), fill="x")
        self.box2.pack(padx=(10, 10), pady=(0, 10), fill="x")
        self.box3.pack(padx=(10, 10), pady=(0, 0), fill="both", expand=True)
        self.box4.pack(padx=(10, 10), pady=(10, 10), fill="x")
        self.tab1.configure(fg_color=("#8f0c04", "#8f0c04"), text_color="white")
        self.tab2.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )
        self.tab3.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )
        self.tab4.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )

    def show_all_products_frame(self):
        self.all_products_frame.pack(
            padx=(0, 0), pady=(0, 10), fill="both", expand=True
        )
        self.all_btn_x.pack(padx=(10, 10), pady=(10, 10), fill="x", side="bottom")
        self.search_product_frame.pack_forget()
        self.ing_frame.pack_forget()
        self.product_frame.pack_forget()
        self.box1.pack_forget()
        self.select_pipe.pack_forget()
        self.box2.pack_forget()
        self.box3.pack_forget()
        self.box4.pack_forget()
        self.btn_x.pack_forget()
        self.load_all_products()
        self.tab1.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )
        self.tab2.configure(fg_color=("#8f0c04", "#8f0c04"), text_color="white")
        self.tab3.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )
        self.tab4.configure(
            fg_color=("#111111", "#111111"), text_color=("#747474", "#747474")
        )

    def type1(self):
        self.db_ing_type1.select()
        self.db_ing_type2.deselect()
        self.db_ing_type3.deselect()

    def type2(self):
        self.db_ing_type1.deselect()
        self.db_ing_type2.select()
        self.db_ing_type3.deselect()

    def type3(self):
        self.db_ing_type1.deselect()
        self.db_ing_type2.deselect()
        self.db_ing_type3.select()

    def load_pr_data_from_json(self):
        with open("db.json", "r") as file:
            data = json.load(file)
            self.ingredients = data[0]["data"]
            self.ingredients.sort(key=lambda ingredient: ingredient["ING_Name"].lower())
            self.ingredient_id_to_name = {
                ing["ING_ID"]: ing["ING_Name"] for ing in self.ingredients
            }
        self.display_pr_ingredients()

    def display_pr_ingredients(self, filter_text=""):
        for widget in self.pr_box3.winfo_children():
            widget.destroy()
        filtered_ingredients = [
            ing
            for ing in self.ingredients
            if filter_text.lower() in ing["ING_Name"].lower()
        ]
        self.pr_checkboxes = []
        row = 0
        col = 0
        for ing in filtered_ingredients:
            ing_id = ing["ING_ID"]
            ing_name = ing["ING_Name"]
            state = self.selected_pr_ingredients.get(ing_id, False)
            checkbox = CTkCheckBox(
                master=self.pr_box3,
                text=ing_name,
                width=275,
                height=40,
                checkbox_width=26,
                checkbox_height=26,
                corner_radius=3,
                border_width=1,
                fg_color=("#ff0000", "#ff0000"),
                hover_color=("#eb0214", "#eb0214"),
                font=CTkFont(family="Nunito", size=16),
                command=self.update_pr_selected_count,
                text_color=("#ffffff", "#ffffff"),
            )
            checkbox.grid(row=row, column=col, padx=5, pady=5)
            if state:
                checkbox.select()
            else:
                checkbox.deselect()
            self.pr_checkboxes.append((ing_id, checkbox))
            col += 1
            if col == 2:
                col = 0
                row += 1

    def update_pr_selected_count(self):
        selected_count = sum(self.selected_pr_ingredients.values())
        if selected_count > 9:
            for ing_id, checkbox in self.pr_checkboxes:
                if checkbox.get() and not self.selected_pr_ingredients.get(
                    ing_id, False
                ):
                    checkbox.deselect()
                    break
            selected_count -= 1
        for ing_id, checkbox in self.pr_checkboxes:
            self.selected_pr_ingredients[ing_id] = checkbox.get()
        selected_count = sum(self.selected_pr_ingredients.values())
        self.pr_select_ing.configure(
            text=f"Selected Ingredients : {selected_count} / 10"
        )

    def update_pr_ingredient_list(self, event):
        filter_text = self.pr_search_ing.get()
        self.display_pr_ingredients(filter_text)
        self.restore_pr_checkbox_states()

    def restore_pr_checkbox_states(self):
        for ing_id, checkbox in self.pr_checkboxes:
            if self.selected_pr_ingredients.get(ing_id, False):
                checkbox.select()
            else:
                checkbox.deselect()
        selected_count = sum(self.selected_pr_ingredients.values())
        self.pr_select_ing.configure(
            text=f"Selected Ingredients : {selected_count} / 10"
        )

    def clear_pr_checkbox_selection(self):
        warnings.filterwarnings("ignore", category=UserWarning)
        for ing_id, checkbox in self.pr_checkboxes:
            checkbox.deselect()
        self.selected_pr_ingredients.clear()
        self.update_pr_selected_count()
        self.db_pl_name.delete(0, END)
        self.pr_search_ing.delete(0, END)
        self.update_pr_ingredient_list(None)
        self.db_pl_desc.delete("1.0", END)
        self.db_pl_htm.delete("1.0", END)
        self.db_pl_img.configure(image="")
        self.selected_image_path = ""
        self.db_pl_cat.set("Cocktail")
        self.selected_pr_ingredients.clear()
        self.pr_select_ing.configure(text="Selected Ingredients : 0 / 10")
        self.load_pr_data_from_json()

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]
        )
        if file_path:
            self.selected_image_path = file_path
            self.display_image(file_path)

    def display_image(self, file_path):
        image = Image.open(file_path)
        image = image.resize((28, 28), Image.LANCZOS)
        photo_image = ImageTk.PhotoImage(image)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.db_pl_img.configure(image=photo_image)
            self.db_pl_img.image = photo_image

    def get_selected_ingredients(self):
        selected_ingredients = []
        for ing_id, state in self.selected_pr_ingredients.items():
            if state:
                selected_ingredients.append(ing_id)
        return selected_ingredients

    def get_ingredient_details(ing_id):
        with open("db.json", "r") as db_file:
            data = json.load(db_file)
            for item in data:
                if item["ING_ID"] == ing_id:
                    return item
        return None

    def get_image_path(self):
        file_path = filedialog.askopenfilename()
        return file_path
        return filedialog.askopenfilename(
            title="Select Image",
            filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")),
        )

    def save_product(self, event=None):
        product_file_path = "product.json"
        product_list = []
        if os.path.exists(product_file_path) and os.path.getsize(product_file_path) > 0:
            with open(product_file_path, "r") as product_file:
                try:
                    product_list = json.load(product_file)
                except json.JSONDecodeError:
                    print(
                        "The product file is empty or corrupted. Initializing a new list."
                    )
                    product_list = []
        pid = len(product_list) + 1
        pname = self.db_pl_name.get()
        pimg = self.get_image_path()
        pcategory = self.db_pl_cat.get()
        pdescription = self.db_pl_desc.get("1.0", "end-1c")
        phtm = self.db_pl_htm.get("1.0", "end-1c")
        pingredients = []
        selected_ingredients = self.get_selected_ingredients()
        for ing_id in selected_ingredients:
            ingredient_details = self.get_ingredient_details(ing_id)
            if ingredient_details:
                pingredients.append(
                    {
                        "ING_ID": ing_id,
                        "ING_Name": ingredient_details["ING_Name"],
                        "ING_Type": ingredient_details["ING_Type"],
                    }
                )
        product_data = {
            "PID": pid,
            "PName": pname,
            "PImg": pimg,
            "PCategory": pcategory,
            "PDescription": pdescription,
            "PHTM": phtm,
            "PIngredients": pingredients,
        }
        product_list.append(product_data)
        with open(product_file_path, "w") as product_file:
            json.dump(product_list, product_file, indent=4)

    def generate_product_id(self):
        if os.path.exists("products.json"):
            with open("products.json", "r") as file:
                try:
                    products = json.load(file)
                except json.JSONDecodeError:
                    products = []
        else:
            products = []
        if products:
            last_product_id = max(product["PID"] for product in products)
            new_product_id = last_product_id + 1
        else:
            new_product_id = 1
        self.db_pl_id.configure(text=str(new_product_id))

    def save_product(self):
        warnings.filterwarnings("ignore", category=UserWarning)
        current_product_name = self.db_pl_name.get()
        if not current_product_name.strip():
            messagebox.showerror("Error", "Product name cannot be empty.")
            return
        if not self.selected_image_path:
            messagebox.showerror("Error", "Product image must be selected.")
            return
        current_product_category = self.db_pl_cat.get()
        if not current_product_category.strip():
            messagebox.showerror("Error", "Product category cannot be empty.")
            return
        current_product_description = self.db_pl_desc.get("1.0", END).strip()
        if not current_product_description.strip():
            messagebox.showerror("Error", "Product description cannot be empty.")
            return
        current_product_htm = self.db_pl_htm.get("1.0", END).strip()
        if not current_product_htm.strip():
            messagebox.showerror("Error", "Product 'How to Make' cannot be empty.")
            return
        selected_ingredients = []
        for ing_id, selected in self.selected_pr_ingredients.items():
            if selected:
                ing_name = self.ingredient_id_to_name.get(ing_id, "")
                ing_type = self.get_ingredient_type(ing_id)
                selected_ingredients.append(
                    {"ING_ID": ing_id, "ING_Name": ing_name, "ING_Type": ing_type}
                )
        if not selected_ingredients:
            messagebox.showerror("Error", "At least one ingredient must be selected.")
            return
        if os.path.exists("products.json"):
            with open("products.json", "r") as file:
                try:
                    products = json.load(file)
                except json.JSONDecodeError:
                    products = []
        else:
            products = []
        current_product_id = int(self.db_pl_id.cget("text"))
        if not os.path.exists("img"):
            os.makedirs("img")
        image_extension = os.path.splitext(self.selected_image_path)[1]
        new_image_path = f"img/product_{current_product_id}{image_extension}"
        shutil.copy(self.selected_image_path, new_image_path)
        new_product = {
            "PID": current_product_id,
            "PName": current_product_name,
            "PImage": new_image_path,
            "PCat": current_product_category,
            "PDesc": current_product_description,
            "PHtm": current_product_htm,
            "PIng": selected_ingredients,
        }
        products.append(new_product)
        with open("products.json", "w") as file:
            json.dump(products, file, indent=4)
        messagebox.showinfo(
            "Success", f"Product '{current_product_name}' has been added successfully."
        )
        self.generate_product_id()
        self.db_pl_name.delete(0, END)
        self.pr_search_ing.delete(0, END)
        self.update_pr_ingredient_list(None)
        self.db_pl_desc.delete("1.0", END)
        self.db_pl_htm.delete("1.0", END)
        self.db_pl_img.configure(image="")
        self.selected_image_path = ""
        self.db_pl_cat.set("Cocktail")
        self.selected_pr_ingredients.clear()
        self.pr_select_ing.configure(text="Selected Ingredients : 0 / 10")
        self.load_pr_data_from_json()

    def get_ingredient_type(self, ing_id):
        for ing in self.ingredients:
            if ing["ING_ID"] == ing_id:
                return ing["ING_Type"]
        return ""

    def show_pipe(self):
        self.current_selected_pipes = {
            ing_id: pipe_var.get() for ing_id, pipe_var in self.selected_pipes.items()
        }
        self.select_pipe.pack(padx=(10, 10), pady=(10, 10), fill="both", expand=True)
        self.product_frame.pack_forget()
        self.search_product_frame.pack_forget()
        self.ing_frame.pack_forget()
        self.box1.pack_forget()
        self.box2.pack_forget()
        self.all_products_frame.pack_forget()
        self.all_btn_x.pack_forget()
        self.btn_x.pack_forget()
        self.box3.pack_forget()
        self.box4.pack_forget()
        self.display_selected_ingredients()
        self.update_dropdown_options()

    def update_dropdown_options(self):
        selected_values = [var.get() for var in self.selected_pipes.values()]
        available_options = [
            option
            for option in self.pipe_options
            if option not in selected_values or option == "select your pipe"
        ]
        for ing_id, pipe_var in self.selected_pipes.items():
            current_value = pipe_var.get()
            option_menu = self.option_menus[ing_id]
            menu = option_menu._dropdown_menu
            menu.delete(0, "end")
            for option in available_options:
                if option not in selected_values or option == current_value:
                    menu.add_command(
                        label=option, command=lambda v=option, sv=pipe_var: sv.set(v)
                    )
            menu.configure(font=("Nunito", 20))

    def clear_selection(self, pipe_var, option_menu):
        pipe_var.set("Select Your Pipe")
        self.update_dropdown_options()

    def clear_all_selections5(self):
        for pipe_var in self.selected_pipes.values():
            pipe_var.set("Select Your Pipe")
        self.update_dropdown_options()

    def on_option_change(self, *args):
        self.update_dropdown_options()

    def display_selected_ingredients(self):
        for widget in self.pipe_box.winfo_children():
            if widget != self.pb1:
                widget.destroy()
        selected_ingredients = [
            ing
            for ing in self.ingredients
            if self.selected_ingredients.get(ing["ING_ID"], False)
        ]
        for ing in selected_ingredients:
            pb2 = CTkFrame(
                master=self.pipe_box, width=597, height=50, fg_color="transparent"
            )
            pb2.pack_propagate(False)
            pb2.pack(padx=(10, 10), pady=(0, 10), fill="x")
            pb_ing = CTkLabel(
                master=pb2,
                text=f"{ing['ING_Name']} :",
                font=CTkFont(family="Nunito", size=16, weight="normal"),
                width=150,
                anchor="w",
                padx=0,
                text_color=("#ffffff", "#ffffff"),
                fg_color="transparent",
                bg_color="transparent",
            )
            pb_ing.pack(padx=(10, 10), side="left")
            selected_pipe = StringVar()
            selected_pipe.set("Select Your Pipe")
            if ing["ING_ID"] in self.current_selected_pipes:
                selected_pipe.set(self.current_selected_pipes[ing["ING_ID"]])
            selected_pipe.trace("w", self.on_option_change)
            self.selected_pipes[ing["ING_ID"]] = selected_pipe
            pb_pipe = CTkOptionMenu(
                master=pb2,
                variable=selected_pipe,
                values=list(self.pipe_options.keys()),
                width=250,
                height=46,
                text_color=("#ffffff", "#ffffff"),
                bg_color=("#111111", "#111111"),
                fg_color=("#1f1f1f", "#1f1f1f"),
                button_color=("#8f0c04", "#8f0c04"),
                button_hover_color=("#e8000f", "#e8000f"),
                dropdown_fg_color=("#1f1f1f", "#1f1f1f"),
                dropdown_hover_color=("#8f0c04", "#8f0c04"),
                dropdown_text_color=("#ffffff", "#ffffff"),
                font=CTkFont(family="Nunito", size=16, weight="normal"),
            )
            pb_pipe.pack(padx=(10, 10), side="left")
            self.clx = CTkButton(
                master=pb2,
                text="",
                width=46,
                height=46,
                image=CTkImage(
                    Image.open(r"img/reset.png"),
                    size=(28, 28),
                ),
                corner_radius=6,
                fg_color=("#8f0c04", "#8f0c04"),
                bg_color=("#111111", "#111111"),
                hover_color=("#e8000f", "#e8000f"),
                command=lambda sv=selected_pipe, om=pb_pipe: self.clear_selection(
                    sv, om
                ),
            )
            self.clx.pack(padx=(10, 10), side="left")
            self.option_menus[ing["ING_ID"]] = pb_pipe
        self.update_dropdown_options()
        if not self.pb8_exists:
            self.pb8 = CTkFrame(
                master=self.pipe_box, width=597, height=60, fg_color="transparent"
            )
            self.pb8.pack_propagate(False)
            self.pb8.pack(
                padx=(10, 10),
                pady=(10, 10),
                fill="x",
                side="bottom",
            )
            self.pb_btn = CTkButton(
                master=self.pb8,
                text="Serial Out",
                width=200,
                height=50,
                fg_color=("#8f0c04", "#8f0c04"),
                hover_color=("#e8000f", "#e8000f"),
                font=CTkFont(family="Nunito", size=15, slant="roman", weight="bold"),
                command=self.serial_out,
            )
            self.pb_btn.pack(side="right")
            self.pb_btn2 = CTkButton(
                master=self.pb8,
                text="Back",
                width=200,
                height=50,
                fg_color=("#3c3c3c", "#3c3c3c"),
                hover_color=("#000000", "#000000"),
                font=CTkFont(family="Nunito", size=15, slant="roman", weight="bold"),
                command=lambda: self.show_search_product_frame(reset_search=False),
            )
            self.pb_btn2.pack(side="right", padx=(10, 10))
            self.pb_btn3 = CTkButton(
                master=self.pb8,
                text="Clear All",
                width=200,
                height=50,
                fg_color=("#8f0c04", "#8f0c04"),
                hover_color=("#e8000f", "#e8000f"),
                font=CTkFont(family="Nunito", size=15, slant="roman", weight="bold"),
                command=self.clear_all_selections5,
            )
            self.pb_btn3.pack(side="left", padx=(10, 10))

    def validate_pipes_assignment(self):
        for ing_id in self.selected_ingredients:
            if self.selected_ingredients[ing_id]:
                pipe_selection = self.selected_pipes.get(ing_id, None)
                if not pipe_selection or pipe_selection.get() == "Select Your Pipe":
                    ingredient_name = next(
                        (
                            ing["ING_Name"]
                            for ing in self.ingredients
                            if ing["ING_ID"] == ing_id
                        ),
                        "Unknown Ingredient",
                    )
                    messagebox.showerror(
                        "Pipe Assignment Error",
                        f"Please assign a valid pipe for ingredient '{ingredient_name}'.",
                    )
                    return False
        return True

    def serial_out(self):
        matching_products = self.find_matching_products()
        selected_pipelines = {}
        for ing_id, pipe_var in self.selected_pipes.items():
            if self.selected_ingredients.get(ing_id, False):
                pipe_selection = pipe_var.get()
                if (
                    pipe_selection == "Select Your Pipe"
                    or pipe_selection not in self.pipe_options
                ):
                    ingredient_name = next(
                        (
                            ing["ING_Name"]
                            for ing in self.ingredients
                            if ing["ING_ID"] == ing_id
                        ),
                        "Unknown Ingredient",
                    )
                    messagebox.showerror(
                        "Selection Error",
                        f"Please select a valid pipe for ingredient '{ingredient_name}'.",
                    )
                    return
                selected_pipelines[ing_id] = self.pipe_options.get(pipe_selection)
        if not selected_pipelines:
            messagebox.showerror(
                "Selection Error", "No valid pipes selected for any ingredients."
            )
            return
        if not matching_products:
            messagebox.showerror(
                "No Match Found", "No products match the selected ingredients."
            )
            return
        self.show_search_product_frame(reset_search=False)

    def show_product_selection_popup(self, matching_products, selected_pipelines):
        popup = tkinter.Toplevel()
        popup.title("Select Product")
        selected_product = tkinter.StringVar()
        selected_product.set("Select a Product")
        product_names = [product["PName"] for product in matching_products]
        product_option_menu = CTkOptionMenu(
            master=popup,
            variable=selected_product,
            values=product_names,
            width=250,
            height=46,
            text_color=("#ffffff", "#ffffff"),
            bg_color=("#F0F0F0", "#F0F0F0"),
            fg_color=("#1f1f1f", "#1f1f1f"),
            button_color=("#8f0c04", "#8f0c04"),
            button_hover_color=("#e8000f", "#e8000f"),
            dropdown_fg_color=("#1f1f1f", "#1f1f1f"),
            dropdown_hover_color=("#8f0c04", "#8f0c04"),
            dropdown_text_color=("#ffffff", "#ffffff"),
            font=CTkFont(family="Nunito", size=16, weight="normal"),
        )
        product_option_menu.pack(padx=10, pady=10)
        confirm_button = CTkButton(
            master=popup,
            text="Send",
            command=lambda: self.confirm_product_selection(
                selected_product.get(), matching_products, selected_pipelines, popup
            ),
            width=150,
            height=40,
            bg_color=("#F0F0F0", "#F0F0F0"),
            fg_color=("#8f0c04", "#8f0c04"),
            hover_color=("#e8000f", "#e8000f"),
        )
        confirm_button.pack(padx=10, pady=10)

    def confirm_product_selection(
        self, selected_product_name, matching_products, selected_pipelines, popup
    ):
        if selected_product_name == "Select a Product":
            messagebox.showerror("Selection Error", "Please select a product.")
            return
        selected_product = next(
            (
                product
                for product in matching_products
                if product["PName"] == selected_product_name
            ),
            None,
        )
        if not selected_product:
            messagebox.showerror("Selection Error", "Selected product not found.")
            return
        product_id = selected_product["PID"]
        pipelines_str = ", ".join(
            f"{pipe}" for ing_id, pipe in selected_pipelines.items()
        )
        serial_data = f"Product ID: {product_id}, Pipelines: {pipelines_str}"
        popup.destroy()
        self.send_serial_data(serial_data)

    def send_serial_data(self, serial_data):
        if not self.validate_pipes_assignment():
            return

        print(f"Serial Data to be sent: {serial_data}")
        try:
            ser = serial.Serial(
                "/dev/ttyS0", 9600, timeout=1
            )  # Adjust COM3 - /dev/ttyUSB0 - /dev/ttyS0 port and baud rate
            ser.write(serial_data.encode("utf-8"))
            ser.close()
            messagebox.showinfo("Success", "Data sent successfully.")
        except serial.SerialException as e:
            messagebox.showerror("Serial Error", str(e))

    def send_product_serial_data(self, product):
        if not self.validate_pipes_assignment():
            return

        selected_pipelines = {}
        for ing_id, pipe_var in self.selected_pipes.items():
            if self.selected_ingredients.get(ing_id, False):
                pipe_selection = pipe_var.get()
                if (
                    pipe_selection == "Select Your Pipe"
                    or pipe_selection not in self.pipe_options
                ):
                    ingredient_name = next(
                        (
                            ing["ING_Name"]
                            for ing in self.ingredients
                            if ing["ING_ID"] == ing_id
                        ),
                        "Unknown Ingredient",
                    )
                    messagebox.showerror(
                        "Selection Error",
                        f"Please select a valid pipe for ingredient '{ingredient_name}'.",
                    )
                    return
                selected_pipelines[ing_id] = self.pipe_options.get(pipe_selection)

        if not selected_pipelines:
            messagebox.showerror(
                "Selection Error", "No valid pipes selected for any ingredients."
            )
            return

        product_id = product["PID"]
        pipelines_str = ", ".join(
            f"{pipe}" for ing_id, pipe in selected_pipelines.items()
        )
        serial_data = f"Product : {product_id}, Pipelines: {pipelines_str}"
        self.send_serial_data(serial_data)


set_default_color_theme("dark-blue")
app = App()
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(f"{screen_width}x{screen_height}")
app.title("Cocktail Order Management By MigArch")
app.configure(fg_color=["#1f1f1f", "#1f1f1f"])
app.mainloop()

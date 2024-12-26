import tkinter
import tkinter.ttk
from tkinter import filedialog, ttk, messagebox, font, Radiobutton, StringVar, IntVar
import PIL
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
import pandas
import random
import matplotlib.pyplot as plt
import itertools
import os


class GuiWatermark(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.title("Watermark.")
        self.config(padx=70, pady=70)

        self.game_label = tkinter.Label(text="Please upload a file and select some options for the watermark.\n")
        self.game_label.grid(column=0, columnspan=3, row=0)

        self.upload_file = tkinter.Button(text="Upload File", command=self.upload_file)
        self.upload_file.grid(column=1, row=1)

        self.filename = None

        self.file_location = tkinter.Label(text="No file selected.\n", wraplength=400, justify='center')
        self.file_location.grid(column=0, columnspan=3, row=2, rowspan=2)

        self.watermark_text = tkinter.Label(text="Text for watermark:")
        self.watermark_text.grid(column=0, columnspan=1, row=4)

        self.text_entry = tkinter.Entry(width=40)
        self.text_entry.grid(column=1, columnspan=2, row=4)

        self.font_text = tkinter.Label(text="Font and size:")
        self.font_text.grid(column=0, columnspan=1, row=5)

        self.font_list = os.listdir('fonts')
        self.font_list = ['--Select or Random--'] + [item.replace('.ttf', '') for item in self.font_list]

        self.font_combo = tkinter.ttk.Combobox(values=self.font_list, state='readonly', width=25)
        self.font_combo.current(0)
        self.font_combo.grid(column=1, columnspan=1, row=5)

        size_range = list(itertools.chain(range(1, 21), range(25, 501, 25)))
        self.fontsize_combo = tkinter.ttk.Combobox(values=size_range, state='readonly', width=5)
        self.fontsize_combo.current(25)
        self.fontsize_combo.grid(column=2, columnspan=1, row=5)

        self.dataframe = pandas.read_csv("waterprint_app_data.csv")
        color_names = ['--Select or Random--'] + list(self.dataframe['color'])

        self.full_color_dict = {}
        for (index, row) in self.dataframe.iterrows():
            self.full_color_dict.update({row.color: {'r': row.r, 'g': row.g, 'b': row.b}})

        self.color_text = tkinter.Label(text="Color:")
        self.color_text.grid(column=0, columnspan=1, row=6)

        self.color_combo = tkinter.ttk.Combobox(values=color_names, state='readonly', width=20)
        self.color_combo.current(0)
        self.color_combo.grid(column=1, columnspan=1, row=6)
        self.color_combo.bind('<<ComboboxSelected>>', self.fill_rgb)

        self.shuffle_button = tkinter.Button(text='Shuffle', command=self.shuffle_colors)
        self.shuffle_button.grid(column=2, columnspan=1, row=6)

        self.custcolor_text = tkinter.Label(text="Customize color:")
        self.custcolor_text.grid(column=0, columnspan=1, row=7)

        self.cust_red_text = tkinter.Label(text="Red (R):")
        self.cust_red_text.grid(column=1, columnspan=1, row=7)

        self.red_entry = tkinter.Entry(width=20)
        self.red_entry.grid(column=2, columnspan=1, row=7)

        self.cust_green_text = tkinter.Label(text="Green (G):")
        self.cust_green_text.grid(column=1, columnspan=1, row=8)

        self.green_entry = tkinter.Entry(width=20)
        self.green_entry.grid(column=2, columnspan=1, row=8)

        self.cust_blue_text = tkinter.Label(text="Blue (B):")
        self.cust_blue_text.grid(column=1, columnspan=1, row=9)

        self.blue_entry = tkinter.Entry(width=20)
        self.blue_entry.grid(column=2, columnspan=1, row=9)

        self.transp_label = tkinter.Label(text="Opacity:")
        self.transp_label.grid(column=0, columnspan=1, row=10)

        self.transp_variable = IntVar()
        self.transp_scale = tkinter.Scale(orient='horizontal', from_=0, to=255, variable=self.transp_variable)
        self.transp_scale.set(125)
        self.transp_scale.grid(column=1, columnspan=1, row=10)

        self.shuffle_colors()

        self.coord_variable = StringVar()

        self.alignment_label = tkinter.Label(text="\nAlignment within picture:")
        self.alignment_label.grid(column=0, columnspan=1, row=11)

        self.nw_button = Radiobutton(text="Top left", value='nw', variable=self.coord_variable)
        self.nw_button.grid(column=0, columnspan=1, row=12)

        self.n_button = Radiobutton(text="Top", value='n', variable=self.coord_variable)
        self.n_button.grid(column=1, columnspan=1, row=12)

        self.ne_button = Radiobutton(text="Top right", value='ne', variable=self.coord_variable)
        self.ne_button.grid(column=2, columnspan=1, row=12)

        self.w_button = Radiobutton(text="Left", value='w', variable=self.coord_variable)
        self.w_button.grid(column=0, columnspan=1, row=13)

        self.c_button = Radiobutton(text="Center", value='c', variable=self.coord_variable)
        self.c_button.select()
        self.c_button.grid(column=1, columnspan=1, row=13)

        self.e_button = Radiobutton(text="Right", value='e', variable=self.coord_variable)
        self.e_button.grid(column=2, columnspan=1, row=13)

        self.sw_button = Radiobutton(text="Bottom left", value='sw', variable=self.coord_variable)
        self.sw_button.grid(column=0, columnspan=1, row=14)

        self.s_button = Radiobutton(text="Bottom", value='s', variable=self.coord_variable)
        self.s_button.grid(column=1, columnspan=1, row=14)

        self.se_button = Radiobutton(text="Bottom right", value='se', variable=self.coord_variable)
        self.se_button.grid(column=2, columnspan=1, row=14)

        self.dict_alignment = {'nw': {'x': 0, 'y': 0}, 'n': {'x': 1/3, 'y': 0}, 'ne': {'x': 2/3, 'y': 0},
                               'w': {'x': 0, 'y': 1/3}, 'c': {'x': 1/3, 'y': 1/3}, 'e': {'x': 2/3, 'y': 1/3},
                               'sw': {'x': 0, 'y': 2/3}, 's': {'x': 1/3, 'y': 2/3}, 'se': {'x': 2/3, 'y': 2/3},
                               }

        self.ghost_label = tkinter.Label(text="")
        self.ghost_label.grid(column=1, columnspan=1, row=15)

        self.reset_button = tkinter.Button(text="Reset", command=self.reset)
        self.reset_button.grid(column=1, row=16)

        self.process_button = tkinter.Button(text="Process Watermark", command=self.check_input)
        self.process_button.grid(column=2, row=16)

        self.mainloop()

    def fill_rgb(self, event):
        this_color = self.color_combo.get()
        try:
            this_rgb = self.full_color_dict[this_color]
        except KeyError:
            self.shuffle_colors()
            this_rgb = {'r': self.red_entry.get(),
                        'g': self.green_entry.get(),
                        'b': self.blue_entry.get()}

        self.red_entry.delete(0, 10)
        self.green_entry.delete(0, 10)
        self.blue_entry.delete(0, 10)

        self.red_entry.insert(0, this_rgb['r'])
        self.green_entry.insert(0, this_rgb['g'])
        self.blue_entry.insert(0, this_rgb['b'])

    def upload_file(self):
        self.filename = filedialog.askopenfilename()
        self.file_location.config(text=f'{self.filename}\n')

    def shuffle_colors(self):
        self.red_entry.delete(0, 'end')
        self.green_entry.delete(0, 'end')
        self.blue_entry.delete(0, 'end')
        self.red_entry.insert(0, random.randint(0, 255))
        self.green_entry.insert(0, random.randint(0, 255))
        self.blue_entry.insert(0, random.randint(0, 255))

    def reset(self):
        self.filename = None
        self.file_location.config(text='No file selected.\n')
        self.text_entry.delete(0, 'end')
        self.font_combo.current(0)
        self.color_combo.current(0)
        self.transp_scale.set(125)

        self.c_button.select()

        self.cust_red_text = tkinter.Label(text="Red (R):")
        self.cust_red_text.grid(column=1, columnspan=1, row=7)

        self.shuffle_colors()

    def check_input(self):
        if self.red_entry.get() == '':
            self.red_entry.insert(0, 0)
        if self.green_entry.get() == '':
            self.green_entry.insert(0, 0)
        if self.blue_entry.get() == '':
            self.blue_entry.insert(0, 0)

        if self.filename is None:
            messagebox.showerror('No file selected',
                                 "You haven't selected any files to add watermark to.")
        elif self.text_entry.get() == '':
            messagebox.showerror('No text inserted',
                                 "You haven't typed in any text to add to the image.")

        elif (self.red_entry.get().isdecimal() is False or
              self.green_entry.get().isdecimal() is False or
              self.blue_entry.get().isdecimal() is False):
            messagebox.showerror('Invalid format.',
                                 "Each color parameter must be a number.")

        elif (int(self.red_entry.get()) not in range(0, 256) or
              int(self.green_entry.get()) not in range(0, 256) or
              int(self.blue_entry.get()) not in range(0, 256)):
            messagebox.showerror('Invalid RGB color values',
                                 "Each color parameter must range between 0 and 255.")
        else:
            try:
                Image.open(self.filename)
                self.process_picture()
            except UnidentifiedImageError:
                messagebox.showerror('Unsupported image type.',
                                     "Please try with supported image types such as:\n"
                                     "JPEG, PNG, BMP, GIF, TIFF, and PPM.")

    def process_picture(self):

        def pic_alignment(w_, h_):
            coords = self.dict_alignment[self.coord_variable.get()]
            return int(w_ * coords['x']), int(h_ * coords['y'])

        plt.close()

        red = int(self.red_entry.get())
        green = int(self.green_entry.get())
        blue = int(self.blue_entry.get())
        transp = self.transp_variable.get()
        colors = (red, green, blue, transp)
        text = self.text_entry.get()
        font_ = self.font_combo.get()
        font_size = int(self.fontsize_combo.get())
        while font_ == '--Select or Random--':
            font_ = random.choice(self.font_list)

        image = Image.open(self.filename)
        image = image.convert('RGBA')
        w, h = image.size
        x, y = pic_alignment(w, h)

        txt = Image.new('RGBA', image.size, (255, 255, 255, 0))

        font_ = ImageFont.truetype(f"fonts/{font_}.ttf", font_size)

        draw = ImageDraw.Draw(txt)
        draw.text((x, y), text=text, fill=colors, font=font_)

        combined = Image.alpha_composite(image, txt)

        plt.imshow(combined)
        plt.axis('off')

        fig = plt.gcf()
        fig.show()

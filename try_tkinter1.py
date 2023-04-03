import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Laser Testing Utility")

# Add a class to style the tkinter widgets
style = ttk.Style()
style.configure('TEntry', foreground = 'red')


# Define a function to change the text color
# def change_color():
#    text.configure(background="red")

# Section 1
logo = ttk.Label(root, text="Logo")
title = ttk.Label(root, text="Laser Testing Utility", font=("Helvetica", 18, "bold"))
version = ttk.Label(root, text="Ver 1.00", font=("Helvetica", 8))
spec_version = ttk.Label(root, text="Spec. Ver 0.01", font=("Helvetica", 8))
logo.grid(row=0, column=0, padx=10)
title.grid(row=0, column=1, padx=10)
version.grid(row=1, column=1, padx=10)
spec_version.grid(row=2, column=1, padx=10)

# Section 2
unit_label = ttk.Label(root, text="Unit Under Test")
unit_label.grid(row=3, column=0, columnspan=3, pady=10)

# Section 2.1
brand_frame = ttk.LabelFrame(root, text="Laser Brand")
brand_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ns")
brand_var = tk.StringVar()
brand_var.set("Laser 111")
brand_rb1 = ttk.Radiobutton(brand_frame, text="Laser 111", variable=brand_var, value="Laser 111")
brand_rb2 = ttk.Radiobutton(brand_frame, text="Laser 222", variable=brand_var, value="Laser 222")
brand_rb3 = ttk.Radiobutton(brand_frame, text="Laser 333", variable=brand_var, value="Laser 333")
brand_rb1.grid(row=0, column=0, pady=5)
brand_rb2.grid(row=1, column=0, pady=5)
brand_rb3.grid(row=2, column=0, pady=5)


root.mainloop()

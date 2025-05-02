import tkinter as tk
import numpy as np

def calculate_result(entries):
    try:
        values = [float(entry.get()) for entry in entries]
        result = np.sum(values)
        result_label.config(text=f"Result: {result}")
    except ValueError:
        result_label.config(text="Please enter valid numbers")

def main():
    root = tk.Tk()
    root.title("Input Window")

    entries = []
    for i in range(4):
        entry = tk.Entry(root)
        entry.pack()
        entries.append(entry)

    calculate_button = tk.Button(root, text="Calculate", command=lambda: calculate_result(entries))
    calculate_button.pack()

    global result_label
    result_label = tk.Label(root, text="Result: ")
    result_label.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
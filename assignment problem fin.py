import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
def get_matrix_size():
    size = int(size_entry.get())
    return size

def sum_zero_cells(original_matrix, result_matrix):
    size = len(original_matrix)
    total_cost = 0

    for i in range(size):
        j = size -1
        while True:
            if result_matrix[i][j] == 0:
                original_value = original_matrix[i][j]
                total_cost += original_value
                break  # Stop at the first zero in each row
            j -= 1
    return total_cost

def sum_zero_cells_Details(original_matrix, result_matrix):
    size = len(original_matrix)
    total_cost = []
    for i in range(size):
        j = size -1 
        while True:
            if result_matrix[i][j] == 0:
                original_value = original_matrix[i][j]
                total_cost.append(original_value)
                total_cost.append("+")
                break  # Stop at the first zero in each row
            j -= 1
            
    return total_cost

def get_matrix_values(size):
    matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            value = int(matrix_entries[i][j].get())
            row.append(value)
        matrix.append(row)
    return matrix

def print_matrix(matrix):
    output_text.insert(tk.END, '\n'.join([' '.join(map(str, row)) for row in matrix]) + '\n')
    output_text.insert(tk.END, "============================" '\n')
def get_row_min(row):
    return min(row)

def get_column_min(matrix, col):
    return min([row[col] for row in matrix])

def subtract_row(matrix, row, value):
    new_row = [cell - value for cell in row]
    matrix[matrix.index(row)] = new_row

def subtract_column(matrix, col, value):
    for row in matrix:
        row[col] -= value

def subtract_smallest_top_right(matrix):
    size = len(matrix)
    flag = 0
    for row in matrix[2:]:
        for element in row:
            if element != 0:
                flag = 1
    for row in matrix:
        for element in row[:-2]:
            if element != 0:
                flag = 1
    
    if flag == 0 and matrix[0][-1] != 0  and matrix[1][-1] != 0 and matrix[0][-2] != 0 and matrix[1][-2] != 0 and size == 3:
        smallest = min(matrix[0][-1], matrix[1][-1], matrix[0][-2], matrix[1][-2])
        matrix[0][-1] -= smallest
        matrix[1][-1] -= smallest
        matrix[0][-2] -= smallest
        matrix[1][-2] -= smallest
    return matrix

def calculate_assignment():
    size = get_matrix_size()
    original_matrix = get_matrix_values(size)
    original_matrix_copy = copy_matrix(original_matrix)

    # First row substitution
    for row in original_matrix:
        min_value = get_row_min(row)
        subtract_row(original_matrix, row, min_value)
    print_matrix(original_matrix)
    
    # Column substitution
    for i in range(size):
        col_min_value = get_column_min(original_matrix, i)
        subtract_column(original_matrix, i, col_min_value)
    print_matrix(original_matrix)
    
    # Last iteration
    max_iterations = 1000
    counter = 0
    while True:
        zeros = []
        for i in range(size):
            for j in range(size):
                if original_matrix[i][j] == 0:
                    zeros.append((i, j))
        if len(zeros) == size * size:
            break
        else:
            rows = [zero[0] for zero in zeros]
            cols = [zero[1] for zero in zeros]
            min_value = min([original_matrix[row][col] for row in rows for col in cols])
            for zero in zeros:
                original_matrix[zero[0]][zero[1]] -= min_value
        counter += 1
        if counter > max_iterations:
            break
    print_matrix(original_matrix)

    result_matrix = subtract_smallest_top_right(original_matrix)
    print("Updated result matrix:")
    print_matrix(result_matrix)

    total_cost = sum_zero_cells(original_matrix_copy, result_matrix)
    total_cost2 = sum_zero_cells_Details(original_matrix_copy, result_matrix)
    print("Total cost: ", end="")
    
    print(" =", total_cost)

    # Display result in GUI
    output_text.insert(tk.END, "\nUpdated result matrix:\n")
    print_matrix(result_matrix)
    print_cost(total_cost2)
    output_text.insert(tk.END, "\nTotal cost: " + str(total_cost) + "\n")

def copy_matrix(source_matrix):
    size = len(source_matrix)
    Copy = [[0] * size for _ in range(size)]  # Create a matrix of zeros with the same size as the source matrix
    
    for i in range(size):
        for j in range(size):
            Copy[i][j] = source_matrix[i][j]  # Copy the value from the source matrix to the Copy matrix
            
    return Copy

def print_cost(cost):
    cost_str = ' '.join(map(str, cost[:-1])) + " = " + str(cost[-1])
    output_text.insert(tk.END, cost_str)

# Create GUI
window = tk.Tk()
window.title("Matrix Calculation GUI")
window.attributes("-fullscreen", True)

# Load and resize background image
bg_image = Image.open("wall3.png")
width, height = window.winfo_screenwidth(), window.winfo_screenheight()
bg_image = bg_image.resize((width, height), Image.Resampling.LANCZOS)

bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(window, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

top_space = tk.Label(window)
top_space.pack(pady=20)
# Matrix Size Input
size_label = tk.Label(window, text="Matrix Size:")
size_label.pack(pady=20)

size_entry = tk.Entry(window)
size_entry.pack()

# Matrix Input
matrix_entries = []
matrix_frame = tk.Frame(window)
matrix_frame.pack()

def exit_program():
    window.destroy()


def generate_matrix_inputs():
    size = int(size_entry.get())
    for i in range(size):
        row_entries = []
        for j in range(size):
            entry = tk.Entry(matrix_frame, width=5)
            entry.grid(row=i, column=j)
            row_entries.append(entry)
        matrix_entries.append(row_entries)

generate_button = tk.Button(window, text="Generate Matrix", command=generate_matrix_inputs)
generate_button.pack(pady=10)

# Calculate Button
calculate_button = tk.Button(window, text="Calculate", command=calculate_assignment)
calculate_button.pack(pady=10)

# Output Text Area
output_text = tk.Text(window, width=40, height=10)
output_text.pack(pady=10)

exit_button = tk.Button(window, text="Exit", command=exit_program)
exit_button.pack(pady=10)


window.mainloop()


import tkinter as tk
from tkinter import ttk

class LineChartApp(tk.Tk):
    def __init__(self):
        # Set initial dimensions for the canvas displaying the temperature chart
        super().__init__()
        self.canvas_temp_width = 600
        self.canvas_temp_height = 300

        # Set initial dimensions for the main canvas displaying the line chart
        self.canvas_width = 800
        self.canvas_height = 300

        # Initialize pointer for temperature indicator
        self.my_pointer = None

        # Set distances for x and y axis scaling
        self.x_dist = 20
        self.y_dist = 5

        # Define temperature ranges and normal range
        self.low_value = 18
        self.high_value = 27
        self.normal_range = [20, 25]

        # Set window title and geometry
        self.title("Line Chart App")
        self.geometry("800x600")

        # Create frame for input elements
        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(pady=10)

        # Create and place label and entry for new temperature values
        self.entry_label = ttk.Label(self.input_frame, text="Enter new value (°C):")
        self.entry_label.grid(row=0, column=0, padx=5)
        self.value_entry = ttk.Entry(self.input_frame)
        self.value_entry.grid(row=0, column=1, padx=5)

        # Create and place update button to add new values to the chart
        self.update_button = ttk.Button(
            self.input_frame, text="Update Chart", command=self.update_chart
        )
        self.update_button.grid(row=0, column=2, padx=5)

        # Create canvas for the line chart
        self.canvas = tk.Canvas(
            self, width=self.canvas_width, height=self.canvas_height, bg="white"
        )
        self.canvas.pack(pady=10)

        # Create frame for information labels
        self.info_frame = ttk.Frame(self)
        self.info_frame.pack(pady=10)

        # Create and place informational labels
        self.units_label = ttk.Label(self.info_frame, text="Units: °C")
        self.units_label.grid(row=0, column=0, padx=10)
        self.low_value_label = ttk.Label(
            self.info_frame, text=f"Low Value: {self.low_value}°C"
        )
        self.low_value_label.grid(row=0, column=1, padx=10)
        self.normal_range_label = ttk.Label(
            self.info_frame,
            text=f"Normal Range: {self.normal_range[0]}°C to {self.normal_range[1]}°C",
        )
        self.normal_range_label.grid(row=0, column=2, padx=10)
        self.high_value_label = ttk.Label(
            self.info_frame, text=f"High Value: {self.high_value}°C"
        )
        self.high_value_label.grid(row=0, column=3, padx=10)

        # Draw the initial chart layout and temperature indicator
        self.values = []
        self.draw_chart()
        self.draw_temperature()
        self.draw_temp_pointer(10)

    def draw_chart(self):
        # Draw the x and y axis with arrows
        self.canvas.delete("all")
        self.canvas.create_line(50, 280, 550, 280, arrow=tk.LAST)
        self.canvas.create_line(50, 280, 50, 10, arrow=tk.LAST)

        # Label the axes
        self.canvas.create_text(550, 290, text="Time (s)", anchor=tk.W)
        self.canvas.create_text(15, 50, text="Temperature (°C)", anchor=tk.E, angle=90)

        # Draw x-axis tick marks and labels
        for i in range(0, 26, 5):
            x = 50 + (i * self.x_dist)
            self.canvas.create_text(x, 288, text=f"{i}", anchor=tk.N)

        # Draw y-axis tick marks and labels
        for i in range(-10, 41, 10):
            y = 280 - (i + 10) * self.y_dist
            self.canvas.create_text(40, y, text=f"{i}", anchor=tk.E)

    def update_chart(self):
        try:
            # Get the new value from the entry and add it to the values list
            new_value = int(self.value_entry.get())
            self.values.append(new_value)

            # Calculate the position for the new data point on the canvas
            new_point = [
                50 + len(self.values) * self.x_dist,
                280 - (new_value + 10) * self.y_dist,
            ]

            # Draw a small oval to represent the new data point
            self.canvas.create_oval(
                new_point[0] - 3,
                new_point[1] - 3,
                new_point[0] + 3,
                new_point[1] + 3,
                fill="red",
            )
            # Label the new data point with its value
            self.canvas.create_text(
                new_point[0], new_point[1] - 10, text=str(new_value), fill="black"
            )

            # Draw a line connecting the new data point to the previous one, if any
            if len(self.values) > 1:
                pre_point = [
                    50 + (len(self.values) - 1) * self.x_dist,
                    280 - (self.values[-2] + 10) * self.y_dist,
                ]
                self.canvas.create_line(
                    new_point[0],
                    new_point[1],
                    pre_point[0],
                    pre_point[1],
                    fill="blue",
                    width=2,
                )

            # Update the temperature pointer with the new value
            self.draw_temp_pointer(new_value)

        except ValueError:
            # Handle invalid input (non-integer values)
            print("Please enter a valid integer")

    def draw_temperature(self):
        # Define dimensions and starting points for the thermometer-like display
        width = 30
        start_point = [700, 10]
        start_point2 = [start_point[0] + width, start_point[1]]

        # Calculate the positions for the oval representing the thermometer bulb
        cir_top_left = [start_point[0], self.canvas_height - start_point[1] - width]
        cir_bottom_right = [start_point2[0], self.canvas_height - start_point[1]]

        # Calculate the starting y-coordinate for the temperature indicator
        self.temp_start_y = cir_bottom_right[1] - (width / 2)

        # Draw the thermometer bulb (oval)
        self.canvas.create_oval(
            cir_top_left[0],
            cir_top_left[1],
            start_point2[0],
            cir_bottom_right[1],
            outline="#f11",
            fill="#1f1",
        )

        # Draw the vertical line (thermometer stem)
        self.canvas.create_line(
            cir_top_left[0] - 2, start_point[1], cir_top_left[0] - 2, self.temp_start_y
        )

        # Define the rectangle representing the filled part of the thermometer
        self.rect_top_left = [cir_top_left[0] + 5, start_point[1]]
        self.rect_bottom_right = [cir_bottom_right[0] - 5, cir_bottom_right[1] - 20]
        self.canvas.create_rectangle(
            self.rect_top_left[0],
            self.rect_top_left[1],
            self.rect_bottom_right[0],
            self.rect_bottom_right[1],
            outline="",
            fill="#1f1",
        )

        # Draw temperature scale labels
        for i in range(0, 100, 10):
            y = self.temp_start_y - (i * 3)
            self.canvas.create_text(start_point[0] - 5, y, text=f"{i}", anchor=tk.E)

    def draw_temp_pointer(self, i):
        # Remove the existing temperature pointer, if any
        if (self.my_pointer is None) is False:
            self.canvas.delete(self.my_pointer)

        # Calculate the new position for the temperature pointer
        new_point = self.temp_start_y - (i * 3)

        # Define the rectangle representing the temperature pointer
        new_rect_top_left = [self.rect_top_left[0], new_point]
        new_rect_bottom_right = [self.rect_bottom_right[0], new_point + (5 * 3)]

        # Draw the new temperature pointer
        self.my_pointer = self.canvas.create_rectangle(
            new_rect_top_left[0],
            new_rect_top_left[1],
            new_rect_bottom_right[0],
            new_rect_bottom_right[1],
            outline="",
            fill="#87cefa",
        )

if __name__ == "__main__":
    app = LineChartApp()
    app.mainloop()

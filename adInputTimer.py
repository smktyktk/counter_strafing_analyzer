import time
import keyboard
import mouse
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

# def detect_key_timing():
#     a_pressed_time = None
#     a_released_time = None
#     d_pressed_time = None
#     d_released_time = None

#     def on_a_event(event):
#         nonlocal a_pressed_time, a_released_time
#         if event.event_type == "down":
#             a_pressed_time = time.time()
#         elif event.event_type == "up":
#             a_released_time = time.time()

#     def on_d_event(event):
#         nonlocal d_pressed_time, d_released_time
#         if event.event_type == "down":
#             d_pressed_time = time.time()
#         elif event.event_type == "up":
#             d_released_time = time.time()

#     keyboard.hook_key('a', on_a_event)
#     keyboard.hook_key('d', on_d_event)

#     print("Press and release 'a' and 'd' as described. Press 'esc' to exit.")
#     while True:
#         if keyboard.is_pressed('esc'):
#             break
#         if a_pressed_time and a_released_time and d_pressed_time and d_released_time:
#             a_hold_time = a_released_time - a_pressed_time
#             d_hold_time = d_released_time - d_pressed_time
#             if a_pressed_time < d_pressed_time:
#                 time_between = d_pressed_time - a_released_time
#                 print(f"'d' hold time: {d_hold_time:.3f} seconds")
#             else:
#                 time_between = a_pressed_time - d_released_time
#                 print(f"'a' hold time: {a_hold_time:.3f} seconds")
            
#             if time_between > 0:
#                 print(f"Time between 'a' and 'd': {time_between:.3f} seconds")
#             else:
#                 print(f"Time overlapsed: {time_between:.3f} seconds")

#             a_pressed_time = None
#             a_released_time = None
#             d_pressed_time = None
#             d_released_time = None
#         time.sleep(0.1)

def create_output_window():
    window = tk.Tk()
    window.title("Key Timing Output")
    window.geometry("500x400")

    text_area = ScrolledText(window, wrap=tk.WORD, font=("Arial", 12))
    text_area.pack(expand=True, fill=tk.BOTH)

    return window, text_area

def detect_key_timing_with_window():
    window, text_area = create_output_window()

    a_pressed_time = None
    a_released_time = None
    d_pressed_time = None
    d_released_time = None
    a_hold_time = None
    d_hold_time = None
    time_between = None
    left_click_pressed_time = None
    mouse_timing = None

    def on_a_event(event):
        nonlocal a_pressed_time, a_released_time, a_hold_time, time_between
        if event.event_type == "down":
            a_pressed_time = time.time()
            print("a prs ", a_pressed_time)
        elif event.event_type == "up":
            a_released_time = time.time()
            print("a rel ", a_released_time)
            a_hold_time = a_released_time - a_pressed_time
            if a_pressed_time and d_pressed_time:
                if a_pressed_time < d_pressed_time:
                    time_between = d_pressed_time - a_released_time
                else:
                    time_between = a_pressed_time - d_released_time

    def on_d_event(event):
        nonlocal d_pressed_time, d_released_time, d_hold_time, time_between
        if event.event_type == "down":
            d_pressed_time = time.time()
            print("d prs ", d_pressed_time)
        elif event.event_type == "up":
            d_released_time = time.time()
            print("d rel ", d_released_time)
            d_hold_time = d_released_time - d_pressed_time
            if a_pressed_time and d_pressed_time:
                if a_pressed_time < d_pressed_time:
                    time_between = d_pressed_time - a_released_time
                else:
                    time_between = a_pressed_time - d_released_time

    def on_mouse_left_click(event):
        nonlocal left_click_pressed_time
        if type(event) == mouse.ButtonEvent and event.event_type != 'up':
            left_click_pressed_time = time.time()
            print("mouse prs ", left_click_pressed_time)

    mouse.hook(on_mouse_left_click)
    keyboard.hook_key('a', on_a_event)
    keyboard.hook_key('d', on_d_event)

    def update_output():
        nonlocal a_pressed_time, a_released_time, d_pressed_time, d_released_time, time_between, left_click_pressed_time, mouse_timing, a_hold_time, d_hold_time

        if left_click_pressed_time:
            if a_hold_time and d_hold_time:

                if a_pressed_time < d_pressed_time:
                    text_area.insert(tk.END, f"Result: 'd' hold time: {d_hold_time:.3f} seconds\n")
                    mouse_timing = left_click_pressed_time - d_pressed_time
                else:
                    text_area.insert(tk.END, f"Result: 'a' hold time: {a_hold_time:.3f} seconds\n")
                    mouse_timing = left_click_pressed_time - a_pressed_time
                print(mouse_timing)
                if time_between > 0:
                    text_area.insert(tk.END, f"Time between: {time_between:.3f} seconds\n")
                else:
                    text_area.insert(tk.END, f"Time overlapped: {time_between:.3f} seconds\n")
                
                text_area.insert(tk.END, f"Mouse click timing: {mouse_timing:.3f} seconds after the first key release\n")
                text_area.see(tk.END)

            mouse_timing = None
            left_click_pressed_time = None

        window.after(1, update_output)
    keyboard.add_hotkey('enter', lambda: analyze_statistics(text_area))
    keyboard.add_hotkey('p', lambda: clear_statistics(text_area))
    window.after(1, update_output)
    window.mainloop()

def analyze_statistics(text_area):
    content = text_area.get("1.0", tk.END).strip().split("\n")
    if len(content) < 60:
        text_area.insert(tk.END, "Not enough data to analyze. Need more entries.\n")
        text_area.see(tk.END)
        return

    latest_entries = content[-60:]
    hold_times = []
    time_betweens = []
    mouse_timings = []

    for line in latest_entries:
        if "Result:" in line:
            hold_time = float(line.split(":")[2].strip().split(" ")[0])
            if hold_time <=  0.150:
                hold_times.append(hold_time)
        elif "Time" in line:
            time_between = float(line.split(":")[1].strip().split(" ")[0])
            if time_between < 0.50:
                time_betweens.append(time_between)
        elif "first key release" in line:
            mouse_timing = float(line.split(":")[1].strip().split(" ")[0])
            if mouse_timing < 0.200:
                mouse_timings.append(mouse_timing)

    avg_hold_time = sum(hold_times) / len(hold_times)
    avg_time_between = sum(time_betweens) / len(time_betweens)
    avg_mouse_timing = sum(mouse_timings) / len(mouse_timings)
    diff_with_80ms_key = avg_hold_time - 0.08
    diff_with_80ms_mouse = avg_mouse_timing - 0.08 if mouse_timings else None

    text_area.insert(tk.END, f"\nAnalysis of latest statistics:\n")
    text_area.insert(tk.END, f"Average hold time of second pressed key: {avg_hold_time:.3f} seconds\n")
    text_area.insert(tk.END, f"Difference with 80ms: {diff_with_80ms_key:.3f} seconds\n")
    text_area.insert(tk.END, f"Average time between keys: {avg_time_between:.3f} seconds\n\n")
    text_area.insert(tk.END, f"Average mouse click timing: {avg_mouse_timing:.3f} seconds\n")
    text_area.insert(tk.END, f"Difference with 80ms (mouse click): {diff_with_80ms_mouse:.3f} seconds\n")

    text_area.see(tk.END)

def clear_statistics(text_area):
    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, "Statistics cleared.\n")
    text_area.see(tk.END)

if __name__ == "__main__":
    detect_key_timing_with_window()



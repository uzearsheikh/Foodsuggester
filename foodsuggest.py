import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import random, datetime, json, os

HISTORY_FILE = "food_history.json"
NO_REPEAT_DAYS = 3

family_foods = {}
food_history = []

# Load food history
def load_history():
    global food_history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            food_history = json.load(f)
    else:
        food_history = []

# Save food history
def save_history():
    with open(HISTORY_FILE, "w") as f:
        json.dump(food_history, f)

# Add food to family member
def add_food():
    member = member_entry.get().strip()
    food = food_entry.get().strip()
    if member and food:
        family_foods.setdefault(member, []).append(food)
        update_status(f"✅ Added '{food}' for {member} 🍴")
        member_entry.delete(0, tk.END)
        food_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter both name and food.")

# Pick food suggestion
def pick_food():
    all_foods = set()
    for foods in family_foods.values():
        all_foods.update(foods)

    today = str(datetime.date.today())
    recent_foods = {entry["food"] for entry in food_history[-NO_REPEAT_DAYS:]}
    available_foods = list(all_foods - recent_foods)

    if not available_foods:
        update_status("⚠️ No new foods available. Add more!")
        return

    chosen = random.choice(available_foods)
    food_history.append({"date": today, "food": chosen})
    if len(food_history) > 10:
        food_history.pop(0)

    save_history()
    update_status(f"🍽️ Today's food: {chosen} 😋")

# Status update label
def update_status(message):
    status_label.config(text=message)

# Load background image
def load_background_image():
    try:
        bg = Image.open(r"C:\Users\HP\Downloads\uzear.py\background.png")
        bg = bg.resize((600, 520), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(bg)
    except Exception as e:
        print("Failed to load background image:", e)
        return None

# ✅ Rounded rectangle function for canvas
def _create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)

tk.Canvas.create_rounded_rect = _create_rounded_rect

# ==== UI Setup ====
root = tk.Tk()
root.title("🍛 Family Food Suggestion App")
root.geometry("600x520")
root.configure(bg="#f7f1e3")

# Background image
bg_img = load_background_image()
if bg_img:
    bg_label = tk.Label(root, image=bg_img)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_img

# Overlay frame
overlay = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
overlay.place(x=30, y=30, width=540, height=460)

# Style
style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background="#ffffff", font=("Segoe UI", 11))
style.configure("TEntry", font=("Segoe UI", 11))
style.configure("TButton", font=("Segoe UI", 11), padding=6)

# Heading
ttk.Label(overlay, text="👨‍👩‍👧‍👦 Family Favorites", font=("Segoe UI", 14, "bold")).pack(anchor="center", pady=(15, 10))

# Input fields
ttk.Label(overlay, text="Family Member's Name").pack(anchor="w", padx=20)
member_entry = ttk.Entry(overlay, width=40)
member_entry.pack(padx=20, pady=5)

ttk.Label(overlay, text="Favorite Food").pack(anchor="w", padx=20)
food_entry = ttk.Entry(overlay, width=40)
food_entry.pack(padx=20, pady=5)

# Custom Button on Canvas
def draw_button(canvas, text):
    canvas.delete("all")
    canvas.create_rounded_rect(0, 0, 150, 45, 20, fill="#ff6b81", outline="#c0392b", width=2, tags="button")
    canvas.create_text(75, 23, text=text, fill="white", font=("Segoe UI", 10, "bold"), tags="button")

def on_add_click(event):
    add_food()
    draw_button(add_canvas, "➕ Add Food")

# Add canvas button
add_canvas = tk.Canvas(overlay, width=150, height=45, bg="#ffffff", highlightthickness=0)
draw_button(add_canvas, "➕ Add Food")
add_canvas.pack(pady=10)
add_canvas.tag_bind("button", "<Button-1>", on_add_click)
add_canvas.tag_bind("button", "<Enter>", lambda e: draw_button(add_canvas, "➕ Add Food"))
add_canvas.tag_bind("button", "<Leave>", lambda e: draw_button(add_canvas, "➕ Add Food"))

# Suggestion Button
ttk.Label(overlay, text="🍽️ Today's Pick", font=("Segoe UI", 13, "bold")).pack(anchor="center", pady=(10, 5))
suggest_button = ttk.Button(overlay, text="🎲 Get Suggestion", command=pick_food)
suggest_button.pack(padx=20, pady=5, fill="x")

# Status Label
status_label = ttk.Label(overlay, text="", foreground="#2d3436", font=("Segoe UI", 11, "italic"))
status_label.pack(padx=20, pady=10, anchor="w")

# Load history and run app
load_history()
root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import requests
import os

class ImageColorizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lineage AI Image Colorizer")
        self.root.geometry("900x600")
        self.root.configure(bg="#9BC03C")

        # Initialize variables
        self.original_image = None
        self.colorized_image = None
        self.image_path = None

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Header Label
        header_label = tk.Label(self.root, text="Lineage AI Image Colorizer",
                                font=("Helvetica", 20, "bold"),
                                bg="#9BC03C", fg="#ffffff")
        header_label.pack(pady=20)

        # Open Image Button
        self.open_button = tk.Button(self.root, text="Open Grayscale Image",
                                     command=self.open_image,
                                     font=("Helvetica", 14),
                                     bg="#4a7c59", fg="white",
                                     activebackground="#6a9e75", activeforeground="white",
                                     bd=0, relief="flat", padx=20, pady=10)
        self.open_button.pack(pady=10)

        # Colorize Image Button
        self.colorize_button = tk.Button(self.root, text="Colorize Image",
                                         command=self.colorize_image,
                                         font=("Helvetica", 14),
                                         bg="#4a7c59", fg="white",
                                         activebackground="#6a9e75", activeforeground="white",
                                         bd=0, relief="flat", padx=20, pady=10)
        self.colorize_button.pack(pady=10)
        self.colorize_button.config(state=tk.DISABLED)

        # Save Image Button
        self.save_button = tk.Button(self.root, text="Save Colorized Image",
                                     command=self.save_image,
                                     font=("Helvetica", 14),
                                     bg="#4a7c59", fg="white",
                                     activebackground="#6a9e75", activeforeground="white",
                                     bd=0, relief="flat", padx=20, pady=10)
        self.save_button.pack(pady=10)
        self.save_button.config(state=tk.DISABLED)

        # Canvas to display images
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="#e0f0d9", bd=0, highlightthickness=0)
        self.canvas.pack(pady=20)

    def open_image(self):
        filetypes = [("Image Files", "*.jpg *.jpeg *.png *.bmp")]
        self.image_path = filedialog.askopenfilename(title="Open Grayscale Image", filetypes=filetypes)

        if self.image_path:
            try:
                # Debug print to check the selected path
                print(f"Selected Image Path: {self.image_path}")
                # Open the image
                self.original_image = Image.open(self.image_path)
                self.display_image(self.original_image, position='left')
                # Enable the colorize button and disable save button until colorization
                self.colorized_image = None
                self.colorize_button.config(state=tk.NORMAL)
                self.save_button.config(state=tk.DISABLED)
            except FileNotFoundError:
                # If file not found, show an error message
                messagebox.showerror("File Not Found", f"The file at {self.image_path} was not found.")
            except Exception as e:
                # Handle any other exceptions that may occur
                messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def display_image(self, image, position='left'):
        # Resize image to fit the canvas
        img_width, img_height = image.size
        max_width = 400
        scale = max_width / img_width
        new_size = (int(img_width * scale), int(img_height * scale))
        image_resized = image.resize(new_size, Image.LANCZOS)
        image_tk = ImageTk.PhotoImage(image_resized)

        if position == 'left':
            self.canvas.create_image(200, 200, image=image_tk)
            self.left_image = image_tk  # Keep a reference
        else:
            self.canvas.create_image(600, 200, image=image_tk)
            self.right_image = image_tk  # Keep a reference

    def colorize_image(self):
        if self.image_path:
            try:
                # Your DeepAI API key
                api_key = 'ed8c68f8-855d-4dbd-ba59-be5206bc9ef7'

                # Call the DeepAI Image Colorization API
                url = 'https://api.deepai.org/api/colorizer'
                with open(self.image_path, 'rb') as file:
                    response = requests.post(
                        url,
                        files={'image': file},
                        headers={'api-key': api_key}
                    )

                # Parse the API response
                result = response.json()
                print("API Response:", result)  # Print the API response for debugging

                # Check if the output_url key exists in the response
                if 'output_url' in result:
                    colorized_image_url = result['output_url']

                    # Download the colorized image
                    colorized_image_response = requests.get(colorized_image_url)
                    colorized_image_path = os.path.join(os.getcwd(), "colorized_image.jpg")
                    with open(colorized_image_path, 'wb') as f:
                        f.write(colorized_image_response.content)

                    # Load and display the colorized image
                    self.colorized_image = Image.open(colorized_image_path)
                    self.display_image(self.colorized_image, position='right')
                    self.save_button.config(state=tk.NORMAL)
                else:
                    # Handle API errors if output_url is missing
                    error_message = result.get('err') or 'Unknown error occurred.'
                    raise Exception(f"API Error: {error_message}")

            except Exception as e:
                # Display an error message box if any exceptions occur
                messagebox.showerror("Error", f"Failed to colorize the image: {str(e)}")

    def save_image(self):
        if self.colorized_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                     filetypes=[("JPEG Image", "*.jpg"),
                                                                ("PNG Image", "*.png"),
                                                                ("All Files", "*.*")])
            if save_path:
                self.colorized_image.save(save_path)
                messagebox.showinfo("Image Saved", f"Colorized image saved to:\n{save_path}")
        else:
            messagebox.showwarning("No Colorized Image", "There is no colorized image to save.")

def main():
    root = tk.Tk()
    app = ImageColorizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

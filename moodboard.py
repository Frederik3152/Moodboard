import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

class MoodboardApp:
    from resize_utils import resize_image, draw_resize_rectangle, update_resize_rectangle, remove_resize_rectangle

    def __init__(self, root):
        self.root = root
        self.root.title("Moodboard")
        self.root.geometry("1200x1000")
        
        # Create canvas
        self.canvas = Canvas(root, bg='beige')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Store current dragging state
        self.dragging = None
        self.drag_start_x = 0
        self.drag_start_y = 0

        # Store current resizing state
        self.resizing = None 
        self.resize_corner = None
        self.original_bbox = None
        self.selected_item = None
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
        # Add a sample image
        self.add_image("sample_image.jpg", 400, 100)
        self.add_image("sample_image.jpg", 700, 300)
    
    def add_image(self, image_path, x, y):
        """
        Add an image to the canvas

        Parameters:
        ------------
        image_path : str
            Path to the image file
        x : int
            X coordinate on the canvas
        y : int
            Y coordinate on the canvas
        """
        try:
            # Load and resize image
            img = Image.open(image_path)
            img.thumbnail((500, 500))
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            # Add to canvas
            image_id = self.canvas.create_image(x, y, image=photo, anchor=tk.NW)
            
            # Store image reference
            if not hasattr(self.canvas, 'images'):
                self.canvas.images = {}
            self.canvas.images[image_id] = {
                'photo': photo,
                'pil_image': img.copy(),
                'path': image_path
            }
            
        except Exception as e:
            print(f"Error loading image: {e}")
    
    def on_click(self, event):
        """
        Handle mouse click

        Parameters:
        ------------
        event : tk.Event
            The mouse event of clicking
        """
        # Find items at click position 
        items = self.canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
    
        # Check if clicked a resize point
        for item in items:
            tags = self.canvas.gettags(item)
            if "resize_point" in tags:
                # Determine which corner based on item ID
                if hasattr(self, '_resizepoint1') and item == self._resizepoint1:
                    self.resize_corner = 'top-left'
                elif hasattr(self, '_resizepoint2') and item == self._resizepoint2:
                    self.resize_corner = 'top-right'
                elif hasattr(self, '_resizepoint3') and item == self._resizepoint3:
                    self.resize_corner = 'bottom-right'
                elif hasattr(self, '_resizepoint4') and item == self._resizepoint4:
                    self.resize_corner = 'bottom-left'
                
                self.resizing = self.selected_item
                self.drag_start_x = event.x
                self.drag_start_y = event.y
                self.original_bbox = self.canvas.bbox(self.selected_item)
                return
        
        # Find items at click position
        image_items = [item for item in items if "resize_point" not in self.canvas.gettags(item)]
        
        if image_items:
            # Draw a rectangle in each corner of the selected item
            self.selected_item = image_items[-1]
            self.draw_resize_rectangle(self.selected_item)
            
            # Start dragging
            self.dragging = image_items[-1]
            self.drag_start_x = event.x
            self.drag_start_y = event.y
        else:
            self.remove_resize_rectangle()
            self.dragging = None
            self.selected_item = None
    
    def on_drag(self, event):
        """
        Handle dragging by calculating movement on canvas based on starting position

        Parameters:
        ------------
        event : tk.Event
            The mouse event of dragging
        """
        if self.resizing:
            # Handle resizing
            self.resize_image(event)
        elif self.dragging:
            # Calculate movement
            dx = event.x - self.drag_start_x
            dy = event.y - self.drag_start_y
            
            # Move the item
            self.canvas.move(self.dragging, dx, dy)
            self.update_resize_rectangle(self.dragging)
            
            # Update drag start position
            self.drag_start_x = event.x
            self.drag_start_y = event.y
    
    def on_release(self, event):
        """
        Handle mouse release which ends dragging

        Parameters:
        ------------
        event : tk.Event
            The mouse event of releasing the button
        """
        self.dragging = None
        self.resizing = None
        self.resize_corner = None
        self.original_bbox = None


# Run the app
root = tk.Tk()
app = MoodboardApp(root)
root.mainloop()

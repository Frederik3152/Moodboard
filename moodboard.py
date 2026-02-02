import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk


class MoodboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Moodboard")
        self.root.geometry("1200x800")
        
        # Create canvas
        self.canvas = Canvas(root, bg='beige')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Store current dragging state
        self.dragging = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        
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
            
            # Store reference to prevent garbage collection
            if not hasattr(self.canvas, 'images'):
                self.canvas.images = []
            self.canvas.images.append(photo)
            
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

        if items:
            # Draw a rectangle in each corner of the selected item
            self.draw_resize_rectangle(items[-1])
        else:
            self.remove_resize_rectangle()
            
        # Only drag if we actually clicked on an item
        if items:
            self.dragging = items[-1]  # Get topmost item
            self.drag_start_x = event.x
            self.drag_start_y = event.y
        else:
            self.dragging = None
    
    def on_drag(self, event):
        """
        Handle dragging by calculating movement on canvas based on starting position

        Parameters:
        ------------
        event : tk.Event
            The mouse event of dragging
        """
        if self.dragging:
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

    def draw_resize_rectangle(self, item_id):
        """
        Draw a rectangle around the given item to indicate it can be resized
        
        Parameters:
        ------------
        item_id : int
            The canvas item ID to draw the rectangle around
        """
        bbox = self.canvas.bbox(item_id)
        self._current_resize_rect = self.canvas.create_rectangle(bbox, tags="resize_point")
        self._resizepoint1 = self.canvas.create_rectangle(bbox[0]-3, bbox[1]-3, bbox[0]+3, bbox[1]+3, tags="resize_point", fill='#000000')
        self._resizepoint2 = self.canvas.create_rectangle(bbox[2]-3, bbox[1]-3, bbox[2]+3, bbox[1]+3, tags="resize_point", fill='#000000')
        self._resizepoint3 = self.canvas.create_rectangle(bbox[2]-3, bbox[3]-3, bbox[2]+3, bbox[3]+3, tags="resize_point", fill='#000000')
        self._resizepoint4 = self.canvas.create_rectangle(bbox[0]-3, bbox[3]-3, bbox[0]+3, bbox[3]+3, tags="resize_point", fill='#000000')

    def update_resize_rectangle(self, item_id):
        """
        Update the resize rectangle position

        Parameters:
        ------------
        item_id : int
            The canvas item ID to update the rectangle for
        """
        self.remove_resize_rectangle()
        bbox = self.canvas.bbox(item_id)
        self.canvas.coords(self._current_resize_rect, bbox)
        self.canvas.coords(self._resizepoint1, bbox[0]-3, bbox[1]-3, bbox[0]+3, bbox[1]+3)
        self.canvas.coords(self._resizepoint2, bbox[2]-3, bbox[1]-3, bbox[2]+3, bbox[1]+3)
        self.canvas.coords(self._resizepoint3, bbox[2]-3, bbox[3]-3, bbox[2]+3, bbox[3]+3)
        self.canvas.coords(self._resizepoint4, bbox[0]-3, bbox[3]-3, bbox[0]+3, bbox[3]+3)
        self.draw_resize_rectangle(item_id)

    def remove_resize_rectangle(self):
        """
        Remove the resize rectangle and points from the canvas
        """
        # self.canvas.delete(self._current_resize_rect if hasattr(self, '_current_resize_rect') else None)
        for x in self.canvas.find_withtag("resize_point"):
            self.canvas.delete(x)


# Run the app
root = tk.Tk()
app = MoodboardApp(root)
root.mainloop()

import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

class MoodboardApp:
    from resize_utils import resize_image, draw_resize_rectangle, update_resize_rectangle, remove_resize_rectangle

    def __init__(self, root):
        self.root = root
        self.root.title("Moodboard")
        self.root.geometry("1500x1200")
        
        # Layout: main canvas + staging
        self.container = tk.Frame(root)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.canvas = Canvas(self.container, bg="beige")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.staging_frame = tk.Frame(self.container, width=250)
        self.staging_frame.pack(side=tk.RIGHT, fill=tk.Y)

        tk.Label(self.staging_frame, text="Loaded Images").pack(fill=tk.X)

        self.staging_canvas = Canvas(self.staging_frame, bg="#f3f3f3", width=250, highlightthickness=0)
        self.staging_canvas.pack(fill=tk.BOTH, expand=True)

        # Store staging references
        self.staging_images = {}
        self._staging_next_y = 10
        self._staging_pad = 10

        # Drag-and-drop state for staging area
        self._staging_drag_item = None
        self._ghost_id = None
        self._ghost_photo = None
        self._ghost_path = None

        # Bind staging canvas events for drag-and-drop
        self.staging_canvas.bind("<Button-1>", self.on_staging_press)
        self.staging_canvas.bind("<B1-Motion>", self.on_staging_drag)
        self.staging_canvas.bind("<ButtonRelease-1>", self.on_staging_release)
        
        # Store current dragging state
        self.dragging = None
        self.drag_start_x = 0
        self.drag_start_y = 0

        # Store current resizing state
        self.resizing = None 
        self.resize_corner = None
        self.original_bbox = None
        self.selected_item = None
        
        # Bind mouse and key events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Delete>", self.on_delete)
        self.root.bind("<BackSpace>", self.on_delete)
        
        # Add a sample image
        self.add_to_staging("sample_image.jpg")
        self.add_to_staging("sample_image1.JPG")

    def add_to_staging(self, image_path):
        """
        Add an image to the staging area as a thumbnail and save reference for dragging

        Parameters:
        ------------
        image_path : str
            Path to the image file to add to the staging area
        """
        # Load and create thumbnail
        img = Image.open(image_path)
        img.thumbnail((220, 220))

        # Add to staging canvas
        photo = ImageTk.PhotoImage(img)
        x, y = 10, self._staging_next_y
        item_id = self.staging_canvas.create_image(x, y, image=photo, anchor=tk.NW)

        # Store reference for dragging
        self.staging_images[item_id] = {
            "photo": photo,
            "path": image_path,
        }

        # Update next Y position for staging to avoid overlap
        self._staging_next_y += img.size[1] + self._staging_pad

    
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

    def on_delete(self, event):
        """
        Handle delete key press to remove selected item

        Parameters:
        ------------
        event : tk.Event
            The keyboard event of pressing delete
        """
        if self.selected_item:
            self.canvas.delete(self.selected_item)
            self.remove_resize_rectangle()
            self.selected_item = None

    def _pointer_to_main_canvas_xy(self):
        """
        Convert current pointer position to main canvas coordinates
        """
        # Get pointer position in absolute screen coordinates
        px, py = self.root.winfo_pointerx(), self.root.winfo_pointery()

        # Get main canvas position in absolute screen coordinates
        cx, cy = self.canvas.winfo_rootx(), self.canvas.winfo_rooty()
        return px - cx, py - cy

    def on_staging_press(self, event):
        """
        Get the image under the mouse in the staging area and create a ghost image on the main canvas for dragging

        Parameters:
        ------------
        event : tk.Event
            The mouse event of pressing the button in staging area
        """
        # Remove any existing resize rectangles when starting a new drag from staging
        self.remove_resize_rectangle()
        self.dragging = None
        self.selected_item = None

        # Find items at click position in staging canvas
        items = self.staging_canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
        if not items:
            return

        item = items[-1]
        if item not in self.staging_images:
            return

        self._staging_drag_item = item
        self._ghost_photo = self.staging_images[item]["photo"]   # reuse thumbnail image
        self._ghost_path = self.staging_images[item]["path"]

        # Create ghost image on main canvas at pointer position
        x, y = self._pointer_to_main_canvas_xy()
        self._ghost_id = self.canvas.create_image(x, y, image=self._ghost_photo, anchor=tk.NW)

    def on_staging_drag(self, event):
        """
        Update ghost image position while dragging

        Parameters:
        ------------
        event : tk.Event
            The mouse event of dragging in staging area
        """
        # Update ghost image position to follow pointer
        if not self._ghost_id:
            return
        x, y = self._pointer_to_main_canvas_xy()
        self.canvas.coords(self._ghost_id, x, y)

    def on_staging_release(self, event):
        """
        On release, if there is a ghost image, add the real image to the canvas at the ghost position and remove the ghost

        Parameters:
        ------------
        event : tk.Event
            The mouse event of releasing the button in staging area
        """
        if not self._ghost_id:
            return

        x, y = self._pointer_to_main_canvas_xy()

        # Drop only if inside the visible main canvas
        if 0 <= x <= self.canvas.winfo_width() and 0 <= y <= self.canvas.winfo_height():
            self.add_image(self._ghost_path, int(x), int(y))  # creates a real canvas image

        self.canvas.delete(self._ghost_id)
        self._staging_drag_item = None
        self._ghost_id = None
        self._ghost_photo = None
        self._ghost_path = None



# Run the app
# root = tk.Tk()
# app = MoodboardApp(root)
# root.mainloop()

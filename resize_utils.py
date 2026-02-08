from PIL import Image, ImageTk

def draw_resize_rectangle(self, item_id):
    """
    Draw a rectangle around the given item to indicate it can be resized
    
    Parameters:
    ------------
    item_id : int
        The canvas item ID to draw the rectangle around
    """
    self.remove_resize_rectangle()
    bbox = self.canvas.bbox(item_id)
    self._current_resize_rect = self.canvas.create_rectangle(bbox, tags="resize_border")
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
    for x in self.canvas.find_withtag("resize_point"):
        self.canvas.delete(x)
    for x in self.canvas.find_withtag("resize_border"):
        self.canvas.delete(x)

def resize_image(self, event):
    """
    Resize the image based on which corner is being dragged
    
    Parameters:
    ------------
    event : tk.Event
        The mouse event during resize dragging
    """
    # Get current bounding box
    current_bbox = self.canvas.bbox(self.resizing)
    x1, y1, x2, y2 = current_bbox
    
    # Get current mouse position
    x, y = event.x, event.y
    
    # Calculate new dimensions based on which corner is being dragged
    if self.resize_corner == 'bottom-right':
        new_width = x - x1
        new_height = y - y1
        new_x, new_y = x1, y1
    elif self.resize_corner == 'bottom-left':
        new_width = x2 - x
        new_height = y - y1
        new_x, new_y = x, y1
    elif self.resize_corner == 'top-right':
        new_width = x - x1
        new_height = y2 - y
        new_x, new_y = x1, y
    elif self.resize_corner == 'top-left': 
        new_width = x2 - x
        new_height = y2 - y
        new_x, new_y = x, y
    else:
        return
    
    # Prevent negative or too small dimensions
    if new_width < 20 or new_height < 20:
        return
    
    # Get the original PIL image
    original_pil = self.canvas.images[self.resizing]['pil_image']
    
    # Resize the PIL image
    resized_pil = original_pil.resize((int(new_width), int(new_height)), Image.Resampling.LANCZOS)
    
    # Convert to PhotoImage
    new_photo = ImageTk.PhotoImage(resized_pil)
    
    # Update the canvas image
    self.canvas.itemconfig(self.resizing, image=new_photo)
    self.canvas.coords(self.resizing, new_x, new_y)
    
    # Update stored reference
    self.canvas.images[self.resizing]['photo'] = new_photo
    
    # Update resize rectangles
    self.update_resize_rectangle(self.resizing)

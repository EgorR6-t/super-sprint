import g2d
import math
from actor import Actor, Arena
from math import dist
from g2d import Point 

# Save the filename to a variable so g2d can use it later
BACKGROUND_IMAGE = "images/super-sprint_use.png"

def actor_center(a: Actor) -> Point:
    # Tuple concatenation: (x, y) + (w, h) = (x, y, w, h)
    x, y, w, h = a.pos() + a.size()
    return (x + w / 2, y + h / 2)

class CurvedWall(Actor):
    def __init__(self, pos, size, center, radius):
        self._pos = pos
        self._size = size
        self._center = center
        self._radius = radius
    
    def move(self, arena):
        pass
    
    def pos(self):
        return self._pos
    
    def size(self):
        return self._size
    
    def sprite(self):
        return None
    
    def center(self):
        return self._center
    
    def radius(self):
        return self._radius

class ExternalWall(CurvedWall):  # attract cars towards center
    def confirm_collision(self, other: Actor) -> bool:
        return dist(self.center(), actor_center(other)) > self.radius()

class InternalWall(CurvedWall):  # repel cars from center
    def confirm_collision(self, other: Actor) -> bool:
        return dist(self.center(), actor_center(other)) < self.radius()

class Car(Actor):  # Placeholder
    def move(self, arena):
        for other in arena.collisions():
            if isinstance(other, ExternalWall) and other.confirm_collision(self):
                # Handle crashing into the outside wall
                pass

def load_walls(filename) -> list[str]:
    walls = []
    with open(filename) as file:
        for line in file:
            walls.append(line.strip())
    return walls

def is_wall(x, y, walls) -> bool:
    return walls[y][x] == "#"


# --- HOW TO DRAW THE IMAGE IN G2D ---
def main():
    arena = Arena((800, 600))  # Adjust to your exact image dimensions
    # arena.add(Car(...))
    
    def tick():
        g2d.clear_canvas()
        
        # 1. Draw your custom local background image first
        g2d.draw_image(BACKGROUND_IMAGE, (0, 0))
        
        # 2. Update and draw everything else
        arena.move_all()
        for a in arena.actors():
            if a.sprite() is not None:
                g2d.draw_image(a.sprite(), a.pos())
                
    g2d.init_canvas((800, 600))
    g2d.main_loop(tick)

if __name__ == "__main__":
    main()
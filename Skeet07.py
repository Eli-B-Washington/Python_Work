"""
File: skeet.py
Original Author: Br. Burton
Designed to be completed by others
This program implements an awesome version of skeet.
"""
import arcade
import math
import random

# These are Global constants to use throughout the game
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600

RIFLE_WIDTH = 20
RIFLE_HEIGHT = 100
RIFLE_COLOR = arcade.color.DARK_RED

BULLET_RADIUS = 3
BULLET_COLOR = arcade.color.BLACK_OLIVE
BULLET_SPEED = 10

TARGET_RADIUS = 20
TARGET_COLOR = arcade.color.CARROT_ORANGE
TARGET_SAFE_COLOR = arcade.color.AIR_FORCE_BLUE
TARGET_SAFE_RADIUS = 15


class Point:
    """initiates point location at a random start."""
    
    def __init__(self):
        self.x = random.uniform(20.00, 30.00)
        self.y = random.uniform(250.00, 500.00)
        
class Velocity:
    """Initiates velocity"""
    def __init__(self):
        
        self.dx = random.uniform(1.00, 5.00)
        self.dy = random.uniform(-2.00, 5.00) 

class Flying:
    """Base class for flying objects"""
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.radius = TARGET_RADIUS
    
  
    def advance(self):
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
    
        
    def is_off_screen(self, screen_width, screen_height):
        if (self.center.x > screen_width or self.center.y > screen_height):
            self.alive = False
        else:
            self.alive = True

class Bullet(Flying):
    """Class for bullets that will be fired from the rifle"""
    def __init__(self):
        super().__init__()
        self.center.x = random.uniform(0.00, 0.00)
        self.center.y = random.uniform(0.00, 0.00)
        self.radius = BULLET_RADIUS

    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, BULLET_RADIUS, BULLET_COLOR)
    
    
    def fire(self, angle):
        self.velocity.dx = math.cos(math.radians(angle)) * BULLET_SPEED
        self.velocity.dy = math.sin(math.radians(angle)) * BULLET_SPEED

class Target(Flying):
    """Base class for general target that inherits the flying class"""
    def __init__(self):
        super().__init__()
        self.score = 0
    
    def draw(self):
        arcade.draw_circle_filled(self.center.x, self.center.y, TARGET_RADIUS, TARGET_COLOR)
    
    def hit(self):
        self.alive = False
        return self.score + 1
        

class Strong_Target(Target):
    """This target inherits from the target class.  This target will be slower and take 3 hits to eliminate."""
    def __init__(self):
        super().__init__()
        self.lives = 3
        self.dx = random.uniform(1.00, 3.00)
        self.dy = random.uniform(-2.00, 3.00)
        
    def draw(self):
        arcade.draw_circle_outline(self.center.x, self.center.y, TARGET_RADIUS, TARGET_COLOR)
        text_x = self.center.x - (self.radius / 2)
        text_y = self.center.y - (self.radius / 2)
        arcade.draw_text(repr(self.lives), text_x, text_y, TARGET_COLOR, font_size=20)
    
    def hit(self):
        self.lives -= 1
        if self.lives == 0:
            self.alive = False
            return self.score + 5
        else:
            return self.score + 1
        
       
       
class Safe_Target(Target):
    """This target inherits from the target class.  This target should not be hit or will incur a 10 point penalty"""
    def __init__(self):
        super().__init__()
    
    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, TARGET_SAFE_RADIUS*2 , TARGET_SAFE_RADIUS*2 , TARGET_SAFE_COLOR)
    
    def hit(self):
        self.alive = False
        return self.score - 10
    

class Super_Strong(Target):
    """This target inherits from the target class.  This target was added as an addition to the assignment and
functions similar to the Strong_Target but takes 10 hits to kill and has 2 times the diameter"""
    
    def __init__(self):
        super().__init__()
        self.lives = 10
        self.radius = TARGET_RADIUS * 2
        self.dx = random.uniform(1.00, 3.00)
        self.dy = random.uniform(-2.00, 3.00)
        
    def draw(self):
        arcade.draw_circle_outline(self.center.x, self.center.y, TARGET_RADIUS*2, arcade.color.VIOLET_BLUE)
        text_x = self.center.x - (self.radius / 2)
        text_y = self.center.y - (self.radius / 2)
        arcade.draw_text(repr(self.lives), text_x, text_y, arcade.color.VIOLET_BLUE, font_size=20)
    
    def hit(self):
        self.lives -= 1
        if self.lives == 0:
            self.alive = False
            return self.score + 10
        else:
            return self.score + 1

class Rifle:
   
    """The rifle is a rectangle that tracks the mouse."""

    def __init__(self):
        self.center = Point()
        self.center.x = 0
        self.center.y = 0
        self.angle = 45

    def draw(self):
        arcade.draw_rectangle_filled(self.center.x, self.center.y, RIFLE_WIDTH, RIFLE_HEIGHT, RIFLE_COLOR, self.angle)


class Game(arcade.Window):
    
    """This class handles all the game callbacks and interaction
    It assumes the following classes exist:
        Rifle
        Target (and it's sub-classes)
        Point
        Velocity
        Bullet
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class, but mostly
    you shouldn't have to. There are a few sections that you
    must add code to.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)

        self.rifle = Rifle()
        self.score = 0

        self.bullets = []

        # TODO: Create a list for your targets (similar to the above bullets)
        self.targets = []


        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        # draw each object
        self.rifle.draw()

        for bullet in self.bullets:
            bullet.draw()

        # TODO: iterate through your targets and draw them...
        for target in self.targets:
            target.draw()

        self.draw_score()

    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.NAVY_BLUE)

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_collisions()
        self.check_off_screen()

        # decide if we should start a target
        if random.randint(1, 50) == 1:
            self.create_target()

        for bullet in self.bullets:
            bullet.advance()

        # TODO: Iterate through your targets and tell them to advance
        for target in self.targets:
            target.advance()
        

    def create_target(self):
        """
        Creates a new target of a random type and adds it to the list.
        :return:
        """

        # TODO: Decide what type of target to create and append it to the list
        target = Target()
        strong_target = Strong_Target()
        safe_target = Safe_Target()
        super_strong = Super_Strong()
        
        
        if len(self.targets) == 0:
            self.targets.append(target)
            self.targets.append(strong_target)
            self.targets.append(safe_target)
            self.targets.append(super_strong)
        
        
        
        
        
    def check_collisions(self):
        """
        Checks to see if bullets have hit targets.
        Updates scores and removes dead items.
        :return:
        """

        # NOTE: This assumes you named your targets list "targets"

        for bullet in self.bullets:
            for target in self.targets:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and target.alive:
                    too_close = bullet.radius + target.radius

                    if (abs(bullet.center.x - target.center.x) < too_close and
                                abs(bullet.center.y - target.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        self.score += target.hit()
                        
                        # We will wait to remove the dead objects until after we
                        # finish going through the list

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for target in self.targets:
            if not target.alive:
                self.targets.remove(target)

    def check_off_screen(self):
        """
        Checks to see if bullets or targets have left the screen
        and if so, removes them from their lists.
        :return:
        """
        for bullet in self.bullets:
            if bullet.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.bullets.remove(bullet)

        for target in self.targets:
            if target.is_off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                self.targets.remove(target)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # set the rifle angle in degrees
        self.rifle.angle =  self._get_angle_degrees(x, y)
        
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        # Fire!
        angle = self._get_angle_degrees(y, x)

        bullet = Bullet()
        bullet.fire(angle)

        self.bullets.append(bullet)

    def _get_angle_degrees(self, x, y):
        """
        Gets the value of an angle (in degrees) defined
        by the provided x and y.
        
        """
        # get the angle in radians
        angle_radians = math.atan2(x, y)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
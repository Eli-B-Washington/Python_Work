"""
This program implements the asteroids game.
"""
import arcade
import math
import random
import threading


# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2







class Point:
    """initiates point location at a random start."""
    
    def __init__(self):
        self.x = random.uniform(0.00, 0.00)
        self.y = random.uniform(0.00, 0.00)
        
class Velocity:
    """Initiates velocity"""
    def __init__(self):
        self.dx = random.uniform(0.00, 0.00)
        self.dy = random.uniform(0.00, 0.00) 
        


class Flying:
    
    """Base class for flying objects"""
    def __init__(self):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.radius = SHIP_RADIUS
        self.speed = 0
        self.direction = 0
        self.angle = 0
        
    def advance(self):
        self.wrap()
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
        
    """ Allows flying objects to wrap from one side of the screen to the other side"""     
    def wrap(self):
        if self.center.x > SCREEN_WIDTH:
            self.center.x -= SCREEN_WIDTH
        if self.center.x < 0:
            self.center.x += SCREEN_WIDTH
        if self.center.y > SCREEN_HEIGHT:
            self.center.y -= SCREEN_HEIGHT
        if self.center.y < 0:
            self.center.y += SCREEN_HEIGHT
            
    
class Bullet(Flying):
    """Class for bullets that will be fired from the rifle"""
    def __init__(self, angle, x, y, dx, dy):
        super().__init__()
        self.speed = BULLET_SPEED
        self.lives = BULLET_LIFE
        self.radius = BULLET_RADIUS
        self.angle = angle
        self.center.x = x
        self.center.y = y
        self.speed_x = abs(dx) + BULLET_SPEED
        self.speed_y = abs(dy) + BULLET_SPEED
        

    def draw(self):
        texture = arcade.load_texture("images/laserBlue01.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width, texture.height, texture, self.angle , 255)
    
    
    def fire(self):
        self.velocity.dx -= (math.cos(math.radians(self.angle -90))) * self.speed_x
        self.velocity.dy += (math.sin(math.radians(self.angle +90))) * self.speed_y
        
    def advance(self):
        super().advance()
        self.lives -= 1
        if (self.lives <= 0):
            self.alive = False
        
        
        

class Ship(Flying):
    """Inherits from Flying and initializes the ship class"""
    def __init__(self):
        super().__init__()
        self.center.x = (SCREEN_WIDTH/2)
        self.center.y = (SCREEN_HEIGHT/2)
        self.radius = SHIP_RADIUS
        self.angle = 1
        self.health = 5
        
        
        
    def draw(self):
        texture = arcade.load_texture("images/playerShip1_orange.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width, texture.height, texture, self.angle, 255)
        
    def hit(self):
        self.health -= 1
        if self.health == 0:
            self.alive = False
    
    def left(self):
        self.angle += SHIP_TURN_AMOUNT
    
    def right(self):
        self.angle -= SHIP_TURN_AMOUNT
        
    def move_forward(self):
        self.velocity.dx -= math.cos(math.radians(self.angle-90)) * SHIP_THRUST_AMOUNT
        self.velocity.dy += math.sin(math.radians(self.angle+90)) * SHIP_THRUST_AMOUNT
    
    def move_backward(self):
        self.velocity.dx += math.cos(math.radians(self.angle-90)) * SHIP_THRUST_AMOUNT
        self.velocity.dy -= math.sin(math.radians(self.angle+90)) * SHIP_THRUST_AMOUNT
    
        

class Asteroid(Flying):
    """ This is the large asteroid.  It will break apart into 2 medium asteroids and 1 small asteroid"""
    def __init__(self):
        super().__init__()
        self.score = 0
        self.center.x = random.randint(1, 50)
        self.center.y = random.randint(1, 500)
        self.direction = random.randint(1,50)
        self.velocity.dx = math.cos(math.radians(self.direction)) * BIG_ROCK_SPEED
        self.velocity.dy = math.sin(math.radians(self.direction)) * BIG_ROCK_SPEED
        self.angle = BIG_ROCK_SPIN
        self.radius = BIG_ROCK_RADIUS
        
        
    def draw(self):
        
        texture = arcade.load_texture("images/meteorGrey_big1.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width, texture.height, texture, self.angle, 255)
        
        
    def hit(self):
        self.alive = False
        return self.score + 1
    
    def rotate(self):
        self.angle += 1
    
    def split_apart(self, asteroids):
        medium_1 = Medium_Asteroid()
        medium_1.center.x = self.center.x
        medium_1.center.y = self.center.y
        medium_1.velocity.dy = self.velocity.dy + 2
        
        medium_2 = Medium_Asteroid()
        medium_2.center.x = self.center.x
        medium_2.center.y = self.center.y
        medium_2.velocity.dy = self.velocity.dy - 2
        
        small_1 = Small_Asteroid()
        small_1.center.x = self.center.x
        small_1.center.y = self.center.y
        small_1.velocity.dx = self.velocity.dx + 5
        
        asteroids.append(medium_1)
        asteroids.append(medium_2)
        asteroids.append(small_1)
        
        self.alive = False
        


class Medium_Asteroid(Asteroid):
    
    """This is a medium asteroid.  It will break into 2 smaller asteroids when it gets hit."""
   
    def __init__(self):
        super().__init__()
        self.radius = MEDIUM_ROCK_RADIUS
        self.angle = MEDIUM_ROCK_SPIN
    
    def draw(self):
        texture = arcade.load_texture("images/meteorGrey_med1.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width, texture.height, texture,self.angle, 255) 
    
    def hit(self):
        self.alive = False
        return self.score + 1
        
    
    def split_apart(self, asteroids):
        small_1 = Small_Asteroid()
        small_1.center.x = self.center.x
        small_1.center.y = self.center.y
        small_1.velocity.dy = self.velocity.dy + 1.5
        small_1.velocity.dx = self.velocity.dx + 1.5
        
        small_2 = Small_Asteroid()
        small_2.center.x = self.center.x
        small_2.center.y = self.center.y
        small_2.velocity.dy = self.velocity.dy - 1.5
        small_2.velocity.dx = self.velocity.dx - 1.5
        
        asteroids.append(small_1)
        asteroids.append(small_2)
        self.alive = False
    
class Small_Asteroid(Asteroid):
    
    """This is a small asteroid.  It will be removed from the game when it is hit"""
        
    def __init__(self):
        super().__init__()
        self.radius = SMALL_ROCK_RADIUS
        self.angle = SMALL_ROCK_SPIN
    
    def draw(self):
        texture = arcade.load_texture("images/meteorGrey_small1.png")
        arcade.draw_texture_rectangle(self.center.x, self.center.y, texture.width, texture.height, texture,self.angle, 255)
    
    def hit(self):
        self.alive = False
        return self.score + 1
    
    def split_apart(self, asteroids):
        self.alive = False
    
    
        
    




class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        self.ship = Ship()
        self.score = 0
        self.lives = 0
        self.bullets = []
        
        self.asteroids = []
        
        
        
        
        

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        

            
        
        # clear the screen to begin drawing
        
        arcade.start_render()
        
        self.background = arcade.load_texture("images/Space_background.jpg")
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # TODO: draw each object
        #Needs to be edited
        
        
        
        
        
        for bullet in self.bullets:
            bullet.draw()

        
        for asteroid in self.asteroids:
            asteroid.draw()

        self.draw_score()
        self.draw_lives()
        
        if self.score < 10:
            arcade.draw_text("Score 30 Points to Win!", 300, 500, arcade.color.WHITE, 15,)
        
        if (self.ship.alive):
            self.ship.draw()
        else:
            arcade.draw_text("You lost...", 300, 300, arcade.color.WHITE, 50,)
            arcade.draw_text("Better Luck Next Time", 300, 150, arcade.color.WHITE, 23,)
            
        if self.score >= 30 and self.score <= 50:
            arcade.start_render()
        
            self.background = arcade.load_texture("images/Space_background.jpg")
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
            arcade.draw_text("You Won!!", 300, 500, arcade.color.WHITE, 50,)
            self.ship.draw()
        
    def draw_score(self):
        
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 40
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=30, color=arcade.color.YELLOW)
        
    def draw_lives(self):
        
        score_text = "Health: {}".format(self.ship.health)
        start_x = 10
        start_y = SCREEN_HEIGHT - 80
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=30, color=arcade.color.YELLOW)
        
        

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        # TODO: Tell everything to advance or move forward one step in time

        # TODO: Check for collisions
        self.check_collisions()
        
        
        while (self.asteroids)== [] :
            self.create_asteroid()
            self.create_asteroid()
            self.create_asteroid()
            self.create_asteroid()
            self.create_asteroid()
            
            

        for bullet in self.bullets:
            bullet.advance()
        self.cleanup_zombies()
                

        # TODO: Iterate through your targets and tell them to advance
        for asteroid in self.asteroids:
            asteroid.advance()
            asteroid.rotate()
        
        self.ship.advance()
        
    
    def create_asteroid(self):
        
        asteroid = Asteroid()
        self.asteroids.append(asteroid)
        
            

                
    
    def check_collisions(self):
        
        """This class detects bullet collisions with asteroids and asteroids collisions with the ship"""
        
        
        for asteroid in self.asteroids:
            if self.ship.alive and asteroid.alive:
                too_close = self.ship.radius + asteroid.radius
                
                if(abs(self.ship.center.x - asteroid.center.x) < too_close and
                           abs(self.ship.center.y - asteroid.center.y) < too_close):
                    
                    asteroid.alive = False 
                    self.ship.hit()
        
        
        for bullet in self.bullets:
            for asteroid in self.asteroids:

                # Make sure they are both alive before checking for a collision
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < too_close and
                                abs(bullet.center.y - asteroid.center.y) < too_close):
                        # its a hit!
                        bullet.alive = False
                        asteroid.split_apart(self.asteroids)
                        self.score += asteroid.hit()
        
        
                    
    
        self.cleanup_zombies()
    

      
   
        
    
    def cleanup_zombies(self):
        
        """This class removes elements that are not alive from the game"""
        
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)
        
        
        


    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.right()

        if arcade.key.UP in self.held_keys:
            self.ship.move_forward()

        if arcade.key.DOWN in self.held_keys:
            self.ship.move_backward()

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y, self.ship.velocity.dx, self.ship.velocity.dy)
                self.bullets.append(bullet)
                bullet.fire()
                

                
                
    def get_angle_degrees(self, x, y):
        
        angle_radians = math.atan2(y, x)

        # convert to degrees
        angle_degrees = math.degrees(angle_radians)

        return angle_degrees

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()
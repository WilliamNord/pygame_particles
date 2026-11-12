import pygame
import random
from pygame import Vector2
import numpy as np

# pos = (0,0)

vek = Vector2(2) - Vector2(3)

print(vek)

SCREEN_SIZE = Vector2(800, 600)

class Particle:
    def __init__(self, pos, vel, size: int, color, mass = 1):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        self.acc = Vector2(0, 0)
        
        self.size = size
        self.color = color
        self.mass = mass
    
    def apply_force(self, force):
        # F = m*a => a = F/m
        self.acc += force / self.mass
        
    def update(self, dt):
        #Akselerasjon
        self.vel += self.acc * dt
        
        #Friksjon / demping av fart slik at systemet gradvis "mister energi"
        self.vel *= 0.98
        
        #oppdaterer posisjon bassert på fart
        self.pos += self.vel * dt
        
        self.acc = Vector2(0,0)

        #Spretter med venstre vegg av spillet
        #Hvis sentrum til partikkelet er nærmere veggen enn radiusen, er partikkelet inni veggen og må sprette tilbake
        if self.pos.x < self.size:
            self.pos.x = self.size
            self.vel.x *= -1
        elif self.pos.x > SCREEN_SIZE.x - self.size:
            self.pos.x = SCREEN_SIZE.x - self.size
            self.vel.x *= -1

        if self.pos.y < self.size:
            self.pos.y = self.size
            self.vel.y *= -1
        elif self.pos.y > SCREEN_SIZE.y - self.size:
            self.pos.y = SCREEN_SIZE.y - self.size
            self.vel.y *= -1
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.size)

class Particle_Manager:
    def __init__(self):
        self.particles = []
    
    def add(self, particles: list[Particle]):
        #extend legget hvert element i en iterable til slutten av listen
        self.particles.extend(particles)
        
    def grav_Force(self, distance, p1_mass, p2_mass):
        """
        F = (G* M1 * M2) / (R^2)

        Args:
            distance (float): avstand mellom to partikkler
            p1_mass (int): vekten til partikkel 1
            p2_mass (int): vekten til partikkel 2

        Returns:
            float: akselerasjon fra tyngdekraft
        """
        grav_const = 10000
        return (grav_const * p1_mass * p2_mass) / (distance**2)
    
    def apply_forces(self):
        num = len(self.particles)
        
        for i in range(num):
            p1: Particle = self.particles[i]
            for j in range(i + 1, num):
                p2: Particle = self.particles[j]
                
                diff: Vector2 = p2.pos - p1.pos
                raw_dist = diff.length()
                
                if raw_dist == 0:
                    p1.pos.x += random.uniform(-0.1, 0.1)
                    p1.pos.y += random.uniform(-0.1, 0.1)
                    continue
                
                if raw_dist > 150:
                    continue
                
                #Vi har garantert at diff og raw_dist ikke er null
                direction = diff.normalize()
                min_dist = p1.size + p2.size + 10
                
                if raw_dist < min_dist:
                    strength = (min_dist - raw_dist) * 25
                    force = direction * strength
                    p1.apply_force(-force)
                    p2.apply_force(force)
                else:
                    #Hvis partiklene er langt nok unna så drar de til hverandre
                    strength = self.grav_Force(raw_dist, p1.mass, p2.mass)
                    force = direction * strength
                    #Direction er FRA p1 TIL p2. For å dra må vi flytte p1 mot p2 og p2 mot p1
                    p1.apply_force(force)
                    p2.apply_force(-force)
                
    def update(self, dt):
        self.apply_forces()
        for particle in self.particles:
            particle.update(dt)
    
    
    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)

    def __len__(self):
        return len(self.particles)


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock() 
        self.running = False
        self.PM = Particle_Manager()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        
        self.spawn_particle(60)
    
    def spawn_particle(self, number):
        new_particles = []
        
        rand_colors = ["red", "green", "blue"]
        
        for i in range(number):
            pos = Vector2(
                random.uniform(50, SCREEN_SIZE.x - 50),
                random.uniform(50, SCREEN_SIZE.y - 50)
            )
            #tilfelldig startfart
            vel = Vector2(random.uniform(-30, 30), random.uniform(-30, 30))
            
            new_particles.append(Particle(pos, vel, size=2, color=random.choice(rand_colors)))
        
        self.PM.add(new_particles)
            
    def update(self, dt):
        if pygame.mouse.get_pressed()[0]:
            pos = Vector2(pygame.mouse.get_pos())
            offset = Vector2(random.uniform(-5, 5), random.uniform(-5, 5))
            self.PM.add( [Particle(pos + offset, vel=Vector2(0,0), size=4, color="white",mass=10)] )
        
        self.PM.update(dt)
    
    def draw(self, surface):
        
        surface.fill('black')
        
        self.PM.draw(surface)
        
        pygame.display.flip()
    
    def run(self):
        
        self.running = True
        
        while self.running:
            dt = self.clock.tick() * 0.001
            
            self.fps = self.clock.get_fps()
            pygame.display.set_caption(f"FPS: {round(self.fps, -1)} | Antall partikler: {len(self.PM)}")
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        
        
            self.update(dt)
            self.draw(self.screen)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
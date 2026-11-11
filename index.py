import pygame
from pygame import Vector2

# pos = (0,0)

vek = Vector2(2) - Vector2(3)

print(vek)

SCREEN_SIZE = Vector2(600, 600)

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
    
    def add(self, particles):
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
        grav_const = 500
        return (grav_const * p1_mass, p2_mass) / (distance**2)
    
    def apply_forces(self):
        for p1 in self.particles:
            p1: Particle
            
            for p2 in self.particles:
                p2: Particle
                
                if p2 == p1:
                    continue
                
                diff: Vector2 = p2.pos - p1.pos
                #Får error hvis vi må dele på null og ungå å påvirke kuler som er for langt unna (sparer arbeid)
                dist = min(max(diff.length(), 0.01), p1.size * 5)
                
                direction = diff.normalize()
                min_dist = p1.size + p2.size + 10
                
                if dist < min_dist:
                    strength = (min_dist - dist) * 25
                    force = direction * strength
                    p1.apply_force(force)
                    p2.apply_force(-force)
                else:
                    #Hvis partiklene er langt nok unna så drar de til hverandre
                    strength = self.grav_Force(dist, p1.mass, p2.mass)
                    force = direction * strength
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
    
    def update(self, dt):
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
            pygame.display.set_caption(f"FPS: {self.fps}")
            
            for event in pygame.event.get():
                if event.type == pygame.quit:
                    self.running = False
        
        
        self.update(dt)
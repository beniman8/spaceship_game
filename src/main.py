from typing import Any
import pygame
from os.path import join
from random import randint,uniform


class Player(pygame.sprite.Sprite):
    
    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.image = pygame.image.load(join('images','player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))   
        self.direction =  pygame.math.Vector2()
        self.speed = 300
        
        
        # cooldown 
        self.can_shoot = True 
        self.laser_shoot_time = 0 
        self.cooldown_duration = 400

        
        # mask 
        self.mask = pygame.mask.from_surface(self.image)
        
        
        
    def laser_timer(self):
        
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
        
    def update(self, dt) -> None:
    
        keys  = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf,self.rect.midtop,(all_sprite,laser_sprite))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
            
        self.laser_timer()     
        
        
        return super().update()   

class Star(pygame.sprite.Sprite):
    def __init__(self, groups,star_surf) -> None:
        super().__init__(groups)
        self.original_surf = star_surf
        self.image= self.original_surf
        self.rect = self.image.get_frect(center= (randint(10,WINDOW_WIDTH),randint(10,WINDOW_HEIGHT)))
        self.speed = randint(400,500)
        self.rotation = 0
        self.rotation_speed= uniform(10,100)
        self.star_size = uniform(0.01,1)
    def update(self, *args: Any, **kwargs: Any) -> None:
        
                #continues rotation
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf,self.rotation,self.star_size)
        self.rect = self.image.get_frect(center = self.rect.center)
        return super().update(*args, **kwargs)

class Laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups ) -> None:
        super().__init__(groups)
        self.image = surf 
        self.rect = self.image.get_frect(midbottom=pos)

        
    def update(self,dt) -> None:
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
        return super().update()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups,meteor_surf) -> None:
        super().__init__(groups)
        self.original_surf = meteor_surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center=(randint(10,WINDOW_WIDTH),randint(-200,-100)))
        self.lifetime = 3000
        self.start_time = pygame.time.get_ticks()
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.speed = randint(400,500)
        self.rotation = 0
        self.rotation_speed= uniform(10,100)

    def update(self,dt) -> None:
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
            
        #continues rotation
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf,self.rotation,1)
        self.rect = self.image.get_frect(center = self.rect.center)
            
        return super().update()
class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames,pos,groups) -> None:
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
        explosion_sound.play()
        
    def update(self, dt) -> None:
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill
        return super().update()

def collisions():
    global running
    collisions_sprites = pygame.sprite.spritecollide(player,meteor_sprite,True,pygame.sprite.collide_mask)
    if collisions_sprites:
        running = False
    
    for laser in laser_sprite:
        collided_sprites = pygame.sprite.spritecollide(laser,meteor_sprite,True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames,laser.rect.midtop,all_sprite)
            

def display_score():
    current_time = pygame.time.get_ticks() #// 100
    text_surf = font.render(str(current_time),True,(240,240,240))
    text_rect = text_surf.get_frect(midbottom= (WINDOW_WIDTH/2,WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface,(240,240,240),text_rect.inflate(20,10).move(0,-10),5,10)
    

# general setup
pygame.init()
WINDOW_WIDTH,WINDOW_HEIGHT = 1280,720
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
running = True
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()

# imports
star_surf = pygame.image.load(join('images','star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images','meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images','laser.png')).convert_alpha()
font = pygame.font.Font(join('images','Oxanium-Bold.ttf'),50)
explosion_frames = [pygame.image.load(join('images','explosion',f'{i}.png')).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join('audio','laser.wav'))
laser_sound.set_volume(0.5)

explosion_sound = pygame.mixer.Sound(join('audio','explosion.wav'))
game_music_sound = pygame.mixer.Sound(join('audio','game_music.wav'))
damage_sound = pygame.mixer.Sound(join('audio','damage.ogg'))
game_music_sound.play(loops=-1).set_volume(0.5)

# sprites
all_sprite = pygame.sprite.Group()
meteor_sprite = pygame.sprite.Group()
laser_sprite = pygame.sprite.Group()
for i in range(50):
    Star(all_sprite,star_surf)
player = Player(all_sprite)

# custom events -> meteor event 
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event,1000)

while running:
    #delta time
    dt = clock.tick() / 1000
    
    # event loop 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor((all_sprite, meteor_sprite),meteor_surf=meteor_surf)
    #update
    all_sprite.update(dt)
    collisions()

    # draw the game
    display_surface.fill('#3a2e3f')
    display_score()
    all_sprite.draw(display_surface) 
    
    

    pygame.display.update()
    
pygame.quit()
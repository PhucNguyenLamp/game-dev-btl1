# game-dev-btl1
## How to run the game 
- Run `pip install pygame numpy` for the libraries
- Navigate to project root, and run `main.py`, Example: `~\game-dev-btl1> python main.py`

## interface 
<img width="1124" height="787" alt="preview" src="https://github.com/user-attachments/assets/1acb5fac-02f9-4d77-8835-d2474727340d" />

## how to play the game
- left click to hit the zombies
- the sound control is on the right, hit it to toggle mute
- score and accuracy are on the left

## Game flow
- Initially, the player will meet the starting screen showing the game name and the starting button
- Press the button, and the player should go on to the main game play
- Player use left click to smash the zombie, and player will earn point
- If player do not smash the zombie in time, it will count as a miss
- The player should defend from the zombie throught out the night (as 60 second in real time)
- Additionally, player can mute the game background.
- Once the night ended, the player should see their score, miss and accuracy with the button to restart the game
- If press the restart button, the player will be taken back to the staring screen

## file structure:
```
game-dev-btl1/
├─ README.md
├─ main.py
├─ audio/
│  └─ sound.py
├─ entities/
│  └─ zombie.py
├─ graphics/
│  └─ utils.py
├─ particles/
│  └─ Particle.py
├─ ui/
│  ├─ button.py
│  ├─ hud.py
│  ├─ overlay.py
│  ├─ start_screen.py
│  ├─ timer.py
│  └─ ui.py
└─ assets/
   ├─ audio/
   │  ├─ bg_music.mp3
   │  ├─ hammer_swing.mp3
   │  └─ zombie_hit.mp3
   ├─ fonts/
   │  └─ Terraria.TTF
   └─ sprites/
      ├─ bg.png
      ├─ grass_mask.png
      ├─ hammer_hit.png
      ├─ hammer.png
      ├─ mute.png
      ├─ old_mute.png
      ├─ old_unmute.png
      ├─ sound.png
      ├─ tombstone.png
      ├─ zombie_despawn.png
      ├─ zombie_spawn.png
      └─ zombie.png
```

## Sprite and sounds reference
- Zombie & Tombstone & Background: ChatGPT & Google AI Studio
- Audio: [Youtube](https://youtu.be/ehMCqtBBUXU?si=lqXwqGVXCfvj5hLL)
- Other: [Terraria Wiki](https://terraria.fandom.com/wiki/Terraria_Wiki) 






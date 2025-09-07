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

## file structure:
```
whack_a_zombie/
├─ README.md
├─ requirements.txt
├─ main.py
├─ config.py
├─ game.py
├─ managers/ # not implemented yet
│  └─ spawn_manager.py
├─ entities/
│  └─ zombie.py
├─ ui/
│  └─ hud.py
├─ input/
│  └─ input.py
├─ audio/
│  └─ sound.py
├─ utils/
│  ├─ timer.py
│  └─ rand.py
└─ assets/
   ├─ sprites/
   │  ├─ bg.png
   │  └─ zombie_head.png
   └─ audio/
      ├─ bgm.mp3
      └─ hit.wav

```

## note
video tutorial chung thư viện: https://www.youtube.com/watch?v=blLLtdv4tvo
docs thư viện (rất có ích): https://www.pygame.org/docs/ref/mouse.html






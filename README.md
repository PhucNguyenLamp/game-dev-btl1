# game-dev-btl1
## How to run the game 
- Run `pip install pygame numpy` for the libraries
- Navigate to project root, and run `main.py`, Example: `~\game-dev-btl1> python main.py`

## interface 
<img width="502" height="415" alt="interface" src="https://github.com/user-attachments/assets/9d12e899-0090-4023-9bf3-89690f377296" />

## how to play the game
- left click to hit the zombies
- the sound control is on the right, hit it to toggle mute
- score and accuracy are on the left

## note
video tutorial chung thư viện: https://www.youtube.com/watch?v=blLLtdv4tvo

docs thư viện (rất có ích): https://www.pygame.org/docs/ref/mouse.html

file structure chi tiết: https://chatgpt.com/s/t_68ad454177f88191baf757171dc85279

## file structure:
```
whack_a_zombie/
├─ README.md
├─ requirements.txt
├─ main.py
├─ config.py
├─ game.py
├─ managers/
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




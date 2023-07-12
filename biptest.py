import pygame
import math
import numpy as np

# Your script code goes here

# Initialize pygame
pygame.init()

# Play a tone when the script is done
frequency = 880  # Frequency of the tone in Hz (A4 note)
duration = 1000  # Duration of the tone in milliseconds (1 second)
volume = 0.5  # Volume of the tone (0.0 to 1.0)

sample_rate = 20000  # Sample rate in Hz (standard for most audio)
num_samples = int(sample_rate * duration / 1000)
amplitude = int(volume * 2 ** 15)

sound_data = []
for i in range(num_samples):
    value = int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate))
    sound_data.append((value, value))

sound_data = np.array(sound_data, dtype=np.int16)

sound = pygame.sndarray.make_sound(sound_data)
sound.play()

pygame.time.wait(duration)

# Quit pygame
pygame.quit()
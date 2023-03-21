import time, platform, sys

def finish_alarm():
    if platform.system() == 'Windows':
        import winsound
        for i in range(3):
            winsound.MessageBeep()
            time.sleep(2)
    elif platform.system() == 'Darwin':  # macOS
        import AppKit
        sound = AppKit.NSSound.alloc()
        sound.initWithContentsOfFile_byReference_('/System/Library/Sounds/Basso.aiff', True)
        sound.play()
    elif platform.system() == 'Linux':
        # 예시로 pygame 라이브러리를 사용하여 소리를 재생합니다.
        import pygame

        pygame.mixer.init()
        pygame.mixer.music.load('../alarm/alarm.wav')
        pygame.mixer.music.play()
    else:
        sys.stderr.write('Unsupported platform: %s' % platform.system())
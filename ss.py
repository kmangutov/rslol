import time
import pyautogui
for i in range(0, 50):
	time.sleep(5)
	ss = pyautogui.screenshot()
	ss.save('screenshots/' + str(i) + '.png')

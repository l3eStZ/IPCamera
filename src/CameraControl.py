class CameraControl():
    def __init__(self, camera, key=None):
        self.camera = camera
        self.key = None

    def control(self, key_press):
        self.key = key_press

        if key_press == 'i':
            self.camera.current_loc()
        elif key_press == 'a':
            self.camera.move_pan(-1.0, 1)
        elif key_press == 'd':
            self.camera.move_pan(1.0, 1)
        elif key_press == 'w':
            self.camera.move_tilt(-1.0, 2)
        elif key_press == 's':
            self.camera.move_tilt(1.0, 2)
        elif key_press == 't':
            self.camera.get_preset()
        elif key_press == 'g':
            self.camera.set_preset('home')
        elif key_press == 'h':
            self.camera.goto_preset('home')
        elif key_press == 'r':
            self.camera.remove_preset()
        return True
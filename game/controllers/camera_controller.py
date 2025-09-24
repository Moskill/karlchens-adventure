from ursina import camera, Vec3, time

class CameraController:
    def __init__(self, center: Vec3, w: int, h: int, padding=2.0):
        self.center = center
        self.half_r = (w/2) + padding
        self.half_u = (h/2) + padding

    def setup_iso(self, fov_factor=1.35, yaw=-45, pitch=55, dist_factor=0.9, height_factor=0.5):
        W = self.half_r*2 - 2  # grobe Rückrechnung nur für FOV/Dist
        H = self.half_u*2 - 2
        s = max(W, H)
        camera.orthographic = True
        camera.fov = max(20, s * fov_factor)
        camera.rotation_x = pitch
        camera.rotation_y = yaw
        dist   = s * dist_factor
        height = s * height_factor
        camera.position = (self.center.x + dist * 0.707, height, self.center.z - dist * 0.707)
        camera.look_at(self.center)

    def _basis(self):
        r = Vec3(camera.right.x, 0, camera.right.z)
        u = Vec3(camera.up.x,    0, camera.up.z)
        if r.length(): r = r.normalized()
        if u.length(): u = u.normalized()
        return r, u

    def pan_step(self, base_speed=32.0):
        return (camera.fov / 40.0) * base_speed * time.dt

    def pan_screen(self, dx_screen: float, dy_screen: float):
        r, u = self._basis()
        move = r * dx_screen + u * dy_screen
        self._apply_obb(move)

    def zoom_ortho(self, delta: float, lo=10, hi=80):
        camera.fov = max(lo, min(hi, camera.fov + delta))

    def _apply_obb(self, move):
        pos = Vec3(camera.position) + move
        r, u = self._basis()
        rel = pos - self.center
        pr = max(-self.half_r, min(self.half_r, rel.dot(r)))
        pu = max(-self.half_u, min(self.half_u, rel.dot(u)))
        new_pos = self.center + r*pr + u*pu
        camera.position = (new_pos.x, camera.position.y, new_pos.z)

    def set_extra_bottom(self, factor: float):
        """Optional asymmetrisch unten mehr erlauben (z. B. factor=2.0)"""
        self.half_u *= factor

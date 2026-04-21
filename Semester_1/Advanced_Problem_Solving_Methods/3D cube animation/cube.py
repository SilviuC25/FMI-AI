from vpython import canvas, vec, rate, sphere, color, slider, wtext, scene, button, box
import numpy as np
import math
import time

MAX_PARTICLES = 150
INITIAL_PARTICLES = 50
DT = 0.02
CUBE_SIZE = 2.0
SUBDIV = 4
SUBCUBE_SIZE = CUBE_SIZE / SUBDIV
PARTICLE_RADIUS = 0.05
PARTICLE_MASS = 0.02
REST_PARTICLE = 0.92
REST_WALL = 0.85
ENTROPY_DECAY = 0.985
ENTROPY_SCALE_COLLISION = 1.0
ENTROPY_SCALE_KE = 0.8
PARTICLE_ENTROPY_DECAY = 0.992

scene.title = "3D Particle Cube with Entropy"
scene.width = 1200
scene.height = 820
scene.background = vec(0.05, 0.05, 0.06)
scene.center = vec(0, 0, 0)
scene.forward = vec(-1, -1, -1)

half = CUBE_SIZE / 2.0

subcubes = []
for i in range(SUBDIV):
    for j in range(SUBDIV):
        for k in range(SUBDIV):
            pos_sub = vec(-half + (i + 0.5) * SUBCUBE_SIZE,
                          -half + (j + 0.5) * SUBCUBE_SIZE,
                          -half + (k + 0.5) * SUBCUBE_SIZE)
            sc = box(pos=pos_sub, size=vec(SUBCUBE_SIZE * 0.96, SUBCUBE_SIZE * 0.96, SUBCUBE_SIZE * 0.96),
                     color=color.white, opacity=0.06)
            subcubes.append({'box': sc, 'entropy': 0.0, 'particles': []})

particles_pos = np.random.uniform(-half + PARTICLE_RADIUS, half - PARTICLE_RADIUS, size=(MAX_PARTICLES, 3))
particles_vel = np.random.uniform(-1.0, 1.0, size=(MAX_PARTICLES, 3))
particles_entropy = np.zeros((MAX_PARTICLES,), dtype=np.float32)
particles_collision_count = np.zeros((MAX_PARTICLES,), dtype=np.int32)
particles_spheres = []
particles_entropy_cubes = []
for i in range(MAX_PARTICLES):
    s = sphere(pos=vec(*particles_pos[i]), radius=PARTICLE_RADIUS, color=color.red, make_trail=False, visible=False)
    ec = box(pos=vec(*particles_pos[i]) + vec(0, PARTICLE_RADIUS + 0.02, 0), size=vec(PARTICLE_RADIUS * 1.2, PARTICLE_RADIUS * 1.2, PARTICLE_RADIUS * 1.2),
             color=color.cyan, opacity=0.25, visible=False)
    particles_spheres.append(s)
    particles_entropy_cubes.append(ec)

voxel_entropy = np.zeros((SUBDIV, SUBDIV, SUBDIV), dtype=np.float32)

state = {"num": INITIAL_PARTICLES, "speed": 1.0, "paused": False, "entropy_on": True}

def clamp_idx(v):
    if v < 0:
        return 0
    if v >= SUBDIV:
        return SUBDIV - 1
    return int(v)

def pos_to_index(p):
    ix = clamp_idx(int((p[0] + half) / SUBCUBE_SIZE))
    iy = clamp_idx(int((p[1] + half) / SUBCUBE_SIZE))
    iz = clamp_idx(int((p[2] + half) / SUBCUBE_SIZE))
    return ix, iy, iz

def color_gradient(v):
    v = max(0.0, min(1.0, v))
    if v < 0.17:
        t = v / 0.17
        return vec(0.0, 0.0 + 0.5 * t, 1.0 - 1.0 * t)
    elif v < 0.33:
        t = (v - 0.17) / (0.16)
        return vec(0.0, 0.5 + 0.5 * t, 0.0)
    elif v < 0.5:
        t = (v - 0.33) / 0.17
        return vec(0.0 + t * 1.0, 1.0 - t * 0.25, 0.0)
    elif v < 0.67:
        t = (v - 0.5) / 0.17
        return vec(1.0, 0.75 + 0.25 * t, 0.0)
    elif v < 0.84:
        t = (v - 0.67) / 0.17
        return vec(1.0, 1.0 - 0.5 * t, 0.0 + 0.5 * t)
    else:
        t = (v - 0.84) / 0.16
        return vec(1.0, 0.5 + 0.5 * t, 0.5 + 0.5 * t)

def spawn_particle_at(i):
    margin = PARTICLE_RADIUS + 0.005
    x = np.random.uniform(-half + margin, half - margin)
    y = np.random.uniform(-half + margin, half - margin)
    z = np.random.uniform(-half + margin, half - margin)
    particles_pos[i, :] = (x, y, z)
    theta = np.random.uniform(0, 2 * math.pi)
    phi = np.random.uniform(0, math.pi)
    s = np.random.uniform(0.3, 1.2) * state["speed"]
    vx = s * math.sin(phi) * math.cos(theta)
    vy = s * math.cos(phi)
    vz = s * math.sin(phi) * math.sin(theta)
    particles_vel[i, :] = (vx, vy, vz)
    particles_entropy[i] = 0.0
    particles_collision_count[i] = 0
    particles_spheres[i].pos = vec(float(x), float(y), float(z))
    particles_spheres[i].visible = True
    particles_entropy_cubes[i].pos = vec(float(x), float(y + PARTICLE_RADIUS + 0.02), float(z))
    particles_entropy_cubes[i].visible = state["entropy_on"]

def show_particle(i, enable):
    particles_spheres[i].visible = enable
    particles_entropy_cubes[i].visible = enable and state["entropy_on"]

def initialize_particles():
    for i in range(MAX_PARTICLES):
        particles_spheres[i].visible = False
        particles_entropy_cubes[i].visible = False
    for i in range(state["num"]):
        spawn_particle_at(i)
        show_particle(i, True)

def elastic_pair_collision(i, j):
    pi = particles_pos[i]
    pj = particles_pos[j]
    dp = pi - pj
    dist = np.linalg.norm(dp)
    min_dist = 2.0 * PARTICLE_RADIUS
    if dist == 0:
        return
    if dist < min_dist:
        n = dp / dist
        overlap = min_dist - dist
        particles_pos[i] += 0.5 * overlap * n
        particles_pos[j] -= 0.5 * overlap * n
        vi = particles_vel[i]
        vj = particles_vel[j]
        rel = vi - vj
        reln = np.dot(rel, n)
        if reln >= 0:
            return
        m1 = PARTICLE_MASS
        impulse = -(1 + REST_PARTICLE) * reln / (1 / m1 + 1 / m1)
        particles_vel[i] = vi + impulse * n / m1
        particles_vel[j] = vj - impulse * n / m1
        particles_collision_count[i] += 1
        particles_collision_count[j] += 1
        ix, iy, iz = pos_to_index(0.5 * (particles_pos[i] + particles_pos[j]))
        voxel_entropy[ix, iy, iz] += ENTROPY_SCALE_COLLISION
        particles_entropy[i] += ENTROPY_SCALE_COLLISION * 0.5
        particles_entropy[j] += ENTROPY_SCALE_COLLISION * 0.5

def wall_collisions(i):
    collided = False
    for d in range(3):
        if particles_pos[i, d] - PARTICLE_RADIUS < -half:
            particles_pos[i, d] = -half + PARTICLE_RADIUS
            particles_vel[i, d] = -particles_vel[i, d] * REST_WALL
            collided = True
        if particles_pos[i, d] + PARTICLE_RADIUS > half:
            particles_pos[i, d] = half - PARTICLE_RADIUS
            particles_vel[i, d] = -particles_vel[i, d] * REST_WALL
            collided = True
    if collided:
        ix, iy, iz = pos_to_index(particles_pos[i])
        voxel_entropy[ix, iy, iz] += ENTROPY_SCALE_COLLISION * 0.6
        particles_entropy[i] += ENTROPY_SCALE_COLLISION * 0.4
        particles_collision_count[i] += 1

def update_voxel_entropy_and_visuals():
    flat = voxel_entropy.flatten()
    maxv = float(np.max(flat)) if flat.size > 0 else 1.0
    maxv = max(maxv, 1e-6)
    idx = 0
    for sc in subcubes:
        v = voxel_entropy.flatten()[idx] / maxv
        sc['entropy'] = v
        sc['box'].color = color_gradient(v)
        sc['box'].opacity = 0.02 + 0.45 * v if state["entropy_on"] else 0.02
        idx += 1

def update_particle_entropy_visuals():
    maxp = max(1e-6, float(np.max(particles_entropy[:state["num"]])))
    for i in range(state["num"]):
        pe = particles_entropy[i] / maxp
        c = color_gradient(pe)
        s = 0.02 + 0.12 * min(1.0, pe * 1.8)
        particles_entropy_cubes[i].pos = vec(float(particles_pos[i, 0]), float(particles_pos[i, 1] + PARTICLE_RADIUS + s / 2 + 0.01), float(particles_pos[i, 2]))
        particles_entropy_cubes[i].size = vec(s, s, s)
        particles_entropy_cubes[i].color = c
        particles_entropy_cubes[i].opacity = 0.12 + 0.55 * min(1.0, pe)
        particles_entropy_cubes[i].visible = state["entropy_on"]

def set_num(v):
    v = int(v)
    prev = state["num"]
    state["num"] = v
    if v > prev:
        start = prev
        for i in range(start, v):
            spawn_particle_at(i)
            show_particle(i, True)
    elif v < prev:
        for i in range(prev - 1, v - 1, -1):
            show_particle(i, False)
    update_status()

def set_speed(v):
    state["speed"] = float(v)
    update_status()

def update_status():
    active = state["num"]
    status.text = f"\nParticles: {active}  Speed mult: {state['speed']:.2f}  Entropy Visible: {'ON' if state['entropy_on'] else 'OFF'}\n"

def toggle_pause(b):
    state["paused"] = not state["paused"]
    b.text = "Resume" if state["paused"] else "Pause"

def toggle_entropy(b):
    state["entropy_on"] = not state["entropy_on"]
    b.text = "Hide Entropy" if state["entropy_on"] else "Show Entropy"
    for i in range(state["num"]):
        particles_entropy_cubes[i].visible = state["entropy_on"]
    for sc in subcubes:
        sc['box'].opacity = 0.02 if not state["entropy_on"] else sc['box'].opacity
    update_status()

wtext(text=" Particle number: ")
num_slider = slider(bind=lambda s: set_num(s.value), min=4, max=MAX_PARTICLES, value=INITIAL_PARTICLES, length=360)
wtext(text="   Speed multiplier: ")
speed_slider = slider(bind=lambda s: set_speed(s.value), min=0.2, max=3.0, value=1.0, length=360)
status = wtext(text=f"\nParticles: {INITIAL_PARTICLES}  Speed mult: 1.00\n")
button(bind=toggle_pause, text="Pause")
button(bind=toggle_entropy, text="Show Entropy")

initialize_particles()
last_time = time.time()
while True:
    rate(1 / DT)
    now = time.time()
    elapsed = now - last_time
    last_time = now
    if state["paused"]:
        continue
    for i in range(state["num"]):
        particles_pos[i] += particles_vel[i] * DT * state["speed"]
    for i in range(state["num"]):
        wall_collisions(i)
    active_idx = np.arange(state["num"])
    n = len(active_idx)
    for a in range(n):
        i = active_idx[a]
        for b in range(a + 1, n):
            j = active_idx[b]
            elastic_pair_collision(i, j)
    for idx in range(state["num"]):
        particles_entropy[idx] *= PARTICLE_ENTROPY_DECAY
    for ix in range(SUBDIV):
        for iy in range(SUBDIV):
            for iz in range(SUBDIV):
                voxel_entropy[ix, iy, iz] *= ENTROPY_DECAY
    for idx in range(state["num"]):
        ix, iy, iz = pos_to_index(particles_pos[idx])
        ke = 0.5 * PARTICLE_MASS * float(np.dot(particles_vel[idx], particles_vel[idx]))
        voxel_entropy[ix, iy, iz] += ke * ENTROPY_SCALE_KE * DT
        particles_entropy[idx] += ke * ENTROPY_SCALE_KE * DT * 0.2
    update_voxel_entropy_and_visuals()
    update_particle_entropy_visuals()
    for i in range(state["num"]):
        particles_spheres[i].pos = vec(float(particles_pos[i, 0]), float(particles_pos[i, 1]), float(particles_pos[i, 2]))
    update_status()

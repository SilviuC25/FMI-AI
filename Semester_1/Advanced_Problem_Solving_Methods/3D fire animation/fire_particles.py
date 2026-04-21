from vpython import canvas, vec, rate, sphere, color, slider, wtext, scene, button, box
import numpy as np
import time
import math

MAX_PARTICLES = 800
INITIAL_ACTIVE = 300
BASE_EMIT_RATE = 24
DT = 0.03

scene.title = "3D Fire"
scene.width = 1100
scene.height = 700
scene.background = vec(0.03, 0.03, 0.04)
scene.center = vec(0, 1, 0)

pos = np.zeros((MAX_PARTICLES, 3), dtype=np.float32)
vel = np.zeros((MAX_PARTICLES, 3), dtype=np.float32)
life = np.zeros((MAX_PARTICLES,), dtype=np.float32)
alive = np.zeros((MAX_PARTICLES,), dtype=np.bool_)

spheres = []
for i in range(MAX_PARTICLES):
    s = sphere(pos=vec(0, -10, 0), radius=0.06, color=color.red, opacity=1.0, visible=False)
    spheres.append(s)

entropy_cubes = []
for i in range(MAX_PARTICLES):
    c = box(pos=vec(0, -10, 0), size=vec(0.12, 0.12, 0.12), color=color.cyan, opacity=0.35, visible=False)
    entropy_cubes.append(c)

stones = []
stone_count = 20
stone_ring_radius = 1.5
for i in range(stone_count):
    ang = 2 * math.pi * i / stone_count
    jitter_r = np.random.uniform(-0.08, 0.08)
    x = (stone_ring_radius + jitter_r) * math.cos(ang)
    z = (stone_ring_radius + jitter_r) * math.sin(ang)
    h = 0.08 + np.random.uniform(-0.03, 0.06)
    r = 0.12 + np.random.uniform(-0.04, 0.06)
    col = vec(0.2 + np.random.uniform(-0.03, 0.05), 0.18 + np.random.uniform(-0.03, 0.04), 0.16 + np.random.uniform(-0.03, 0.04))
    st = sphere(pos=vec(x, h, z), radius=r, color=col, shininess=0.2)
    stones.append(st)

ground = box(pos=vec(0, -0.06, 0), size=vec(10, 0.12, 10), color=vec(0.08, 0.06, 0.04), shininess=0.1)

state = {"active": INITIAL_ACTIVE, "energy": 1.0, "paused": False, "entropy_visible": False}

ENERGY_KJ_PER_UNIT = 25.0
E_REF_KJ = 25.0
BUOY_COEFF = 1.2
DRAG_COEFF = 0.6
TURB_SCALE = 0.9
PARTICLE_MASS = 0.02

def set_count(v):
    state['active'] = int(v)
    update_status()

def set_energy(v):
    state['energy'] = float(v)
    update_status()

def update_status():
    energy_kj = state['energy'] * ENERGY_KJ_PER_UNIT
    emit_rate_per_frame = int(BASE_EMIT_RATE * state['energy'])
    emit_rate_per_sec = emit_rate_per_frame / DT
    active_count = int(alive.sum())
    avg_speed = 0.0
    idxs = np.where(alive)[0][:state['active']]
    if idxs.size > 0:
        speeds = np.linalg.norm(vel[idxs, :], axis=1)
        avg_speed = float(np.mean(speeds))
    approx_buoy = BUOY_COEFF * (energy_kj / E_REF_KJ)
    status.text = f"\n Active: {state['active']}  Energy: {energy_kj:.1f} kJ/particle  Emit: {emit_rate_per_sec:.0f} part/s  Avg speed: {avg_speed:.2f} m/s \n" 
    # Buoyancy: {approx_buoy:.2f} m/s^2\n"

def toggle_pause(b):
    state['paused'] = not state['paused']
    b.text = "Resume" if state['paused'] else "Pause"

def toggle_entropy(b):
    state['entropy_visible'] = not state['entropy_visible']
    b.text = "Hide Entropy" if state['entropy_visible'] else "Show Entropy"
    if not state['entropy_visible']:
        for c in entropy_cubes:
            c.visible = False
    update_status()

wtext(text="  Particle count: ")
count_slider = slider(bind=lambda s: set_count(s.value), min=10, max=MAX_PARTICLES, value=INITIAL_ACTIVE, length=320)
wtext(text="   ")
wtext(text="Energy: ")
energy_slider = slider(bind=lambda s: set_energy(s.value), min=0.2, max=4.0, value=1.0, length=320)
status = wtext(text=f"\n Active: {state['active']}  Energy: {state['energy']*ENERGY_KJ_PER_UNIT:.1f} kJ/particle\n")
button(bind=toggle_pause, text="Pause")
button(bind=toggle_entropy, text="Show Entropy")

fire_core_radius = 0.9
stone_inner_limit = stone_ring_radius - 0.12

def spawn_particle(i, energy):
    sigma = 0.18 / max(0.18, energy * 0.45)
    while True:
        x = np.random.normal(0.0, sigma)
        z = np.random.normal(0.0, sigma)
        r = math.sqrt(x * x + z * z)
        if r <= stone_inner_limit:
            break
    y = abs(np.random.normal(0.02, 0.02))
    pos[i, :] = (x, y, z)
    energy_kj = energy * ENERGY_KJ_PER_UNIT
    up_speed = 1.8 * (energy_kj / E_REF_KJ) * np.random.uniform(0.7, 1.6)
    lateral = 0.5 * np.random.normal(0.0, 0.33) * (energy_kj / E_REF_KJ)
    vx = lateral * np.random.uniform(-1, 1)
    vz = lateral * np.random.uniform(-1, 1)
    vy = up_speed
    vel[i, :] = (vx, vy, vz)
    life[i] = np.random.uniform(0.9, 1.9) * (1.0 + 0.7 * energy)
    alive[i] = True
    spheres[i].pos = vec(float(x), float(y), float(z))
    spheres[i].visible = True
    spheres[i].radius = 0.06 * (0.9 + 0.7 * energy)

def radial_color(x, y, z, l):
    r = math.sqrt(x * x + z * z)
    rn = min(1.0, r / (fire_core_radius + 0.2))
    if rn < 0.4:
        t = rn / 0.4
        c = np.array([1.0, 0.5 * t, 0.05 * (1 - t)])
    elif rn < 0.8:
        t = (rn - 0.4) / 0.4
        c = np.array([1.0, 0.5 + 0.5 * t, 0.05 - 0.02 * t])
    else:
        t = (rn - 0.8) / 0.2
        c = np.array([1.0, 1.0 - 0.6 * t, 0.0 + 0.2 * t])
    height_factor = np.clip(1.0 - (y / 2.2), 0.0, 1.0)
    life_factor = np.clip(l / 2.0, 0.0, 1.0)
    bright = 0.4 + 0.6 * height_factor * life_factor
    c = np.clip(c * bright + (1 - life_factor) * 0.18, 0.0, 1.0)
    return vec(float(c[0]), float(c[1]), float(c[2]))

def entropy_value_from_ke(ke, scale=0.06):
    return math.log1p(ke / scale)

def color_from_norm(v):
    v = max(0.0, min(1.0, v))
    if v < 0.33:
        t = v / 0.33
        return vec(0.0 + t * 0.0, 0.0 + t * 0.7, 1.0 - t * 1.0)
    elif v < 0.66:
        t = (v - 0.33) / 0.33
        return vec(0.0 + t * 1.0, 0.7 + t * 0.3, 0.0)
    else:
        t = (v - 0.66) / 0.34
        return vec(1.0, 1.0 - 0.7 * t, 0.0 + 0.6 * t)

for i in range(state['active']):
    spawn_particle(i, state['energy'])

last_time = time.time()

while True:
    rate(1 / DT)
    now = time.time()
    elapsed = now - last_time
    last_time = now
    if state['paused']:
        continue
    emit_rate = int(BASE_EMIT_RATE * state['energy'])
    alive_count = int(alive.sum())
    to_emit = max(0, min(emit_rate, state['active'] - alive_count))
    if to_emit > 0:
        free_idx = np.where(~alive)[0]
        take = min(len(free_idx), to_emit)
        for j in free_idx[:take]:
            spawn_particle(j, state['energy'])
    energy_kj_array = state['energy'] * ENERGY_KJ_PER_UNIT
    buoyant_base = BUOY_COEFF * (energy_kj_array / E_REF_KJ)
    buoyant = buoyant_base * np.exp(-pos[:, 1] / 2.0)
    turb = TURB_SCALE * (energy_kj_array / E_REF_KJ) * np.exp(-pos[:, 1] / 1.2)
    acc = np.zeros_like(pos)
    acc[:, 0] = np.random.normal(0, 1.0, size=MAX_PARTICLES) * turb
    acc[:, 2] = np.random.normal(0, 1.0, size=MAX_PARTICLES) * turb
    acc[:, 1] = buoyant
    acc += -DRAG_COEFF * vel
    pos_prev = pos.copy()
    vel += acc * DT
    radial = np.sqrt(pos[:, 0] * pos[:, 0] + pos[:, 2] * pos[:, 2])
    outside = radial > stone_inner_limit
    if outside.any():
        idxs = np.where(outside & alive)[0]
        for idx in idxs:
            x, y, z = pos[idx]
            r = math.sqrt(x * x + z * z)
            if r == 0:
                dirx, dirz = 0.0, 0.0
            else:
                dirx, dirz = x / r, z / r
            new_r = stone_inner_limit - 0.02
            pos[idx, 0] = new_r * dirx
            pos[idx, 2] = new_r * dirz
            vel[idx, 0] *= -0.3
            vel[idx, 2] *= -0.3
    pos += vel * DT
    pos[:, 1] = np.maximum(pos[:, 1], 0.0)
    life[alive] -= DT
    died = (life <= 0) & alive
    if died.any():
        for idx in np.where(died)[0]:
            alive[idx] = False
            spheres[idx].visible = False
            entropy_cubes[idx].visible = False
    out_of_bounds = (pos[:, 1] > 6.5) | (np.abs(pos[:, 0]) > 5.0) | (np.abs(pos[:, 2]) > 5.0)
    if out_of_bounds.any():
        for idx in np.where(out_of_bounds & alive)[0]:
            alive[idx] = False
            spheres[idx].visible = False
            entropy_cubes[idx].visible = False
    active_idx = np.where(alive)[0][:state['active']]
    max_entropy_seen = 1e-9
    ke_vals = np.zeros_like(life)
    for i in active_idx:
        vx, vy, vz = vel[i]
        ke = 0.5 * (vx * vx + vy * vy + vz * vz)
        ke_vals[i] = ke
        if ke > max_entropy_seen:
            max_entropy_seen = ke
    norm_scale = max_entropy_seen if (state['entropy_visible'] and max_entropy_seen > 0) else 1.0
    for i in active_idx:
        x, y, z = pos[i]
        radial_dist = math.sqrt(x * x + z * z)
        falloff = np.clip(1.0 - (radial_dist / (fire_core_radius + 0.6)), 0.0, 1.0)
        height_bias = np.clip(1.0 - (y / 2.2), 0.0, 1.0)
        flameshape = 0.6 + 0.8 * falloff * height_bias * (0.8 + 0.2 * state['energy'])
        spheres[i].pos = vec(float(x), float(y), float(z))
        spheres[i].color = radial_color(x, y, z, life[i])
        spheres[i].opacity = max(0.10, min(1.0, life[i] / 1.8))
        spheres[i].radius = 0.04 * flameshape * (0.9 + 0.6 * state['energy'])
        if state['entropy_visible']:
            ke = ke_vals[i]
            s = entropy_value_from_ke(ke, scale=0.06)
            s_norm = s / (math.log1p(norm_scale / 0.06) + 1e-9)
            color_e = color_from_norm(s_norm)
            size_e = 0.04 + 0.18 * min(1.0, s_norm * 1.6)
            entropy_cubes[i].pos = vec(float(x), float(y + 0.12 + size_e / 2), float(z))
            entropy_cubes[i].size = vec(size_e, size_e, size_e)
            entropy_cubes[i].color = color_e
            entropy_cubes[i].opacity = 0.28
            entropy_cubes[i].visible = True
        else:
            entropy_cubes[i].visible = False
    update_status()

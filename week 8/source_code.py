from controller import Robot

# Konfigurasi dasar
TIME_STEP = 64
MAX_SPEED = 6.28

# Inisialisasi robot
robot = Robot()

# Inisialisasi sensor jarak inframerah (ps0 hingga ps7)
prox_sensor = []
sensor_names = ["ps0", "ps1", "ps2", "ps3", "ps4", "ps5", "ps6", "ps7"]

for name in sensor_names:
    sensor = robot.getDevice(name)
    sensor.enable(TIME_STEP)
    prox_sensor.append(sensor)

# Inisialisasi motor
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# Threshold jarak sensor
SIDE_THRESHOLD = 150.0  # Jarak untuk mendeteksi dinding di samping kiri
FRONT_THRESHOLD = 200.0  # Jarak untuk mendeteksi dinding di depan

# Loop utama
while robot.step(TIME_STEP) != -1:
    # Membaca nilai sensor jarak
    left_side = prox_sensor[7].getValue()  # Sensor samping kiri (ps7)
    front_left = prox_sensor[6].getValue()  # Sensor depan kiri (ps6)

    # Mengatur kecepatan dasar
    left_speed = 0.5 * MAX_SPEED
    right_speed = 0.5 * MAX_SPEED
    
    # Logika kontrol sederhana mengikuti dinding
    if front_left > FRONT_THRESHOLD:  # Jika ada dinding di depan
        # Berbelok kanan untuk menghindari tabrakan
        left_speed = 0.5 * MAX_SPEED
        right_speed = -0.2 * MAX_SPEED
    elif left_side < SIDE_THRESHOLD:  # Jika tidak ada dinding di samping kiri
        # Berbelok kiri sedikit untuk mendekati dinding
        left_speed = 0.4 * MAX_SPEED
        right_speed = 0.8 * MAX_SPEED
    else:
        # Berjalan lurus mengikuti dinding
        left_speed = 0.5 * MAX_SPEED
        right_speed = 0.5 * MAX_SPEED

    # Mengatur kecepatan motor
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)

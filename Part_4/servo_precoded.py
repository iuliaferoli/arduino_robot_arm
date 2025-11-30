from machine import Pin, PWM, ADC #import libraries for Pin, PWM, ADC
from time import sleep
    
    
servoPin0 = PWM(Pin(14)) # rotating base
servoPin0.freq(50)
servoPin1 = PWM(Pin(17)) # first joiny
servoPin1.freq(50)
servoPin2 = PWM(Pin(16)) # second joint
servoPin2.freq(50)       
servoPin3 = PWM(Pin(15)) #3rd joint
servoPin3.freq(50)
servoPin4 = PWM(Pin(18)) # claw
servoPin4.freq(50)



servos = [servoPin0, servoPin1, servoPin2, servoPin3]

def interval_mapping(x, in_min, in_max, out_min, out_max):
    """
    Maps a value from one range to another.
    This function is useful for converting servo angle to pulse width.
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def servo_write(pin, angle):
    """
    Moves the servo to a specific angle.
    The angle is converted to a suitable duty cycle for the PWM signal.
    """
    pulse_width = interval_mapping(
        angle, 0, 180, 0.5, 2.5
    )  # Map angle to pulse width in ms
    duty = int(
        interval_mapping(pulse_width, 0, 20, 0, 65535)
    )  # Map pulse width to duty cycle
    pin.duty_u16(duty)  # Set PWM duty cycle

def smooth_move(pin, start_angle, end_angle, duration=1, steps=20):
    """
    Smoothly moves a servo from start_angle to end_angle over specified duration.
    
    Args:
        pin: PWM pin object to control
        start_angle: Starting angle (0-180)
        end_angle: Target angle (0-180)
        duration: Time in seconds for the movement (can be float)
        steps: Number of intermediate steps (more steps = smoother)
    """
    step_delay = duration / steps
    angle_step = (end_angle - start_angle) / steps
    
    for i in range(steps + 1):
        current_angle = start_angle + (angle_step * i)
        servo_write(pin, current_angle)
        if i < steps:  # Don't sleep after the last step
            sleep(step_delay)

def smooth_move_multiple(pins_angles, duration=1, steps=20):
    """
    Smoothly moves multiple servos simultaneously to their target angles.
    
    Args:
        pins_angles: List of tuples [(pin, start_angle, end_angle), ...]
        duration: Time in seconds for the movement (can be float)
        steps: Number of intermediate steps (more steps = smoother)
    """
    step_delay = duration / steps
    
    for i in range(steps + 1):
        for pin, start_angle, end_angle in pins_angles:
            angle_step = (end_angle - start_angle) / steps
            current_angle = start_angle + (angle_step * i)
            servo_write(pin, current_angle)
        if i < steps:  # Don't sleep after the last step
            sleep(step_delay)

def straight_up():
    servo_write(servoPin1, 110)
    servo_write(servoPin2, 100)
    servo_write(servoPin3, 80)
    

def down():
    servo_write(servoPin1, 60)
    servo_write(servoPin2, 40)
    servo_write(servoPin3, 30)

def pick_and_place(position):
    """
    Pick up an item from specified position and place it at the opposite side.
    
    Args:
        position: "left" or "right" - where the item is located
    """
    if position == "left":
        pick_angle = 30  # Left side
        place_angle = 150  # Right side
    elif position == "right":
        pick_angle = 150  # Right side
        place_angle = 30  # Left side
    else:
        print("Invalid position. Use 'left' or 'right'")
        return
    
    # Move to pick position
    smooth_move(servoPin0, 90, pick_angle, duration=0.8, steps=40)
    sleep(0.3)
    smooth_move_multiple([(servoPin1, 110, 110), (servoPin2, 100, 100), (servoPin3, 80, 80)], duration=0.4, steps=20)
    sleep(0.3)
    
    # Lower arm to pick
    smooth_move_multiple([(servoPin1, 110, 60), (servoPin2, 100, 40), (servoPin3, 80, 30)], duration=0.8, steps=40)
    sleep(0.3)
    
    # Grab
    smooth_move(servoPin4, 90, 45, duration=0.5, steps=25)
    sleep(0.3)
    
    # Raise arm
    smooth_move_multiple([(servoPin1, 60, 110), (servoPin2, 40, 100), (servoPin3, 30, 80)], duration=0.8, steps=40)
    sleep(0.3)
    
    # Rotate to place position
    smooth_move(servoPin0, pick_angle, place_angle, duration=1.0, steps=50)
    sleep(0.3)
    
    # Lower arm to place
    smooth_move_multiple([(servoPin1, 110, 60), (servoPin2, 100, 40), (servoPin3, 80, 30)], duration=0.8, steps=40)
    sleep(0.3)
    
    # Release
    smooth_move(servoPin4, 45, 90, duration=0.5, steps=25)
    sleep(0.3)
    
    # Raise arm
    smooth_move_multiple([(servoPin1, 60, 110), (servoPin2, 40, 100), (servoPin3, 30, 80)], duration=0.8, steps=40)
    sleep(0.3)
    
    # Return to home
    smooth_move(servoPin0, place_angle, 90, duration=0.8, steps=40)

def wave(waves=3):
    """
    Makes the arm wave back and forth with wrist rotation.
    
    Args:
        waves: Number of waves to perform (default 3)
    """
    # Move arm to waving position (straight out to the side, slightly raised)
    smooth_move_multiple([(servoPin1, 110, 90), (servoPin2, 100, 110), (servoPin3, 80, 70)], duration=0.6, steps=30)
    sleep(0.2)
    
    # Wave back and forth with wrist rotation
    for i in range(waves):
        # Wave left with wrist up
        smooth_move_multiple([(servoPin0, 90, 60), (servoPin3, 70, 110)], duration=0.4, steps=20)
        sleep(0.1)
        
        # Wave right with wrist down
        smooth_move_multiple([(servoPin0, 60, 120), (servoPin3, 110, 30)], duration=0.4, steps=20)
        sleep(0.1)
    
    # Return to center with wrist neutral
    smooth_move_multiple([(servoPin0, 120, 90), (servoPin3, 30, 70)], duration=0.4, steps=20)
    sleep(0.2)
    
    # Return arm to rest position
    smooth_move_multiple([(servoPin1, 90, 110), (servoPin2, 110, 100), (servoPin3, 70, 80)], duration=0.6, steps=30)

def nod_yes(nods=2):
    """
    Makes the arm nod "yes" by moving up and down.
    
    Args:
        nods: Number of nods to perform (default 2)
    """
    # Move arm to neutral position
    smooth_move_multiple([(servoPin1, 110, 100), (servoPin2, 100, 90), (servoPin3, 80, 80)], duration=0.4, steps=20)
    sleep(0.2)
    
    # Nod up and down
    for i in range(nods):
        # Nod forward (down)
        smooth_move(servoPin2, 90, 120, duration=0.3, steps=15)
        sleep(0.1)
        
        # Nod back (up)
        smooth_move(servoPin2, 120, 60, duration=0.3, steps=15)
        sleep(0.1)
    
    # Return to neutral
    smooth_move(servoPin2, 60, 90, duration=0.3, steps=15)
    sleep(0.2)
    
    # Return arm to rest position
    smooth_move_multiple([(servoPin1, 100, 110), (servoPin2, 90, 100), (servoPin3, 80, 80)], duration=0.4, steps=20)


def _parse_yes_no(text):
    """Return 'yes' / 'no' / None for unclear input."""
    if not text:
        return None
    t = text.strip().lower()
    yes = ("yes", "y", "yeah", "yep", "true", "1", "sure")
    no = ("no", "n", "nope", "false", "0", "nah")
    for w in yes:
        if w == t or t.startswith(w + " ") or (w in t and len(t) <= 5):
            return "yes"
    for w in no:
        if w == t or t.startswith(w + " ") or (w in t and len(t) <= 5):
            return "no"
    return None


def ask_and_get(question):
    """Prompt the user (console) and return parsed yes/no/None."""
    try:
        resp = input(question + " (yes/no): ")
    except Exception:
        # No interactive input available
        print("Interactive input not available; defaulting to 'no'.")
        return "no"
    return _parse_yes_no(resp)


def run_scenarios(side):
    """Scenario loop: wave, prompt user for tissue side (left/right), then pick it up."""
    # 1) Wave
    print("Scenario: wave now.")
    wave(3)
    sleep(0.5)


    # 3) Pick up from the specified side
    if side in ("left", "l"):
        print("Picking up tissue from the left.")
        pick_and_place("left")
    elif side in ("right", "r"):
        print("Picking up tissue from the right.")
        pick_and_place("right")
    else:
        print("Invalid side '%s'; defaulting to left." % side)
        pick_and_place("left")





def shake_no(shakes=3):
    """
    Makes the arm shake "no" by moving left and right.
    
    Args:
        shakes: Number of shakes to perform (default 3)
    """
    # Move arm to neutral position
    smooth_move_multiple([(servoPin1, 110, 100), (servoPin2, 100, 90), (servoPin3, 80, 80)], duration=0.4, steps=20)
    sleep(0.2)
    
    # Shake left and right
    for i in range(shakes):
        # Shake left
        smooth_move(servoPin0, 90, 60, duration=0.3, steps=15)
        sleep(0.1)
        
        # Shake right
        smooth_move(servoPin0, 60, 120, duration=0.3, steps=15)
        sleep(0.1)
    
    # Return to center
    smooth_move(servoPin0, 120, 90, duration=0.3, steps=15)
    sleep(0.2)
    
    # Return arm to rest position
    smooth_move_multiple([(servoPin1, 100, 110), (servoPin2, 90, 100), (servoPin3, 80, 80)], duration=0.4, steps=20)


run_scenarios("left")
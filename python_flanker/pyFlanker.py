import pygame
import time
import random
import os
import serial
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from unittest.mock import MagicMock

'''
# Mock Serial object
class MockSerial(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.port = 'COM99'  # Simulate port number
        self.baudrate = 9600
        self.timeout = 0.1

    def open(self):
        pass

    def close(self):
        pass

    def write(self, data):
        print(f"Mock Serial Write: {data}")

    def read(self, size):
        return b'Mock Serial Data'
'''


# Replace 'COMX' with the actual serial port your Arduino is connected to
ser = serial.Serial('COM5', 9600, timeout=0.1) 
#ser = serial.Serial = MockSerial

# Set the position of the window
#x, y = 4000, 200
x, y = 0, 0
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"

# Initialize Pygame
pygame.init()

# Set up the display
#screen = pygame.display.set_mode((800, 800))
#screen = pygame.display.set_mode((5120, 1440))
screen = pygame.display.set_mode((5120, 1440))
pygame.display.set_caption('Arrow Key Response Test')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define the font
font = pygame.font.Font(None, 200)

response_directions = []
response_times = []
response_correctness = []
response_question = []

# Define the text list and corresponding correct responses
text_list = [(">>>>>", "right"), ("<<><<", "right"), (">><>>", "left"), ("<<<<<", "left"),]
total_texts = 5
display_time = 0.5  # Time in seconds to show question
response_window = 2  # Time in seconds to allow responses

# Function to display text
def display_text(text, colorMode):
    
    if colorMode == "dark":
        screen.fill(BLACK)
        text_surface = font.render(text, True, WHITE)
    else:
        screen.fill(WHITE)
        text_surface = font.render(text, True, BLACK)
        
        
    # Get the rectangle of the text surface
    text_rect = text_surface.get_rect()

    # Center the text rectangle on the screen
    text_rect.center = screen.get_rect().center
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

def wrap_text(text, font, max_width):
    words = text.split()
    wrapped_lines = []
    current_line = ''

    for word in words:
        test_line = current_line + ' ' + word if current_line != '' else word
        test_width, _ = font.size(test_line)
        if test_width <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word

    if current_line:
        wrapped_lines.append(current_line)

    return wrapped_lines

# Function to wait for a key press and check correctness
def wait_for_key(correct_key):
    start_time = time.time()
    question_visible = True;
    
    while time.time() - start_time < response_window:
        
        if time.time() - start_time > display_time and question_visible == True:
            display_text("", "dark")
            question_visible = False
        
        handle_events()  # Check for events after each text display and key waiting
        try:
            line = ser.readline()  # Read a line from the serial port with timeout
            if line:
                directionAsString = line.decode('utf-8').strip()  # Decode the bytes to string
                response_directions.append(directionAsString)
                
                line = ser.readline()  # Read the next line for time
                if line:
                    time_as_string = line.decode('utf-8').strip()  # Decode the bytes to string
                    #response_times.append(timeAsString)
                    
                    # Convert microseconds to milliseconds
                    microseconds = int(time_as_string)  # Assuming time_as_string is a string representing microseconds
                    milliseconds = microseconds / 1000  # Convert microseconds to milliseconds
                    
                    response_times.append(float(milliseconds))  # Store time as float
                
                response_correctness.append(directionAsString == correct_key)
                return directionAsString == correct_key
            time.sleep(0.1)  # Add a small delay to prevent high CPU usage
        except serial.SerialTimeoutException:
            # Handle timeout case if needed
            pass
            
    response_directions.append("no response")
    #response_times.append(int(999999))
    response_correctness.append(False)
    return False
    
def wait_for_time(wait_time):
    start_time = time.time()
    while time.time() - start_time < wait_time:
        handle_events()  # Check for events after each text display and key waiting
        pass  # Do nothing, just wait
    
    return True  # Return True after waiting

# Function to handle pygame events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            ser.close()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                ser.close()
                exit()

def remove_outliers(data):
    if len(data) < 4:
        return data
    
    data.sort()
    q1, q3 = data[len(data)//4], data[3*len(data)//4]
    iqr = q3 - q1
    lower_bound = q1 - 5.5 * iqr
    upper_bound = q3 + 5.5 * iqr
    
    return [x for x in data if lower_bound <= x <= upper_bound]

def convert_to_floats(mixed_list):
    return [float(item) if isinstance(item, str) else item for item in mixed_list if str(item).replace('.', '').isdigit()]


# Main game loop
def main():
    global response_times, response_directions, response_correctness, response_question

    
    correct_responses = 0
    display_text("Please respond as fast and accurately as possible.", "dark")
    wait_for_time(5)
    

    for _ in range(total_texts):
        text, correct_key = random.choice(text_list)
        response_question.append(text)
        display_text("+", "light")
        random_number = random.uniform(1, 2)
        wait_for_time(random_number)
        display_text(text, "dark")
        correct = wait_for_key(correct_key)
        if correct:
            correct_responses += 1
            display_text("Correct", "dark")
            wait_for_time(0.5)
        else:
            display_text("Incorrect", "dark")
            wait_for_time(0.5)

        handle_events()  # Check for events after each text display and key waiting

        # Clear the screen for a moment
        #screen.fill(BLACK)
        #pygame.display.flip()
        #time.sleep(0.5)

    # Display the result
    screen.fill(BLACK)
    result_text = f"Correct responses: {correct_responses}/{total_texts}"
    result_surface = font.render(result_text, True, WHITE)
    
    # Get the rectangle of the text surface
    result_rect = result_surface.get_rect()

    # Center the text rectangle on the screen
    result_rect.center = screen.get_rect().center
    
    
    screen.blit(result_surface, result_rect)
    pygame.display.flip()

    # Wait for a few seconds before closing
    time.sleep(3)

    pygame.quit()
    
    # Close the serial port when done
    ser.close()
    
    
    
    response_times = convert_to_floats(response_times)
    #response_times = remove_outliers(response_times)
    
    # Assuming response_times is your data array
    min_time = np.min(response_times)
    max_time = np.max(response_times)

    # Create more appropriate bins
    bins = np.linspace(min_time, max_time, 20)  # 20 evenly spaced bins

    plt.figure(figsize=(10, 6))
    plt.hist(response_times, bins=bins, edgecolor='black')
    plt.xlabel('Response Time (ms)')
    plt.ylabel('Frequency')
    plt.title('Histogram of Response Times')
    plt.grid(True)

    # Optional: Use log scale if data range is very wide
    # plt.xscale('log')

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.savefig(f'response_times_histogram_{current_datetime}.png')

    
    print(response_question)
    print(response_directions)
    print(response_correctness)
    print(response_times)
    
    # Calculate the sum of all elements in the list
    total_sum = sum(response_times)

    # Calculate the average
    if len(response_times) > 0:
        average = total_sum / len(response_times)
    else:
        average = 0  # or handle this case as per your requirements
    print("Average response time:", average)

    # Count the number of True values
    true_count = sum(response_correctness)

    # Calculate the percentage of True values
    percentage_true = (true_count / len(response_correctness)) * 100
    print(f"Percentage of correct reponses: {percentage_true}%")


if __name__ == "__main__":
    main()

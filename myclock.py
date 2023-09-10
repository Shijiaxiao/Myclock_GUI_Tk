import sys
import os
import tkinter as tk
import time
import threading
import pygame



def get_audio_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "rings", filename)
    else:
        return os.path.join("rings", filename)



class MYCLOCK:
    
    
    ''' INITIALIZATION '''
    
    def __init__(self):
        
        ''' Tkinter Window '''
        self.root = tk.Tk()
        self.root.geometry("+500+280")
        
        ''' Content Frame '''
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack()
        self.content_frame_init()
        
        ''' Button Frame '''
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()
        self.button_frame_init()

        ''' Ring Window '''
        self.ring_window = tk.Toplevel(self.root)
        self.ring_window.withdraw()
        self.ring_window.geometry("+535+100")
        self.ring_window_init()
        
        ''' Ring Thread '''
        self.ring_thread_init()
        
    def content_frame_init(self):
        self.clock_init()
        self.stopwatch_init()
        self.timer_init()
        self.alarm_init()
    
    def clock_init(self):
        
        # Font:
        self.clock_label_font = ('Pacifico', 26, 'bold')
        
        # Color:
        self.clock_label_fg = (0, 0, 0)
        self.clock_label_fg_hex = "#{:02X}{:02X}{:02X}".format(*self.clock_label_fg)
        
        # Label:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label = tk.Label(self.content_frame, text = "{}".format(current_time), font = self.clock_label_font, fg = self.clock_label_fg_hex)
        
        # Flag:
        self.clock_update = False
        
    def stopwatch_init(self):
        
        # Fonts:
        self.stopwatch_label_font = ('Pacifico', 26, 'bold')
        self.stopwatch_button_font = ('Pacifico', 22, 'bold')
        
        # Colors:
        self.stopwatch_label_fg = (255, 206, 30)
        self.stopwatch_toggle_button_start = (128, 215, 88)
        self.stopwatch_toggle_button_stop = (180, 0, 0)
        self.stopwatch_reset_button_grey = (120, 120, 120)
        self.stopwatch_reset_button_black = (0, 0, 0)
        self.stopwatch_label_fg_hex = "#{:02X}{:02X}{:02X}".format(*self.stopwatch_label_fg)
        self.stopwatch_toggle_button_start_hex = "#{:02X}{:02X}{:02X}".format(*self.stopwatch_toggle_button_start)
        self.stopwatch_toggle_button_stop_hex = "#{:02X}{:02X}{:02X}".format(*self.stopwatch_toggle_button_stop)
        self.stopwatch_reset_button_grey_hex = "#{:02X}{:02X}{:02X}".format(*self.stopwatch_reset_button_grey)
        self.stopwatch_reset_button_black_hex = "#{:02X}{:02X}{:02X}".format(*self.stopwatch_reset_button_black)
        
        # Label:
        self.stopwatch_label = tk.Label(self.content_frame, text = "00:00:00.00", font = self.stopwatch_label_font, fg = self.stopwatch_label_fg_hex)
        
        # Buttons:
        self.stopwatch_toggle_button = tk.Button(self.content_frame, text = "Start", font = self.stopwatch_button_font, fg = self.stopwatch_toggle_button_start_hex, command = self.toggle_stopwatch)
        self.stopwatch_reset_button = tk.Button(self.content_frame, text = "Reset", font = self.stopwatch_button_font, fg = self.stopwatch_reset_button_grey_hex, command = self.reset_stopwatch)
        
        # Flags:
        self.stopwatch_active = False
        self.stopwatch_started = False
        
        # Data:
        self.stopwatch_show_time = 0
        self.stopwatch_start_time = 0
        self.stopwatch_stop_time = 0
        self.stopwatch_last_stop_time = 0
        
    def timer_init(self):
        
        # Fonts:
        self.timer_label_font = ('Pacifico', 26, 'bold')
        self.timer_button_font = ('Pacifico', 22, 'bold')
        
        # Colors:
        self.timer_label_fg = (255, 206, 30)
        self.timer_toggle_button_start = (128, 215, 88)
        self.timer_toggle_button_stop = (180, 0, 0)
        self.timer_reset_button_grey = (120, 120, 120)
        self.timer_reset_button_black = (0, 0, 0)
        self.timer_label_fg_hex = "#{:02X}{:02X}{:02X}".format(*self.timer_label_fg)
        self.timer_toggle_button_start_hex = "#{:02X}{:02X}{:02X}".format(*self.timer_toggle_button_start)
        self.timer_toggle_button_stop_hex = "#{:02X}{:02X}{:02X}".format(*self.timer_toggle_button_stop)
        self.timer_reset_button_grey_hex = "#{:02X}{:02X}{:02X}".format(*self.timer_reset_button_grey)
        self.timer_reset_button_black_hex = "#{:02X}{:02X}{:02X}".format(*self.timer_reset_button_black)
        
        # Label:
        self.timer_label = tk.Label(self.content_frame, text = "00:00:00.00", font = self.timer_label_font, fg = self.timer_label_fg_hex)
        
        # Buttons:
        self.timer_toggle_button = tk.Button(self.content_frame, text = "Start", font = self.timer_button_font, fg = self.timer_toggle_button_start_hex, command = self.toggle_timer)
        self.timer_reset_button = tk.Button(self.content_frame, text = "Reset", font = self.timer_button_font, fg = self.timer_reset_button_grey_hex, command = self.reset_timer)
        
        # Sliders:
        self.timer_hour_slider = tk.Scale(self.content_frame, from_ = 0, to = 99, orient = "horizontal", command = self.apply_timer)
        self.timer_minute_slider = tk.Scale(self.content_frame, from_ = 0, to = 59, orient = "horizontal", command = self.apply_timer)
        self.timer_second_slider = tk.Scale(self.content_frame, from_ = 0, to = 59, orient = "horizontal", command = self.apply_timer)
        self.timer_millisecond_slider = tk.Scale(self.content_frame, from_ = 0, to = 99, orient = "horizontal", command = self.apply_timer)
        self.timer_hour_slider.set(0) 
        self.timer_minute_slider.set(0)
        self.timer_second_slider.set(0)
        self.timer_millisecond_slider.set(0)
        
        # Flags:
        self.timer_active = False
        self.timer_started = False
        
        # Data:
        self.timer_lastone = 0
        self.timer_seconds = 0
        self.timer_show_time = 0
        self.timer_start_time = 0
        self.timer_stop_time = 0
        
    def alarm_init(self):
        
        # Fonts:
        self.alarm_label_font = ('Pacifico', 28, 'bold')
        self.alarm_button_font = ('Pacifico', 22, 'bold')
        
        # Colors:
        self.alarm_label_fg = (0, 0, 0)
        self.alarm_toggle_button_set = (128, 215, 88)
        self.alarm_toggle_button_cancel = (180, 0, 0)
        self.alarm_label_fg_hex = "#{:02X}{:02X}{:02X}".format(*self.alarm_label_fg)
        self.alarm_toggle_button_set_hex = "#{:02X}{:02X}{:02X}".format(*self.alarm_toggle_button_set)
        self.alarm_toggle_button_cancel_hex = "#{:02X}{:02X}{:02X}".format(*self.alarm_toggle_button_cancel)
        
        # Sliders:
        self.alarm_hour_slider = tk.Scale(self.content_frame, from_ = 0, to = 23, orient = "horizontal", command = self.apply_alarm)
        self.alarm_minute_slider = tk.Scale(self.content_frame, from_ = 0, to = 59, orient = "horizontal", command = self.apply_alarm)
        self.alarm_second_slider = tk.Scale(self.content_frame, from_ = 0, to = 59, orient = "horizontal", command = self.apply_alarm)
        self.alarm_hour_slider.set(0) 
        self.alarm_minute_slider.set(0)
        self.alarm_second_slider.set(0)
        
        # Label:
        self.alarm_label = tk.Label(self.content_frame, text = "00:00:00", font = self.alarm_label_font, fg = self.alarm_label_fg_hex)
        
        # Button:
        self.alarm_toggle_button = tk.Button(self.content_frame, text = "Set", font = self.alarm_button_font, fg = self.alarm_toggle_button_set_hex, command = self.toggle_alarm)
        
        # Flag:
        self.alarm_set = False
        
        # Data:
        self.alarm_lastone = None
        self.alarm_hour = 0
        self.alarm_minute = 0
        self.alarm_second = 0
        
    def button_frame_init(self):
        
        # Font:
        self.button_font = ('Pacifico', 18, 'bold')
        
        # Colors:
        self.button_fg = (120, 205, 255)
        self.button_highlight_fg = (238, 130, 238)
        self.button_fg_hex = "#{:02X}{:02X}{:02X}".format(*self.button_fg)
        self.button_highlight_fg_hex = "#{:02X}{:02X}{:02X}".format(*self.button_highlight_fg)
        
        # Buttons:
        self.clock_button = tk.Button(self.button_frame, text = "Clock", font = self.button_font, fg = self.button_fg_hex, command = self.show_clock)
        self.stopwatch_button = tk.Button(self.button_frame, text = "Stopwatch", font = self.button_font, fg = self.button_fg_hex, command = self.show_stopwatch)
        self.timer_button = tk.Button(self.button_frame, text = "Timer", font = self.button_font, fg = self.button_fg_hex, command = self.show_timer)
        self.alarm_button = tk.Button(self.button_frame, text = "Alarm", font = self.button_font, fg = self.button_fg_hex, command = self.show_alarm)

        # Pack buttons:
        self.clock_button.pack(side = tk.LEFT)
        self.stopwatch_button.pack(side = tk.LEFT)
        self.timer_button.pack(side = tk.LEFT)
        self.alarm_button.pack(side = tk.LEFT)
    
    def ring_window_init(self):
        
        # Tag:
        self.ring_tag = None
        self.ring_window.title(self.ring_tag)
        
        # Fonts:
        self.ring_label_lastone_font = ('Pacifico', 26, 'bold')
        self.ring_label_font = ('Pacifico', 22, 'bold')
        
        # Colors:
        self.ring_label_lastone_fg = (0, 0, 0)
        self.ring_label_fg = (180, 0, 0)
        self.ring_label_lastone_fg_hex = "#{:02X}{:02X}{:02X}".format(*self.ring_label_lastone_fg)
        self.ring_label_fg_hex = "#{:02X}{:02X}{:02X}".format(*self.ring_label_fg)
        
        # Labels:
        self.ring_label_lastone = tk.Label(self.ring_window, text = None, font = self.ring_label_lastone_font, fg = self.ring_label_lastone_fg_hex)
        self.ring_label = tk.Label(self.ring_window, text = "Press the button to end {}.".format(self.ring_tag), font = self.ring_label_font, fg = self.ring_label_fg_hex)
        self.ring_label_lastone.pack()
        self.ring_label.pack()
        
        # Button:
        self.ring_button_font = ('Pacifico', 22, 'bold')
        self.ring_close_button = tk.Button(self.ring_window, text = "Close", font = self.ring_button_font, command = self.stop_ring)
        self.ring_close_button.pack()
        
    def ring_thread_init(self):
        
        # Player:
        pygame.mixer.init()
        
        # Ring path:
        self.timer_ring_path = get_audio_path("timer_ring.mp3")
        self.alarm_ring_path = get_audio_path("alarm_ring.mp3")
        
        # Thread safety:
        self.end_thread = False
        self.lock = threading.Lock()
        
        



    '''CLEAN CONTENT FRAME '''
    def clean_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()





    ''' CLOCK '''
    
    def show_clock(self):
        
        # Set title and buttons:
        self.root.title("CLOCK")
        self.clock_button.config(fg = self.button_highlight_fg_hex)
        self.stopwatch_button.config(fg = self.button_fg_hex)
        self.timer_button.config(fg = self.button_fg_hex)
        self.alarm_button.config(fg = self.button_fg_hex)
        
        # Update clock and clean content:
        self.clock_update = True
        self.clean_content_frame()
        
        # Pack label:
        self.clock_label.pack()
        
        # Start update clock:
        self.update_clock()
        
    def update_clock(self):
        if self.clock_update:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            self.clock_label.config(text = "{}".format(current_time))
            self.root.after(1000, self.update_clock)
    
    
    
    
    
    ''' STOPWATCH '''
    
    def show_stopwatch(self):
        
        # Set title and buttons:
        self.root.title("STOPWATCH")
        self.clock_button.config(fg = self.button_fg_hex)
        self.stopwatch_button.config(fg = self.button_highlight_fg_hex)
        self.timer_button.config(fg = self.button_fg_hex)
        self.alarm_button.config(fg = self.button_fg_hex)
        
        # Stop update clock and clean content:
        self.clock_update = False
        self.clean_content_frame()
        
        # Pack label:
        self.stopwatch_label.pack()

        # Pack buttons:
        self.stopwatch_toggle_button.pack()
        self.stopwatch_reset_button.pack()

        # Start update stopwatch:
        self.update_stopwatch()

    def toggle_stopwatch(self):
        
        # Start from 00:00:00, set to active and able to reset:
        if not self.stopwatch_active:
            self.stopwatch_active = True
            self.stopwatch_reset_button.config(fg = self.stopwatch_reset_button_black_hex)
        
        # Judge whether start or stop:
        if self.stopwatch_started:
            
            # Change to start:
            self.stopwatch_started = False
            self.stopwatch_toggle_button.config(text = "Start")
            self.stopwatch_toggle_button.config(fg = self.stopwatch_toggle_button_start_hex)
            
            # Record stop time, update last stop time:
            self.stopwatch_stop_time = time.time()
            self.stopwatch_last_stop_time += self.stopwatch_stop_time - self.stopwatch_start_time
            
        else:
            
            # Change to start:
            self.stopwatch_started = True
            self.stopwatch_toggle_button.config(text = "Stop")
            self.stopwatch_toggle_button.config(fg = self.stopwatch_toggle_button_stop_hex)
            
            # Record start time, start to show time:
            self.stopwatch_start_time = time.time()
            self.update_stopwatch()

    def update_stopwatch(self):
        
        if self.stopwatch_active:
            
            # Started:
            if self.stopwatch_started:
                self.stopwatch_show_time = self.stopwatch_last_stop_time + time.time() - self.stopwatch_start_time
                self.root.after(10, self.update_stopwatch)
            
            # Stopped:
            else:
                self.stopwatch_show_time = self.stopwatch_last_stop_time
                
            # Show time:
            self.stopwatch_show()
            
    def reset_stopwatch(self):
        
        # Inactive and stopped:
        self.stopwatch_active = False
        self.stopwatch_started = False
        
        # Set to initial situation and show time:
        self.stopwatch_show_time = 0
        self.stopwatch_start_time = 0
        self.stopwatch_stop_time = 0
        self.stopwatch_last_stop_time = 0
        self.stopwatch_show()
        
        # Start and set to active and able to reset:
        self.stopwatch_toggle_button.config(text = "Start")
        self.stopwatch_toggle_button.config(fg = self.stopwatch_toggle_button_start_hex)
        self.stopwatch_reset_button.config(fg = self.stopwatch_reset_button_grey_hex)

    def stopwatch_show(self):
        minutes, seconds = divmod(self.stopwatch_show_time, 60)
        hours, minutes = divmod(minutes, 60)
        self.stopwatch_label.config(text = "{:02}:{:02}:{:05.2f}".format(int(hours), int(minutes), seconds))





    ''' TIMER '''
    
    def show_timer(self):
        
        # Set title and buttons:
        self.root.title("TIMER")
        self.clock_button.config(fg = self.button_fg_hex)
        self.stopwatch_button.config(fg = self.button_fg_hex)
        self.timer_button.config(fg = self.button_highlight_fg_hex)
        self.alarm_button.config(fg = self.button_fg_hex)
        
        # Stop update clock and clean content:
        self.clock_update = False
        self.clean_content_frame()
        
        # Pack label:
        self.timer_label.pack()
        
        # Pack sliders:
        self.timer_hour_slider.pack()
        self.timer_minute_slider.pack()
        self.timer_second_slider.pack()
        self.timer_millisecond_slider.pack()
        
        # Pack buttons:
        self.timer_toggle_button.pack()
        self.timer_reset_button.pack()

        # Start update timer
        self.update_timer()

    def toggle_timer(self):
        
        # Start from set, set to active and able to reset:
        if not self.timer_active:
            self.timer_active = True
            self.timer_reset_button.config(fg = self.timer_reset_button_black_hex)
            
            # Record this timer:
            self.timer_lastone = self.timer_seconds
        
        # Judge whether start or stop:
        if self.timer_started:
            
            # Change to start:
            self.timer_started = False
            self.timer_toggle_button.config(text = "Start")
            self.timer_toggle_button.config(fg = self.timer_toggle_button_start_hex)
            
            # Record stop time, update timer seconds:
            self.timer_stop_time = time.time()
            self.timer_seconds -= self.timer_stop_time - self.timer_start_time
            
        else:
            
            # Change to stop:
            self.timer_started = True
            self.timer_toggle_button.config(text = "Stop")
            self.timer_toggle_button.config(fg = self.timer_toggle_button_stop_hex)
            
            # Record start time, start to show time:
            self.timer_start_time = time.time()
            self.update_timer()

    def update_timer(self):
        
        if self.timer_active:
            
             # Started:
            if self.timer_show_time > 0 and self.timer_started:
                self.timer_show_time = self.timer_seconds - (time.time() - self.timer_start_time)
                self.root.after(10, self.update_timer)
                
             # Stopped:
            elif self.timer_show_time > 0 and not self.timer_started:
                self.timer_show_time = self.timer_seconds
            
            # Finished:
            else:
                self.reset_timer()
                self.start_ring("TIMER")
                
            # Show time:
            self.timer_show()
        
    def reset_timer(self):
        
        # Inactive and stopped:
        self.timer_active = False
        self.timer_started = False
        
        # Set to initial situation and show time:
        self.timer_seconds = self.timer_hour_slider.get() * 3600 + self.timer_minute_slider.get() * 60 + self.timer_second_slider.get() + 0.01 * self.timer_millisecond_slider.get()
        self.timer_show_time = self.timer_seconds
        self.timer_start_time = 0
        self.timer_stop_time = 0
        self.timer_show()
        
        # Start and set to active and able to reset:
        self.timer_toggle_button.config(text = "Start")
        self.timer_toggle_button.config(fg = self.timer_toggle_button_start_hex)
        self.timer_reset_button.config(fg = self.timer_reset_button_grey_hex)

    def apply_timer(self, *args):
        if not self.timer_active:
            self.timer_seconds = self.timer_hour_slider.get() * 3600 + self.timer_minute_slider.get() * 60 + self.timer_second_slider.get() + 0.01 * self.timer_millisecond_slider.get()
            self.timer_show_time = self.timer_seconds
            self.timer_show()
            
    def timer_show(self):
        if self.timer_show_time < -0.001:
            self.timer_show_time = 0
        minutes, seconds = divmod(self.timer_show_time, 60)
        hours, minutes = divmod(minutes, 60)
        self.timer_label.config(text = "{:02}:{:02}:{:05.2f}".format(int(hours), int(minutes), seconds))
    
    def timer_show_last(self):
        minutes, seconds = divmod(self.timer_lastone, 60)
        hours, minutes = divmod(minutes, 60)
        return "{:02}:{:02}:{:05.2f}".format(int(hours), int(minutes), seconds)
    
    
    
    
    
    ''' ALARM '''
    
    def show_alarm(self):
        
        # Set title and buttons:
        self.root.title("ALARM")
        self.clock_button.config(fg = self.button_fg_hex)
        self.stopwatch_button.config(fg = self.button_fg_hex)
        self.timer_button.config(fg = self.button_fg_hex)
        self.alarm_button.config(fg = self.button_highlight_fg_hex)
        
        # Stop update clock and clean content:
        self.clock_update = False
        self.clean_content_frame()
        
        # Pack label:
        self.alarm_label.pack()
        
        # Pack sliders:
        self.alarm_hour_slider.pack()
        self.alarm_minute_slider.pack()
        self.alarm_second_slider.pack()
        
        # Pack button:
        self.alarm_toggle_button.pack()

        # Update label:
        self.update_alarm_label()
        
        # Check alarm:
        self.check_alarm()

    def toggle_alarm(self):
        
        # Judge whether start or stop:
        if self.alarm_set:
            
            # Set to set:
            self.alarm_set = False
            self.alarm_toggle_button.config(text = "Set")
            self.alarm_toggle_button.config(fg = self.alarm_toggle_button_set_hex)
            
            # Update alarm:
            self.alarm_hour = self.alarm_hour_slider.get()
            self.alarm_minute = self.alarm_minute_slider.get()
            self.alarm_second = self.alarm_second_slider.get()
            self.update_alarm_label()
            
        else:
            
            # Set to cancel and check alarm:
            self.alarm_set = True
            self.alarm_toggle_button.config(text = "Cancel")
            self.alarm_toggle_button.config(fg = self.alarm_toggle_button_cancel_hex)
            self.check_alarm()
            
            # Record this timer:
            self.alarm_lastone = "{:02}:{:02}:{:02}".format(self.alarm_hour, self.alarm_minute, self.alarm_second)

    def apply_alarm(self, *args):
        if not self.alarm_set:
            self.alarm_hour = self.alarm_hour_slider.get()
            self.alarm_minute = self.alarm_minute_slider.get()
            self.alarm_second = self.alarm_second_slider.get()
            self.update_alarm_label()
            
    def update_alarm_label(self):
        self.alarm_label.config(text = "{:02}:{:02}:{:02}".format(self.alarm_hour, self.alarm_minute, self.alarm_second))
    
    def check_alarm(self):
        
        if self.alarm_set:
            current_time = time.localtime()
            current_time_str = time.strftime("%H:%M:%S", current_time)
            
            # Reach set time:
            if current_time_str == self.alarm_lastone:
                
                # Set to set:
                self.alarm_set = False
                self.alarm_toggle_button.config(text = "Set")
                self.alarm_toggle_button.config(fg = self.alarm_toggle_button_set_hex)
                
                # # Reset and ring:
                self.alarm_hour = self.alarm_hour_slider.get()
                self.alarm_minute = self.alarm_minute_slider.get()
                self.alarm_second = self.alarm_second_slider.get()
                self.update_alarm_label()
                self.start_ring("ALARM")
            
            # Continue to check:
            else:
                self.root.after(500, self.check_alarm)
              
              
              
              
              
    ''' RING '''       
      
    def start_ring(self, tag):
        
        # Apply tag:
        self.ring_tag = tag
        
        with self.lock:
            
            # Hide toplevel:
            self.ring_window.withdraw()
            
            # Kill the last thread:
            self.end_thread = True
            
            # Show new window:
            self.ring_window.title(self.ring_tag)
            if self.ring_tag == "TIMER":
                self.ring_label_lastone.config(text = "{}".format(self.timer_show_last()))
            elif self.ring_tag == "ALARM":
                self.ring_label_lastone.config(text = self.alarm_lastone)
            else:
                print("[ERROR] Failed to set Label.")
            self.ring_label.config(text = "Press the button to end {}.".format(self.ring_tag))
            self.ring_window.deiconify()
            
        ring_thread = threading.Thread(target = self.play_ring, name = "{} RING THREAD".format(self.ring_tag), daemon = True)
        ring_thread.start()

    def play_ring(self):
        
        # Play music:
        with self.lock:
            self.end_thread = False
            if self.ring_tag == "TIMER":
                pygame.mixer.music.load(self.timer_ring_path)
            elif self.ring_tag == "ALARM":
                pygame.mixer.music.load(self.alarm_ring_path)
            else:
                print("[ERROR] Failed to load music.")
            pygame.mixer.music.play()
        
        while True:
            
            if self.end_thread:
                break
            
            # Play loop with lock:
            with self.lock:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
        
        # Stop play:
        with self.lock:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            
    def stop_ring(self):
        with self.lock:
            self.end_thread = True
            self.ring_window.withdraw()
    
        
        
        
            
    """ MAINLOOP """
    def run(self):
        self.show_clock()
        self.root.mainloop()
       
       
       
       
        
if __name__ == "__main__":
    app = MYCLOCK()
    app.run()

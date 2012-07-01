'''
'''

from gi.repository import Gtk, Gdk

def log(something):
    '''
    '''
    print something

class Handler:
    '''
    '''
    def on_py_factero_window_delete_event(self, *args, **kwds):
        '''
        '''
        Gtk.main_quit(*args)
    
    def on_copyhost_clicked(self, *args, **kwds):
        '''
        '''
        log(data.hostname)
        window.clipboard.set_text(data.hostname, -1)
        
    def on_copyuser_clicked(self, *args, **kwds):
        '''
        '''
        log(data.username)
        window.clipboard.set_text(data.username, -1)
        
    def on_copydist_clicked(self, *args, **kwds):
        '''
        '''
        log(data.distribution)
        window.clipboard.set_text(data.distribution, -1)
        
    def on_copylocal_clicked(self, *args, **kwds):
        '''
        '''
        log(data.local_ip)
        window.clipboard.set_text(data.local_ip, -1)
        
    def on_copyglobal_clicked(self, *args, **kwds):
        '''
        '''
        log(data.global_ip)
        window.clipboard.set_text(data.global_ip, -1)
        
    def on_copyuptime_clicked(self, *args, **kwds):
        '''
        '''
        log(data.uptime)
        window.clipboard.set_text(data.uptime, -1)
        
    
    
import os, pwd, socket, urllib2


class Data:
    '''
    '''
    def __init__(self):
        '''
        '''
        temp = os.uname()
        #Get hostname
        self.hostname = temp[1]

        #Get distribution
        self.distribution = ' could not be determined'
        try:
            with open('/etc/lsb-release', 'r') as lsb_release:
                lines = lsb_release.readlines()
                for line in lines:
                    if "DISTRIB_DESCRIPTION=" in line:
                        self.distribution = line.split("=\"")[1][:-2]
        except:
            pass
        
        #Get username
        self.username = pwd.getpwuid( os.getuid() )[ 0 ]
        
        #Get local IP
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("gmail.com",80))
            self.local_ip = str(s.getsockname()[0])
            s.close()
        except:
            self.local_ip = " could not be determined"
        
        #Get global IP
        url = "http://icanhazip.com/"
        try:
            global_ip_file = urllib2.urlopen(url, timeout=20)
            lines = global_ip_file.readlines()
            self.global_ip = str(lines[0][:-1])
        except:
            self.global_ip = " could not be determined"
        
        #Get uptime
        try:
            with open( "/proc/uptime", "r" ) as f:
                contents = f.read().split()
                f.close()
                total_seconds = float(contents[0])
                # Helper vars:
                MINUTE  = 60
                HOUR    = MINUTE * 60
                DAY     = HOUR * 24
                # Get the days, hours, etc:
                days    = str(int( total_seconds / DAY ))
                hours   = str(int( ( total_seconds % DAY ) / HOUR ))
                minutes = str(int( ( total_seconds % HOUR ) / MINUTE ))
                seconds = str(int( total_seconds % MINUTE ))
                self.uptime = days + ":" + hours + ":" + minutes + ":" + seconds
        except:
            self.uptime = " could not be determined"
        self.labels = {'hostname' : self.hostname,
                  'username' : self.username,
                  'distribution' : self.distribution,
                  'local_ip' : self.local_ip,
                  'global_ip' : self.global_ip,
                  'uptime' : self.uptime
                  }
    
    def update_labels(self):
        '''
        '''
        for label_name in self.labels.keys():
            log(label_name + ': ' + self.labels[label_name])
            try:
                this_label = builder.get_object(label_name)
                this_label.set_text(self.labels[label_name])
            except:
                pass
        window.queue_draw()
        

builder = Gtk.Builder()
builder.add_from_file("ui/pyfactero.glade")
builder.connect_signals(Handler())
window = builder.get_object("py_factero_window")
window.set_title("System Statistics")
window.show_all()

data = Data()
data.update_labels()

window.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

Gtk.main()

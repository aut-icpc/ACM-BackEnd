from django.apps import AppConfig
import threading

def import_receiver():
    global receiver
    receiver = __import__(name='receiver', fromlist=['.'])

class UsermanagementConfig(AppConfig):
    name = 'usermanagement'

    def ready(self):
        receiver_thread = threading.Thread(target=import_receiver)
        receiver_thread.start()

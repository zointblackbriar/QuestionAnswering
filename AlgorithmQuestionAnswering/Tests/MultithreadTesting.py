import json
import os
os.chdir(r'../')

from threading import Thread
import time
import unittest

import requests
import MainFlask

SERVER_URL = "http://127.0.0.1:5000"


class WebServiceThreadingTest(unittest.TestCase):
    def setup(self):
        app = MainFlask()
        self.app = app
    def tear_down(self):
        pass

    def runTest(self):
        #Run the actual threading test

        def start_and_init_server(app):
            app.run(threaded=True)

    #create a thread that will contain our running server
        server_thread = Thread(target=start_and_init_server, args=(self.app, ))
        request_threads = []

        try:
            server_thread.start()
            r = requests.get(SERVER_URL + "/integratedstaticmessage")
            dynamicQueryResult = {"What is the value of sensor1"}
            data = dict(result=dynamicQueryResult)
            range_of_thread = 50
            def post_data():
                r = requests.post(SERVER_URL + "/integratedstaticmessage",data = json.dumps(data))

            for i in range(range_of_thread):
                t = Thread(target=post_data)
                request_threads.append(t)
                t.start()

            # Wait until all of the threads are complete
            all_done = False
            while not all_done:
                all_done = True
                for t in request_threads:
                    if t.is_alive():
                        all_done = False
                        time.sleep(1)

            r = requests.get(SERVER_URL + "/posts/count")
            n_posts = int(r.json()['count'])
            print(n_posts)

        except Exception, ex:
            print("Something went horribly wrong!", ex.message)
        finally:
            server_thread._Thread__stop()
            for t in request_threads:
                t._Thread__stop()


if __name__ == 'main':
    unittest.main()
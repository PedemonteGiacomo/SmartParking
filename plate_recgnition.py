# %% [markdown]
# # Pip dependencies

# %%
#%pip install influxdb-client[ciso]

# %%
#%pip install git+https://github.com/influxdata/flightsql-dbapi.git

# %%
#%pip install flightsql-dbapi

# %%
#!pip install easyocr
#!pip install imutils
#%pip install influxdb3-python

# %%
#%pip install pandas

# %%
#%pip install opencv-python

# %%
#%pip install imutils

# %%
#%pip install easyocr
#%pip install mqtt_client

# %% [markdown]
# # Imports

# %%
import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import influxdb_client_3 as InfluxDBClient3
import pandas as pd
import numpy as np
from influxdb_client_3 import flight_client_options, Point
import certifi
import random
import time
import sys

# %% [markdown]
# # Setup InfluxDB_Client

# %%

def startClient():
    # as reported in the documentation of influxdb_client_3 -> https://github.com/InfluxCommunity/influxdb3-python
    fh = open(certifi.where(), "r")
    cert = fh.read()
    fh.close()

    token = "PBQsMSGwxHHTPHJE_BnjnHa0Ftan6IofOPkq7L5qHAkFWaj8sSuj_mhDyOHIuhfyeCpzuvZ2CRuhU4NypQh-kQ=="
    org = "a12a386fcd5e0885"
    host = "https://eu-central-1-1.aws.cloud2.influxdata.com"
    database="Parking"

    client = InfluxDBClient3.InfluxDBClient3(
        token=token,
        host=host,
        org=org,
        database=database,
        flight_client_options=flight_client_options(
            tls_root_certs=cert))
    
    return client


# %% [markdown]
# # Start Plate Recognition

# %% [markdown]
# ## New, easy reusable funciton

# %%
def recognize_plate(image_path):
  img = cv2.imread(image_path)

  # Define brightness adjustment parameter
  brightness_factor = 0.9     # Values < 1 darken the image

  # Apply brightness reduction
  img = np.clip(img * brightness_factor, 0, 255).astype(np.uint8)

  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
  edged = cv2.Canny(bfilter, 30, 200) #Edge detection

  keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  contours = imutils.grab_contours(keypoints)
  contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

  location = None
  for contour in contours:
      approx = cv2.approxPolyDP(contour, 10, True)
      if len(approx) == 4:
          location = approx
          break

  mask = np.zeros(gray.shape, np.uint8)
  new_image = cv2.drawContours(mask, [location], 0,255, -1)
  new_image = cv2.bitwise_and(img, img, mask=mask)

  (x,y) = np.where(mask==255)
  (x1, y1) = (np.min(x), np.min(y))
  (x2, y2) = (np.max(x), np.max(y))
  cropped_image = gray[x1:x2+1, y1:y2+1]

  reader = easyocr.Reader(['en'])
  result = reader.readtext(cropped_image)

  text = result[0][-2]

  return text

# %% [markdown]
# # Query InfluxDB for plate monitoring

# %%
car_images = ["capture.jpg", "ferrari.jpg", "twingo.jpeg", "NLE003.jpg", "H982FKL.jpg", "mini.jpg", "bmw.jpg", "lambo.jpg", "wolfswagen.jpg"]

def choose_random_plate():
    selected_image = random.choice(car_images)
    plate_number = recognize_plate("license-plates/"+selected_image)
    #print(selected_image+": "+plate_number)
    return plate_number

# %% [markdown]
# ## Inserting data

# %%
def monitor_parked_plate(plate_number, parked, client):
    data = {
        "point1": {
        "plate": plate_number,
        "parked": parked,
        },
    }

    for key in data:
        point = (
        Point("plates_monitoring")
        .tag("vehicole", data[key]["plate"])
        .field("parked",data[key]["parked"])
        )
        client.write(database="Parking",record=point)
        time.sleep(1) # separate points by 1 second

    print("Insertion Completed. Return to the InfluxDB UI.")
  

# %% [markdown]
# ## Query data

# %%

def choose_plate_entrance(client):
    client = client
    plate_number = choose_random_plate()
    inserted = False
    while not inserted:
        
        query = f'SELECT * FROM plates_monitoring WHERE vehicole = \'{plate_number}\''
        # Execute the query
        table = client.query(query=query, language='sql')

        # Convert to dataframe
        df = table.to_pandas().sort_values(by="time", ascending=False)
        
        #print(df)

        # Check if the result is empty to understand if a plate wasn't already present in the db to check if assign it to the car which is try to enter
        if df.empty:
            #print("The plate wasn't yet in the DB. Welcome!")
            # Call the insert_db function to insert a new record
            monitor_parked_plate(plate_number, True, client=client)
            inserted = True
            return plate_number
        else:
            value = df.at[df.index[0], "parked"]
            #print(value)
            if not value:
                #print("Plate already recognized in the past! Welcome back!")
                monitor_parked_plate(plate_number, True, client=client)
                inserted = True
                return plate_number
            # if is already parked I need to choose a different plate
            elif value:
                plate_number = choose_random_plate()
        
    #print(df)
    
def choose_plate_exits(client):
    client = client
    plate_number = choose_random_plate()
    exited = False
    while not exited:
        query = f'SELECT * FROM plates_monitoring WHERE vehicole = \'{plate_number}\''
        # Execute the query
        table = client.query(query=query, language='sql')

        # Convert to dataframe
        df = table.to_pandas().sort_values(by="time", ascending=False)
        
        #print(df)

        # Check if the result is empty to understand if a plate wasn't already present in the db to check if assign it to the car which is try to enter
        if df.empty:
            # plate not already present in the park
            plate_number = choose_random_plate()
        else:
            value = df.at[df.index[0], "parked"]
             #print(value)
            if value:
                #print("Plate already recognized in the past! Welcome back!")
                monitor_parked_plate(plate_number, False, client=client)
                exited = True
                #return plate_number
            # if is already parked I need to choose a different plate
            else:
                plate_number = choose_random_plate()
                
    return plate_number
    




# %%
# plate_number = choose_plate_entrance()
# print(plate_number)

# %%
# plate_number = choose_plate_exits()
# print(plate_number)

#%%
import paho.mqtt.client as mqtt
import json 
# %%

if __name__ == "__main__":
    
    clientInflux = startClient()
    # Create a client
    client = mqtt.Client(clean_session=True)

    # Connect to the broker
    client.connect("test.mosquitto.org", 1883)

    # Subscribe to the topic
    client.subscribe("provaTopic/pythonTrigger")

    #lastmessage = ""

    # Receive messages
    def on_message(client, userdata, message):
        #global lastmessage
        data = message.payload.decode()
        print(data)
        json.dumps(data)
        try:
            # Parse the JSON data in the message
            message_data = json.loads(data)
            #print(message_data)
            # Extract Entrance and Exit values
            entrance_request = message_data.get("EntranceRequest", 0)
            exit_request = message_data.get("ExitRequest", 0)

            # Determine which action to take based on the values
            if entrance_request == 1:
                plate_number = choose_plate_entrance(clientInflux)
                print("Entrance: Plate Number =", plate_number)
            elif exit_request == 1:
                plate_number = choose_plate_exits(clientInflux)
                print("Exit: Plate Number =", plate_number)
            else:
                print("No valid action request in the message.")

        except Exception as e:
            print(f"Error parsing message: {str(e)}")

    # Set the callback function
    client.on_message = on_message

    # Start listening
    client.loop_forever()

# %%

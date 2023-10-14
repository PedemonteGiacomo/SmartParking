#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <Ultrasonic.h>
#include <ESP32Servo.h>
#include <Wire.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqttServer = "test.mosquitto.org";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
const char* temperatureTopic = "provaTopic/temperature";
const char* parkingTopic = "provaTopic/parking";
const char* accessTopic = "provaTopic/access";
const char* pythonTrigger = "provaTopic/pythonTrigger"; 
const char* devicesMonitoring = "provaTopic/devicesMonitoring";

DHT dht(15, DHT22);
Ultrasonic ultrasonic[] = {
    Ultrasonic(13,35),
    Ultrasonic(19,12),
    Ultrasonic(32,14),
    Ultrasonic(33,4)
};
Ultrasonic ultrasonic_access[] = {
  Ultrasonic(5,18),
  Ultrasonic(2,34)
};
Servo servo;
Servo servoExit;

WiFiClient espClient;
PubSubClient client(espClient);

bool occupiedParking[] = {false, false, false, false};
int getArrayLengthOccupiedParking = sizeof(occupiedParking) / sizeof(bool);
// bool prevOccupiedParking[] = {false, false, false, false};
bool accessTry[] = {false, false};
bool deviceMonitoring[] = {true, true, true, true, true, true};
int getArrayLengthDeviceMonitoring = sizeof(deviceMonitoring) / sizeof(bool);

// d25 green led d26 red led
const int greenLedPin = 25;
const int redLedPin = 26;

void setup() {

    Serial.begin(115200);

    // Initialize and connect to WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("WiFi connected");

    servo.attach(21);
    servoExit.attach(27);

    servo.write(0);
    servoExit.write(0);

    // Initialize LED pins as outputs
    pinMode(greenLedPin, OUTPUT);
    pinMode(redLedPin, OUTPUT);

    // Connect to MQTT broker
    client.setServer(mqttServer, mqttPort);
    while (!client.connected()) {
        if (client.connect("esp32-client", mqttUser, mqttPassword)) {
            Serial.println("Connected to MQTT broker");
        } else {
            Serial.print("Failed, rc=");
            Serial.print(client.state());
            Serial.println(" retrying...");
            delay(5000);
        }
    }
}

void loop() {
    
    // Temperature reading
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();
    if (!isnan(temperature) && !isnan(humidity)) {
        String temperatureMessage = "{\"temp\": " + String(temperature) + ", \"humidity\": " + String(humidity) + "}";
        Serial.println("Publishing temperature: " + temperatureMessage);
        client.publish(temperatureTopic, temperatureMessage.c_str());
    }

    // checking istantaneatly the number of occupied park
    int numFreeSpots = 0;
    for (int i = 0; i < getArrayLengthOccupiedParking; i++) {
        if (!occupiedParking[i]) {
            numFreeSpots++;
        }
    }
    bool all_occupied = false;
    if(numFreeSpots == 0){
        all_occupied = true;
    }

    // set the green led high when a park is free, else the park is full so turn on the red light
    if(all_occupied){
        // Turn on the red LED and turn off the green LED
        digitalWrite(greenLedPin, LOW);
        digitalWrite(redLedPin, HIGH);
    }else{
        // Turn on the green LED and turn off the red LED
        digitalWrite(greenLedPin, HIGH);
        digitalWrite(redLedPin, LOW);
    }
        

    // Parking and access status reading
    for (int i = 0; i < getArrayLengthOccupiedParking; i++) {
        int distance = ultrasonic[i].read();
        occupiedParking[i] = (distance < 10) ? true : false; // handling parking sensors
        deviceMonitoring[i] = (distance < 2 || distance > 400)? false : true;
    }


    // PARKING SERVO'S AND PLATE RECOGNITION AND MONITORING
    // when the car pass leaves the sensor 
    if(ultrasonic_access[0].read() > 10 && accessTry[0]){
        servo.write(0);
        accessTry[0]= false;

        // message for entrance request that will call the plate recognition
        String plateMessageEntrance = "{\"EntranceRequest\": " + String(true) + ", \"ExitRequest\": " + String(false) + "}";
        Serial.println("Publishing entrance_plate: " + plateMessageEntrance);
        client.publish(pythonTrigger, plateMessageEntrance.c_str());      
    }
    if(ultrasonic_access[1].read() > 10 && accessTry[1]){
        servoExit.write(0);
        accessTry[1]= false;

        // message for exit request that will call the plate recognition
        String plateMessageExit = "{\"EntranceRequest\": " + String(false) + ", \"ExitRequest\": " + String(true) + "}";
        Serial.println("Publishing exit_plate: " + plateMessageExit);
        client.publish(pythonTrigger, plateMessageExit.c_str());
    }
    // when the car is listened by the sensor
    if(ultrasonic_access[0].read() < 10 && !all_occupied){
        accessTry[0]= true;
        servo.write(90);
    }
    if(ultrasonic_access[1].read() < 10){
        accessTry[1]= true;
        servoExit.write(90);
    }
    // finish the device monitoring
    deviceMonitoring[4] = (ultrasonic_access[0].read() < 2 || ultrasonic_access[0].read() > 400)? false : true;
    deviceMonitoring[5] = (ultrasonic_access[1].read() < 2 || ultrasonic_access[1].read() > 400)? false : true;

    // message for the Device Monitoring
    String message = "{";
    for(int i = 0; i < getArrayLengthDeviceMonitoring - 1; i++){
        message += " \"Device "+ String(i + 1) + "\" : "+ String(deviceMonitoring[i]) + " ,";
    }
    message +=  " \"Device "+ String(getArrayLengthDeviceMonitoring) + "\" : "+ String(deviceMonitoring[getArrayLengthDeviceMonitoring - 1]);
    message += " }";
    Serial.println("Publishing device monitoring: " + message);
    client.publish(devicesMonitoring, message.c_str());

    // Decomment this to send data of parking occupation every time a sensor change:
    // bool changed = false;
    // for(int i = 0; i < getArrayLengthOccupiedParking && changed == false; i++){
    //     if(prevOccupiedParking[i] != occupiedParking[i])
    //         changed = true;
    // }

    //if(changed){
        // Generate the message for the parking 
    String parkingMessage = "{ ";
    for(int i = 0; i < getArrayLengthOccupiedParking - 1; i++){
        parkingMessage += "\"Parking " + String(i + 1) + "\": " + String(occupiedParking[i]) + " , ";
    }
    parkingMessage += "\"Parking " + String(getArrayLengthOccupiedParking) + "\": " + String(occupiedParking[getArrayLengthOccupiedParking - 1]) + " }";
    Serial.println("Publishing parking: " + parkingMessage);
    client.publish(parkingTopic, parkingMessage.c_str());
        // for(int i = 0; i < getArrayLengthOccupiedParking; i++)
        //     prevOccupiedParking[i] = occupiedParking[i];
    //}
    
    delay(1000);
}



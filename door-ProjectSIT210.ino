#include "MQTT.h"
Servo myservo;
// Create an MQTT client
MQTT client("test.mosquitto.org", 1883, callback);


void callback(char* topic, byte* payload, unsigned int length) 
{
    payload[length] = '\0';
    String s = String((char*)payload);
    int counter = s.toInt();
    Particle.publish("Counter",String(counter));
    if(counter<=3){
        
        myservo.attach(D8);
        myservo.writeMicroseconds(1600);
        delay(400);
        myservo.detach();
        delay(4000);
        myservo.attach(D8);
        myservo.writeMicroseconds(1200);
        delay(320);
        myservo.detach();
        delay(4000);
        }
    if(counter==3){
        Particle.publish("limitReached",String(counter));
    }

}

// Setup the Photon
void setup() 
{
    // Connect to the server and call ourselves "photonDev"
    client.connect("photonDev");
    client.subscribe("subscribeTome");

}


// Main loop
void loop() 
{
    // Only try to send messages if we are connected
    if (client.isConnected())
    {
        
        // If the button is pressed it will be read as 0V since the button is
        // in an inverting configuation. 
        
        if(digitalRead(0) == 0)
        {
            // Publish our message to the test server
            client.publish("photonLog", "Button has been pressed");
            delay(1000);        
        }
        
        client.loop();
    }
}

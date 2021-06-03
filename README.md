# Overview
In the past few weeks controlling the crowd or the number of people inside a
shop, office, restaurant ie, was all over the news and it is a current requirement
anywhere we go. When I did my research on the internet I found out that there
are many people counter products on the market, the issue with them was that
they were a bit expensive and they did not provide the functionality to control the
entrance when a certain limit was reached. Thinking about it I decided to base
my SIT210 project around this, so the prototype that I have built has the
following features,
- device which will count the amount of people entering a certain premise.
- An automatic barrier which is connected to a servo and a argon.
- Plotly dashboard for visualizations (could not implement it due to limited
time but have demonstrated how it can be added)

# Design Principles
- Camera should be placed in a place where everyone coming in and out can
be seen.
- The lines which is used In the video’s frames to count entering and leaving
amount should be placed in the right position so that it will correctly
distinguish entering and leaving people.
- Camera should be placed in a good lighting place.

# Prototype Architecture
The raspberry pi camera detects humans using the classifier and if the human
crosses the entering line which is drawn in the video stream, the counter will be
incremented and the value will be sent to the particle argon using the MQTT
protocol. The particle argon then acts by opening the barrier which is controlled
by a servo, the barrier will open and close until the limit as reached and then it
will be closed until a person leaves and the counter is decremented. The particle
argon will trigger a notification which will be sent to the respective person as well
(IFTTT). The protype is Realtime and uses multithreading to maximize
the utilization of the CPU. I could not implement the dashboard due to time
constraints, but ideally if we are going to implement it simply we have to create a
firebase account for the database and connect it to the particle argon which will
send the data. Later on we can easily create a dash web app connected to the
firebase database, which will allow us to display the required visualizations
with the collected data.

# Testing Approach
###### The classifiers accuracy of detecting humans
Tested this using various methods, firstly I was going to use tensorflow lite, since
its machine learning model required more cpu/ram to run smoothly on a
raspberry pi 3, I decided to use cascade classifier which was recommended to
be used with a raspberry pi and it ran the pi camera smoothly with a frame rate
of around 20-25 compared with the TensorFlow lights model which was just
2fps. The cascade classifier is not one of the best classifier’s,but it was good for
my requirements and detected well most of the time I tested it.
######  The incrementing function when a person enters
I tested this functionality many times since this was the main part of the
project, Ideally the counter should be incremented only when the rectangle
which is displayed in the video stream passes all the way through the first
line it did not work as expected the first time I tested it but after making some
changes I was able to fix the issue.
###### The barrier closing function when a limit has reached
When testing this functionality the prototype worked as expected.

# Conclusion
Overall, this was a great experience for me, I was able to learn a lot while
implementing this project including non technical lessons as well, some of the
main technical things I was able to learn was machine learning models,
communication protocols between embedded devices, multi-threading and etc.

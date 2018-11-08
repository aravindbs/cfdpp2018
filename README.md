[StraightOuttaKengeri](https://twitter.com/SoKengeri)'s submission for [Microsoft's codefundo++ 2018](http://www.codefundo.io/).

# DiseaseWatch 

There have been 9 major epidemics of infectious diseases in India since 2006, and have had a death toll of over 50,000 over the last decade world-
wide.

Early preparedness and government initiative could provide epidemic prevention and control capabilities, and potentially save thousands of lives annually.

We attempt to provide epidemic forcasting by disease surveillance using medical information, expert knowledge and statistical modelling of disease activity to predict times and localities of risk. Such an early warning system can provide a mechanism for governments and health-care services to respond to outbreaks in a timely fashion, enabling the impact to be minimized and limited resources to be saved.

## Proposed Solution 

Health data is collected from pharmacies and hospitals regarding recent diagnosis, symptoms, pharmaceutical prescriptions. Anomolous incidents can be detected to help predict possible outbreaks.
Assessment of regional and national statistics will help detect changes in the incidence of infectious diseases.

In case of onset of a possible epidemic, alerts are sent out to the users and relevant agencies along with precautionary measures to be taken.


## Architecture & Tech stack 
![Architecure](https://github.com/aravindbs/cfdpp2018/blob/master/docs/img/architecture.jpg)

---
### [Video Demonstration](https://youtu.be/xOkbK5FE-44)

### [Presentation](https://github.com/aravindbs/cfdpp2018/blob/master/docs/presentation/DiseaseWatch.pdf)

---
## Instructions to run the code 

- Clone the repository 
```
$ git clone https://github.com/aravindbs/cfdpp2018
```
- Change your working directory
```
$ cd cfdpp2018
```
- Create a python virtual environment and activate it.
```
$ virtualenv -p python3 venv
$ . venv/bin/activate 
```
- Install the requirements specified in requirements.txt
```
$ pip install -r requirements.txt 
```
- Download the config file from [here](https://drive.google.com/file/d/1HVrXfXcR-E7o-haZsGN-LOWq_660q9yL/view) and place it in the working directory. 

- Start the server
```
$ cd web
$ python main.py
```
- Open up a web browser and type in ```localhost:5000```


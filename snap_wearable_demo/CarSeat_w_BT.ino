  #define BLUE 3
  #define GREEN 5
  #define HALL 9
  
  char data_from_pi;
  int mode = 0;
  int value = 0;
  int flag = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(HALL, INPUT);
  pinMode(GREEN, OUTPUT);  //GREEN
  pinMode(BLUE, OUTPUT);  //BLUE

  
  digitalWrite(BLUE, LOW);
  digitalWrite(GREEN, LOW);
  
}

void turnBlue()
{
  digitalWrite(BLUE, HIGH);
  digitalWrite(GREEN, HIGH);  
}

void turnGreen()
{
  digitalWrite(BLUE, LOW);
  digitalWrite(GREEN, HIGH);
}

void lightsOff()
{
  digitalWrite(BLUE, LOW);
  digitalWrite(GREEN, LOW);
}


void loop()
{
  value = digitalRead(HALL);
  if (Serial.available() > 0)
  {
    data_from_pi = Serial.read();
    //Serial.println(data_from_pi);
    if (data_from_pi == 'A'){          //pi sends 'A' to turn on
      //Serial.println("MODE 1");
      //turnBlue();
      mode = 1;
    }
      
    else if (data_from_pi == 'D')    //pi sends D to turn off ligthts
      {
        lightsOff();
        mode = 0;
      }
  }
 
  //COUPLING
  if (value == 1 && mode == 1)
  {
    turnGreen();
  }
  
  
  //UNCOUPLING
  if (value == 0 && mode == 1)
  {
    turnBlue();
  }  
}


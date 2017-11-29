int incomingByte = 0;   // for incoming serial data

void setup() 
{
	pinMode(8, OUTPUT);          // sets the digital pin 13 as output
	Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}

void loop() 
{
	if (Serial.available() > 0) 
	{
		incomingByte = Serial.read();
		incomingByte -= 48;
		switch (incomingByte)
		{
			case 1:
					Serial.println("PAPEL");
					digitalWrite(8, HIGH);
					delay(1000);
					digitalWrite(8, LOW);
					break;
			case 2:
					Serial.println("PRASTICO");
					digitalWrite(8, HIGH);
					delay(2000);
					digitalWrite(8, LOW);
					break;
			case 3:
					Serial.println("METAL");
					digitalWrite(8, HIGH);
					delay(3000);
					digitalWrite(8, LOW);
					break;
			case 4:
					Serial.println("Vidro");
					digitalWrite(8, HIGH);
					delay(4000);
					digitalWrite(8, LOW);
					break;
			case 5:
					Serial.println("Organico");
					digitalWrite(8, HIGH);
					delay(5000);
					digitalWrite(8, LOW);
					break;
				default:
					Serial.println("Num te entendi moço");
					break;
		}
	}
}
 
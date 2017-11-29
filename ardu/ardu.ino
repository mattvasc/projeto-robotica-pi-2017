int incomingByte = 0;   // for incoming serial data

void setup() 
{
	/*Configuring arduino's pin to output mode*/
	pinMode(8, OUTPUT);         
  pinMode(10, OUTPUT);
  pinMode(12, OUTPUT);

 	/* opens serial port, sets data rate to 9600 bps*/
	Serial.begin(9600);    

	/*Setting startup values just for safeness*/
	digitalWrite(8, low);
	digitalWrite(10, low);
	digitalWrite(12, low);
	
	/*Moving back the striker if needed*/
	delay(100);
	digitalWrite(10,HIGH);
	delay(400);
	digitalWrite(10, LOW);

}

void aciona_batedor()
{

	/*

  Motor - positivo: relay 1
  Motor - negativo: relay 2

  relay 1: 
  	NF: -
		NA: +
		coil p10

  relay 2:
  	NF: - 
		NA: + 
		coil p12

  */
	Serial.println("Acionando Batedor...");
	Serial.println("Indo");
	digitalWrite(12, HIGH);
	delay(500);
	digitalWrite(12, LOW);
	delay(100);
	Serial.print(" Voltando\n");
	digitalWrite(10,HIGH);
	delay(400);
	digitalWrite(10, LOW);
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
				aciona_batedor();
				break;
			case 2:
				Serial.println("PRASTICO");
				digitalWrite(8, HIGH);
				delay(2000);
				digitalWrite(8, LOW);
				aciona_batedor();
				break;
			case 3:
				Serial.println("METAL");
				digitalWrite(8, HIGH);
				delay(3000);
				digitalWrite(8, LOW);
				aciona_batedor();
				break;
			case 4:
				Serial.println("Vidro");
				digitalWrite(8, HIGH);
				delay(4000);
				digitalWrite(8, LOW);
				aciona_batedor();
				break;
			case 5:
				Serial.println("Organico");
				digitalWrite(8, HIGH);
				delay(5000);
				digitalWrite(8, LOW);
				aciona_batedor();
				break;
			default:
				Serial.println("Num te entendi moço");
				/* Make an elegant dance with the striker */
				digitalWrite(12, HIGH);
				delay(50);
				digitalWrite(12, LOW);
				delay(100);
				digitalWrite(10,HIGH);
				delay(50);
				digitalWrite(10, LOW);
				delay(100);
				digitalWrite(12, HIGH);
				delay(50);
				digitalWrite(12, LOW);
				delay(100);
				digitalWrite(10,HIGH);
				delay(50);
				digitalWrite(10, LOW);
				break;
		}
	}
}
 


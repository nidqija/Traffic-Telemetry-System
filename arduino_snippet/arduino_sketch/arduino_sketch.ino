void setup() {
  // put your setup code here, to run once:

  Serial.begin(9600); // initialize serial communication at 9600 bit per second
  pinMode(12 , OUTPUT);
  pinMode(8 , OUTPUT);
  pinMode(7 , OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(12,HIGH);
  digitalWrite(7,LOW);
  digitalWrite(8,LOW);
  Serial.println("12:1;7:0;8:0");
  delay(3000);

  digitalWrite(12 , LOW);
  digitalWrite(7, HIGH);
  digitalWrite(8,LOW);
  Serial.println("12:0;7:1;8:0");
  delay(3000);
  
  digitalWrite(12,LOW);
  digitalWrite(7,LOW);
  digitalWrite(8,HIGH);
  Serial.println("12:0;7:0;8:1");
  delay(3000);
}

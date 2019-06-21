// Defining Pins
int WE = 10;
int OE = 11;
int increment = 8;
int zero_addr = 9;

int IO[8] = {2,3,4,5,6,7,12,13};
bool input = false; // Flag specifying the input/output state of the IO pins

//Defining Variables
int delay_time = 10; //delay time in millis defining write cycles
int address = 0;
int request = 0;
byte BUFF = 8; //Buffer size for transmission lengths

// ASCII control bytes
byte NEG = '\x00'; // Negetive
byte POS = '\x01'; // Positive

void load_byte(int number){
  //Loads Data to the IO pins to be written
  //Serial.write(number);
  digitalWrite(OE, HIGH);
  digitalWrite(WE, HIGH);
  
   
  // Converts and integar to binary to be loaded into storm
    bool digits[8] = {false,false,false,false,false,false,false,false};
    int count = 0; // Determining where to start in the array
    
    while(number > 0){
      digits[count] = (number % 2 == 1); // Setting True if there is a remainder, false otherwise
      number /= 2;
      count += 1;
    }
  
  //Setting pins to output
  for(int x = 0; x < 8; x++){
      pinMode(IO[x], OUTPUT);
  }
 
  // Setting pin data
  for(int x = 0; x < 8; x++){
    digitalWrite(IO[x], digits[x]);
  }

  
  //Cycling WE
  digitalWrite(WE, true);
  delay(delay_time);
  digitalWrite(WE, false);
  delay(delay_time);
  digitalWrite(WE, true);
  delay(delay_time);
}

int read_byte(){
  //Reads and returns a byte from I/O pins
  int received = 0;
 
  digitalWrite(OE, LOW);
  digitalWrite(WE, HIGH);
  
  // Converting to binary to load to pins

  //Setting pins to output
    for(int x = 0; x < 8; x++){
        pinMode(IO[x], INPUT);
  }
  
  //Reading pins and calculating integar
  for(int x = 0; x < 8; x++){
        if(digitalRead(IO[x])){
            received += (int)( 0.5 + pow(2,x));
        }
  }
  return received;
}

void increment_counter(){
  // Increments the program counter by 2, and sets address accordingly. Increments by two because A[0] is tied to mux
  digitalWrite(increment, LOW);
  digitalWrite(increment, HIGH);
  address += 1;
  delay(0.25);//Waiting for data to latch
  digitalWrite(increment, LOW);
   
  digitalWrite(increment, LOW);
  digitalWrite(increment, HIGH);
  //address += 1;
  delay(0.25);//Waiting for data to latch
  digitalWrite(increment, LOW);
}

void clear_counter(){
  // Zeros the counter
  digitalWrite(zero_addr, HIGH);
  digitalWrite(zero_addr, LOW);
  address = 0;
  delay(0.5);//Waiting for data to latch
  digitalWrite(zero_addr, HIGH);

}

void set_counter(int new_address){
  // Sets the counter to the specified address, by repeatedly incrementing.
  // If the new address is greater than the current, increment untill it is reached
  if(new_address >= address){
    for(int x; x < (new_address - address); x++){
        increment_counter();
    }
  }else{
  // If it is smaller, zero the counter and increment to the new address
    clear_counter();
    for(int x; x < new_address; x++){
        increment_counter();
    }
  }
}

void romRead(int start_address, int end_address){
  clear_counter();
  set_counter(start_address);
  int count = 0;
  
  while(count < (end_address - start_address)){
    Serial.write(read_byte());
    increment_counter();
    increment_counter();
    count++;
  }
  Serial.read();
}


void romWrite(int start_address, int end_address){
  //Writing
  byte dataIn = 0;
  
  //Waiting for data
  clear_counter();
  set_counter(start_address);

  // Getting packets of 64 bytes at a time and requesting more when the buffer is empty
  while(address < end_address){
    if((end_address-address)%64==0)Serial.write(POS);
    while(Serial.available() == 0){}
    dataIn = Serial.read();
      
    //Loading data
    load_byte(dataIn);
    increment_counter();
  }
  Serial.write(NEG);
}

void setup() {
  // put your setup code here, to run once:
  // Setting PinModes
  pinMode(WE, OUTPUT);
  pinMode(OE, OUTPUT);
  
  pinMode(increment, OUTPUT);
  pinMode(zero_addr, OUTPUT);
  digitalWrite(zero_addr, HIGH);
  digitalWrite(increment, HIGH);

  Serial.begin(9600);
  clear_counter();

  // Waiting for connection
  while(Serial.available() == 0){}
  if(Serial.read() == POS){
    Serial.write(POS);
  }
  else{
    Serial.write(NEG);
  }
}

void loop() {
  // put your main code here, to run repeatedly:
    // Getting operation to preform, addresses to perform on, and message size.
  while(Serial.available() < 5){}
  byte operation = Serial.read();
  int start_addr = Serial.read()*256 + Serial.read(); //16 bit addressing
  int end_addr = Serial.read()*256 + Serial.read();
  
  if(operation == POS){
    romRead(start_addr, end_addr);
  }
  if(operation == NEG){
    romWrite(start_addr, end_addr);
  }
  clear_counter();
}

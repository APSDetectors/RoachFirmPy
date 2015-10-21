#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>



volatile int incnt=0;
volatile int outcnt=0;

volatile int inaddr=0;
volatile int outaddr=0;

unsigned char fifo[1048576];


int fifosize=1048576;
int cntsize=2097152;

void readfunct(void *x);
void writefunct(void *x);

unsigned char inbuff[32768];
unsigned char outbuff[1024];


int insize=32768;
int outsize=1024;

pthread_mutex_t mylock;



void readfunct(void *x)
{
	int nbytes;
	
	while (nbytes=read(stdin, inbuff, insize)>0)
	{
		room = outcnt - incnt;
		


	}

}



void readfunct(void *x)
{


}




int main( int argc, const char* argv[] )
{

	pthread_t threadin, threadout;

	int  iret1, iret2;

	iret1 = pthread_create( &threadin, NULL, readfunc, 0);
	if(iret1)
	{
		fprintf(stderr,"Error - RD pthread_create() return code: %d\n",iret1);
		exit(EXIT_FAILURE);
	}

	iret2 = pthread_create( &threadout, NULL, writefunc, 0);
	if(iret2)
	{
		fprintf(stderr,"Error - WR pthread_create() return code: %d\n",iret2);
		exit(EXIT_FAILURE);
	}


	pthread_mutex_init(&mylock, NULL);

    	/* Wait till threads are complete before main continues. Unless we  */
     	/* wait we run the risk of executing an exit which will terminate   */
     	/* the process and all threads before the threads have completed.   */
	 
	pthread_join( thread1, NULL);
	pthread_join( thread2, NULL);
     	exit(EXIT_SUCCESS);
}





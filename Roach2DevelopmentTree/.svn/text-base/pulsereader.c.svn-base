#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>
#include <time.h>


char polarmems[256];
char regstats[256];
char regctrls[256];
char fifoovcnts[256];
char memaddrs[256];


FILE  *polarmem;
int regctrl;
int regstat;
int fifoovcnt;
int memaddr;


int valstat;

int valctrl=0;

int b_fftmemweds=0;
int b_stfftmemds =1;
int b_bitfromds0 =2;
int b_bitfromds1 =3;
int b_bitfromds2 =4;
int b_bitfromds3 =5;
int b_fifoovrst=6;

void enableOutMem(int is_en);


int readRewindMem(void);
int readRewindMem2(void);
void rewindOutMem(void);
void resetFifoOvCnt(void);


int mem_buff[32768];


int total_buffers=0;
int total_unread = 0;

int num_fulls=0;

//unsigned int header1[]={0xcccccccc,0xbbbbbbbb};
//unsigned int header2[]={0xeeeeeeee,0xdddddddd};

//sec to run. -1 mean forever
int runtime = -1;
//sec stat time.
int starttime=0;


/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  
void my_handler(sig_t s){
           fprintf(stderr,"Caught signal %d\n Dumping last bit of mem\n",s);
	   
	
	 readRewindMem2();
	fflush(stdout);
	fclose(stdout);
	fclose(stdin);

	   //usleep(2000000);
           exit(0); 

}



int main( int argc, const char* argv[] )
{
	int is_run=1;
	int nread;
	int dct=0;
	
	int fftcnt_done, is_pulse,run_ffts,fifo_data_full,bittods0,bittods1,fifo_data_avail,fftmemwe,outmemdone,stfftmem;
	
	
	//a ctrl D will cause nice close up where last bit of mem is read
	 signal (SIGINT,my_handler);
	
	starttime = clock()/CLOCKS_PER_SEC;
				

	if (argc<2)
	{
		fprintf(stderr,"Need 1 arg that is pid of fpga\n optional 2nd arg for sec to run\n");
		exit(EXIT_FAILURE);
	}
	
	if (argc==3)
	{
		runtime = atoi(argv[2]);
	
	}
	
	sprintf(polarmems,"/proc/%s/hw/ioreg/MemRecordPolar_Shared_BRAM",argv[1]);
	sprintf(regstats,"/proc/%s/hw/ioreg/readoutStat",argv[1]);
	sprintf(regctrls,"/proc/%s/hw/ioreg/readoutControl",argv[1]);
	sprintf(fifoovcnts,"/proc/%s/hw/ioreg/fifoOverFlowCnt",argv[1]);

	sprintf(memaddrs,"/proc/%s/hw/ioreg/MemRecordPolar_coefRamAddr",argv[1]);



	polarmem = fopen(polarmems,"rb");
	regctrl = open(regctrls,O_WRONLY);
	regstat = open(regstats,O_RDONLY);
	fifoovcnt = open(fifoovcnts,O_RDONLY);
	memaddr = open(fifoovcnts,O_RDONLY);
	
	


	if (polarmem==NULL)
	{
		fprintf(stderr,"Cannot find polarmem");
		exit(EXIT_FAILURE);
	}

	

	if (regctrl<0)
	{
		fprintf(stderr,"Cannot find regctrl");
		exit(EXIT_FAILURE);
	}
	
	if (regstat<0)
	{
		fprintf(stderr,"Cannot find reg stat");
		exit(EXIT_FAILURE);
	}
    	if (fifoovcnt<0)
	{
		fprintf(stderr,"Cannot find fifoovcnt");
		exit(EXIT_FAILURE);
	}	
    	if (memaddr<0)
	{
		fprintf(stderr,"Cannot find MemRecordPolar_coefRamAddr");
		exit(EXIT_FAILURE);
	}	
	enableOutMem(1);
	resetFifoOvCnt();
	
	while(is_run)
	{
		
		nread =readRewindMem();
		if (runtime>-1)
		{
		  clock_t tt;
		  int secx;

		  tt=clock();
		  secx=(tt/CLOCKS_PER_SEC)-starttime;
		  if (secx>=runtime)
		   {   is_run=0;
			  fprintf(stderr,"All Done- out of time\n");
		   }
		}		
		
		
		if (nread>0)
		{
			
			
			if (dct==0)
			{    
			    fftcnt_done=valstat&512;
			    is_pulse=valstat&256;
			    run_ffts=valstat&128;
			    fifo_data_full=valstat&64;
			    bittods0=valstat&32;
			    bittods1=valstat&16;
			    fifo_data_avail=valstat&8;
			    fftmemwe=valstat&4;
			    outmemdone=valstat&2;
			    stfftmem=valstat&1;

			    fprintf(stderr,
				"\n------------\nfftcnt_done=%d \n is_pulse=%d \nrun_ffts=%d \nfifo_data_full=%d \nbittods0=%d \nbittods1=%d \nfifo_data_avail=%d \nfftmemwe=%d \noutmemdone=%d \nstfftmem=%d\n",
				fftcnt_done, is_pulse,run_ffts,fifo_data_full,bittods0,bittods1,fifo_data_avail,fftmemwe,outmemdone,stfftmem);
				
				
			      fprintf(stderr,"\nregctrl 0x%x\n",valctrl);
			      
			      fprintf(stderr,"Recent Words Read %d\n",nread);
			      fprintf(stderr,"Total Buffs Read %d\n",total_buffers);
			      fprintf(stderr,"Total Words UnRead %d\n",total_unread);
			      	
			      lseek(fifoovcnt,0,SEEK_SET);
			      read(fifoovcnt,&num_fulls, sizeof(int));
			      
			      fprintf(stderr,"FifoOverflows  %d\n",num_fulls);
			      
			     
			      
			      
			}
			
		}

		dct= (dct+1)%30000;
		
		

		//usleep(100000);
	}
	 readRewindMem2();
	fflush(stdout);
	fclose(stdout);
		fclose(stdin);


}

void resetFifoOvCnt(void)
{

	valctrl=valctrl | (1<<b_fifoovrst);
	lseek(regctrl,0,SEEK_SET);
	write(regctrl,&valctrl,4);
		
	valctrl=valctrl - (1<<b_fifoovrst);
	
	lseek(regctrl,0,SEEK_SET);
	write(regctrl,&valctrl,4);
}


void enableOutMem(int is_en)
{


	if (is_en)
		valctrl=valctrl| (1<<b_fftmemweds);
	else
	{
		if (valctrl&b_fftmemweds)
			valctrl=valctrl - (1<<b_fftmemweds);
	}
	lseek(regctrl,0,SEEK_SET);
	write(regctrl,&valctrl,4);

}



void rewindOutMem(void)
{
	valctrl=valctrl | (1<<b_stfftmemds);
	lseek(regctrl,0,SEEK_SET);
	write(regctrl,&valctrl,4);
		
	valctrl=valctrl - (1<<b_stfftmemds);
	
	lseek(regctrl,0,SEEK_SET);
	write(regctrl,&valctrl,4);

}

//
// of outmem is full, outmemdone flag is hi. if hi then read 32k from outmem
//

int readRewindMem(void)
{	
	int outmemdone;
	int nread;
	int nreadleft;
	int toread;
	
	int num2read=32878;
	int bsize=4096;
	
	nread=0;
	
	lseek(regstat,0,SEEK_SET);
	nread = read(regstat,&valstat, sizeof(int));
	
	if (nread)
	{
	    outmemdone=valstat&2;
	  
	    
	    if (outmemdone)
	    {
	     	//enableOutMem(0);

		
		fseek(polarmem,0,SEEK_SET);
		nreadleft = num2read;//32768
		nread=1;
		toread=bsize;//4096
		while(nread && (nreadleft>0))
		 {
		    
		    if (nreadleft<toread)
		    	toread=nreadleft;
		 
		    nread = fread(mem_buff,sizeof(int), nreadleft,polarmem);
		    fflush(polarmem);
		    nreadleft=nreadleft - nread;
		   
		  }
		
		
		total_unread+=	nreadleft;
		total_buffers+=1;
		rewindOutMem();
		
		fwrite(mem_buff, sizeof(int), 32768, stdout);




		fflush(stdout);
		
		//enableOutMem(1);
	    }
	}
	
	return(nread);
	

}
//
// get address of the mem counter. read the number of words that is shown in address
//
int readRewindMem2(void)
{	
	int outmemdone;
	int nread;
	int nreadleft;
	int toread;
	int numwords;
	int bsize=4096;
	nread=0;
	
	lseek(memaddr,0,SEEK_SET);
	nread = read(memaddr,&numwords, sizeof(int));
	
	if (nread)
	{
	    
	  
	    
	    if (numwords>0)
	    {
	     	//enableOutMem(0);

		
		fseek(polarmem,0,SEEK_SET);
		nreadleft = numwords;
		nread=1;
		toread=bsize;//4096
		while(nread && (nreadleft>0))
		 {
		    
		    if (nreadleft<toread)
		    	toread=nreadleft;
		 
		    nread = fread(mem_buff,sizeof(int), nreadleft,polarmem);
		    fflush(polarmem);
		    nreadleft=nreadleft - nread;
		   
		  }
		
		
		total_unread+=	nreadleft;
		total_buffers+=1;
		rewindOutMem();
		
		fwrite(mem_buff, sizeof(int), numwords, stdout);




		fflush(stdout);
		
		//enableOutMem(1);
	    }
	}
	
	return(nread);
	

}




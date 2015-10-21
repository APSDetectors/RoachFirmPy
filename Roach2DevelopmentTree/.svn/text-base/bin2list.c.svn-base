/**
cd ROACH/projcts

gcc -lm -o bin2list bin2list.c


to run
  
./bin2hdf5 aa.h5 65536 < testdata.bin


*/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>






#define MAX_CHAN 256
#define EVLEN 34
#define WAVELEN 32
#define BUFFSIZE 65536
#define PI 3.14159

//
// masks and datatuypes for readingh the raw data
//

//
//we get data in retuyrned memory in packets. we have two rams, for phase and mag
//phase has the header data.preceeding phse data
//header is 0x10000 followed by int, chan number . The length of the data is set in 	
//fifoFSMPh.m, or the firmware. it is 32 words long in the memory.
int outmem_headerlen=2;
//32 ints long
int outmem_datalen=32;
//mem is 32 bits wide.
int outmem_width=32;
//below is sign buts, total buts, num frac buts
int outmem_mag_datatype[] = {0,16,16};
int outmem_phs_datatype[] = {1,16,13};

int outmem_hi_zero=0xfe000000;
int outmem_ts_masklow = 0x01fffe00;
int outmem_ts_maskhi = 0xffff0000;
int outmem_ts_norm= 65536;
int outmem_fff_mask=0xffff;
int outmem_chan_mask=0xff;
int outmem_pulse_mask=0x100;




unsigned int membuff[BUFFSIZE];
int memindex=0;


unsigned short dp[32];
unsigned short dm[32];
float dataph[32];
float datamag[32];

int datasetlength=4096;


int extractMag(unsigned int *mem,unsigned short *mag_);
int extractPhs(unsigned int *mem,unsigned short *phs_);

void convToFloat(int dlen,unsigned short data[], int datatype[],float newdata[],float gain);
 int swapIntEndian(unsigned int *data, int len);



int legal_chans[MAX_CHAN];
int leg_chan_cnt=0;

int num_illegal_chans=0;


/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  

int main(int argc, char *argv[])
{
FILE *fin;

 int k;
 int searches;
 int carryoffs;
 int chan;
 unsigned int timestamp;
 int is_pulse;
 int nread;
int endsearch;
int list_index;
int nextk;
int evtcnt=0;
int readcount = 0;

int k2=0;

int is_chan_legal=1;


searches=0;







    if (argc>1)
    {
        char *chanstr;
	char *chan_s;
    	int argi=1;
	
	//look for options. argc-1 is the outfilename.
	while (argi<(argc-1))
	{
	
	    if (strcmp(argv[argi],"-chans")==0)
	    {
		//found list of legal channels
		chanstr=argv[argi+1];
		
		
		fprintf(stderr, "Found channel list:\n");
		chan_s = strtok(chanstr,",");
		while(chan_s!=NULL)
		{
	
		    //fprintf(stdout,"here\n");
		    //fprintf(stdout,"%s\n",chan_s);
	    	    legal_chans[leg_chan_cnt]=atoi(chan_s);
		   
		    
		    fprintf(stderr,"%d ",legal_chans[leg_chan_cnt]);
		    leg_chan_cnt++;
		    chan_s=strtok(NULL,",");
		}
		    fprintf(stderr,"\n");
		
		
		argi+=2;
		
	    }
	    else
	       argi++;
	
	}
	
	
    
    }



   
    carryoffs = 0;
    nread = fread(membuff+carryoffs,sizeof(int),BUFFSIZE-carryoffs,stdin);
    
    swapIntEndian(membuff+carryoffs, nread);
    while (nread > 0)
    {
    	//printf("nread = %d",nread);
	endsearch=nread-(EVLEN+4);
	k=0;
	while(k<endsearch)
	{
//	    if ( (membuff[k]&outmem_fff_mask == 0xaaaa) && (membuff[k+EVLEN]&outmem_fff_mask == 0xaaaa) )
	    if ( (membuff[k]&outmem_fff_mask) == 0xaaaa )
	    {
	       // printf("found start of event\n");

		chan=membuff[k+1]&outmem_chan_mask;
		is_chan_legal=1;
		if (leg_chan_cnt>0)
		{
		    //make sure chan is in legal chan
		    is_chan_legal=0;
		    for (k2=0;k2<leg_chan_cnt;k2++)
		    {
		         if (chan==legal_chans[k2])
			     is_chan_legal=1;
		    }
		    
		}
		
		if (is_chan_legal)
		{

		    timestamp = (int)(membuff[k]&outmem_ts_maskhi);
		    timestamp = timestamp + ((membuff[k+1]&outmem_ts_masklow) >>9);
		    is_pulse = membuff[k+1]&outmem_pulse_mask;


		    extractMag(&membuff[k+2],dm);	
		    extractPhs(&membuff[k+2],dp);	

		    convToFloat(WAVELEN,dp,outmem_phs_datatype,dataph,PI);
		    convToFloat(WAVELEN,dm,outmem_mag_datatype,datamag,1.0);




		    printf("Chan %d nread=%d, ts 0x%x eventcnt %d readcnt %d searches %d\n",			
			    chan,
			    nread,
			    timestamp,
			    evtcnt,
			    readcount,
			    searches);
		}
		else
		{
		    //printf("Illegal chan %d\n",chan);
		    num_illegal_chans++;
		}
		
		

		nextk=k+outmem_headerlen + outmem_datalen;			


		k = nextk;
		evtcnt=evtcnt+1;

	    
	    }
	    else
	    {
	    	k++;
		searches++;
		//printf("0x%x  masked 0x%x  \n",
		//	membuff[k],
		//	(membuff[k]&outmem_fff_mask));
	    }

	}
	
	carryoffs=BUFFSIZE-k;
	
	memcpy(membuff,membuff+k,carryoffs*sizeof(int));
	nread = fread(membuff+carryoffs,sizeof(int),BUFFSIZE-carryoffs,stdin);
	swapIntEndian(membuff+carryoffs, nread);
	//copy carryiover to start of buffer
	readcount++;

    }
	

printf("searches %d, events %d  k %d illigalchans %d\n",searches, evtcnt,k,num_illegal_chans);

}


/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  
 int swapIntEndian(unsigned int *data, int len)
 {
 
 int k;
 
 unsigned char tval[4];
 unsigned char tval2[4];
 
 unsigned int *iptr;
 
 for (k=0;k<len;k++)
 {
    iptr=(unsigned int*)tval;
    *iptr=data[k];
    tval2[0]=tval[3];  
    tval2[1]=tval[2];  
    tval2[2]=tval[1];  
    tval2[3]=tval[0];  
    iptr=(unsigned int*)tval2;
    data[k]=*iptr;

    
 }
 
 }
  
/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  
int extractMag(unsigned int *mem,unsigned short *mag_)
{
    int k;
    
    for (k=0;k<WAVELEN;k++)
    {
    	mag_[k]=(mem[k]&0xffff0000)>>16;
    }			
			
			

}
/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  


int extractPhs(unsigned int *mem,unsigned short *phs_)
{

    int k;
    
    for (k=0;k<WAVELEN;k++)
    {
    	phs_[k]=(mem[k]&0xffff);
    }			
			
			
}
  


//###########################################################################
//#
//#/data type is (18,15) where we have 18 bits data, 15 fraction bits
//#converts vector of binary twos comp to floats.
//###########################################################################

void convToFloat(int dlen,unsigned short data[], int datatype[],float newdata[],float gain)
{
   	int k;
	unsigned short d;

	int numintbits=0;
	int intmask=0;
	int signmask=0;
	float signval_=0;
	float signval=0.0;
	
	int fracmask=0;
	float fracnorm=1.0;
	
	int nfrac=2;
	int nbits=1;
	int sbit=0;
	float frac=0.0;
	int fracpart=0;
	int intpart=0;
	float intval=0;
	float signbit=0.0;
	float val=0.0;
	
	if (datatype[nfrac]>0)
	{
	    fracmask = (int)(pow(2.0,datatype[nfrac])-1);
	    fracnorm=(float)(pow(2.0,datatype[nfrac]));
	}
	else
	{
	    fracmask = 0;
	    fracnorm=1.0;
	}

	//mask for int part not including sign bit.
	//datatype[output][0] - datatype[output][1] - 1 is 18-15-1=2, where we have 2 bits
	//fir int part not counting sign bit.
	numintbits =   datatype[nbits] - (datatype[sbit] + datatype[nfrac]);
	
	//for 2 int buits, we take 3<<numfracbits, 3<<15	
	//his is int portion mask not incl the 	
	if (numintbits>0)	
	    intmask=((int)(pow(2.0,numintbits)-1)) << datatype[nfrac];
	else
	    intmask=0;

	//sign mask is numbuts-1
	if (datatype[sbit]>0)
	 {
	    signmask = (int)(pow(2.0,(datatype[nbits]-1)));
	    signval = -1.0 * ((float)(signmask))/fracnorm;
	}
	else
	{
	    signmask=0;
	    signval=0.0;
	}

	//print 'fracmask %x fracnorm  %f numintbits  %d intmask  %x signmask  %x signval  %f '%\
	//	(fracmask,fracnorm,numintbits,intmask,signmask,signval)

	for ( k =0; k<dlen;k++)
	{
	    d=data[k];
	

	    fracpart=((int)(floor(d))) &  fracmask;
	    frac =  ((float)(fracpart))/fracnorm;

	    intpart = ((int)(d)) & intmask;
	    intval = ((float)(intpart)) / fracnorm;

	    //if we have 18 bit data, sign but is but 17.
	    //signbit will be 1 or 0, below becayse of > sign
	    signbit=0.0;
	    if  ((( (int)(d)) & signmask)>0)
	        signbit=1.0;
		
		
	    signval_ = signbit*signval;

	    val = signval_ + intval + frac;

		//#print ' fracpart  %d   frac %f intpart  %d  intval %f signbit  %d signval_  %f  val %f'%\
		//#	(fracpart,frac,intpart,intval,signbit,signval_,val)

	    newdata[k]=val*gain;

	}
}
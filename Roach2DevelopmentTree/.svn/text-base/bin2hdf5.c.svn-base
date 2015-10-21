/**
cd ROACH/projcts

gcc -lm -o bin2hdf5 bin2hdf5.c\
-I../../swWork/hdf5/hdf5-1.8.7-linux-x86_64-static/include \
../../swWork/hdf5/hdf5-1.8.7-linux-x86_64-static/lib/libhdf5.a \
../../swWork/hdf5/hdf5-1.8.7-linux-x86_64-static/lib/libhdf5_hl.a \
../../swWork/hdf5/hdf5-1.8.7-linux-x86_64-static/lib/libz.a \
../../swWork/hdf5/hdf5-1.8.7-linux-x86_64-static/lib/libsz.a \
-lc 



to run
  
./bin2hdf5 aa.h5  < testdata.bin

To stream from network to hdf5
nc -l 7777 | ./bin2hdf5 myhdf.h5


ctrl c will cauyse close of hdf5 files
*/

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <signal.h>
#include <string.h>


#include "hdf5.h"



struct chaninfo{
int chan;
// store group, or directory for each channel
hid_t groupid;
// array of magnitures
hid_t magdsid;
//num of things in mag array
hid_t magattr;
// array of phases
hid_t phsdsid;
//num ele in phase array
hid_t phsattr;
//array of timestamps
hid_t tsid;
//num of timestamps
hid_t tsattr;


//num of ele in mag, phs as an int. same as the above attrs
unsigned int dataindex;
//num of timestamps in array, same as above attr
unsigned int tsindex;
// lengh of actual datasets (always mylt of 4k, and > than the num of ele)
unsigned int datalen;
unsigned int tslen;
};



char rootname[255];
rootname = "/"; 


#define MAX_NAME 1024


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

int outmem_ts_masklow = 0x0001fffe00;
int outmem_ts_maskhi = 0xffff0000;
int outmem_ts_norm= 65536;
int outmem_fff_mask=0xffff;
int outmem_chan_mask=0xff;
int outmem_pulse_mask=0x100;




struct chaninfo chanlist[MAX_CHAN];

int chanlist_len=0;

char *outfilename;
char *infilename;


unsigned int membuff[BUFFSIZE];
int memindex=0;


unsigned short dp[32];
unsigned short dm[32];
float dataph[32];
float datamag[32];

//hdf 5 file
hid_t hfile;
// memory size we write to the hdf5 file. it will be 32 floats.
hid_t memspace_id;
hid_t memspace_id2;
hid_t memspace_id3;
hid_t memspace_id4;
hid_t memspace_id5;


int datasetlength=4096;



void closeChannels(void);
int extractMag(unsigned int *mem,unsigned short *mag_);
int extractPhs(unsigned int *mem,unsigned short *phs_);
int findChannel(int cnum);
int makeNewChannel(int cnum);
int writeData(int k, int timestamp, float mag[], float phs[]);
void convToFloat(int dlen,unsigned short data[], int datatype[],float newdata[],float gain);
int swapIntEndian(unsigned int *data, int len);
 int openChannel(int cnum);

  int openHdfFileObjects(void);



int legal_chans[MAX_CHAN];
int leg_chan_cnt=0;

int num_illegal_chans=0;

/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  
void my_handler(sig_t s){
           printf("Caught signal %d\n",s);
	   
	closeChannels();

	   
           exit(0); 

}


/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  
void closer(void){
           
	   
	closeChannels();

	   
           exit(0); 

}


/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  

int main(int argc, char *argv[])
{
FILE *fin;

 int k,k2,k3;
 int searches;
 int carryoffs;
 int chan;
 unsigned int timestamp;
 int is_pulse;
 hsize_t memdims[2];
 int nread;
int endsearch;
int list_index;
int nextk;
int evtcnt=0;

int is_chan_legal=1;


 signal (SIGINT,my_handler);
// atexit (closer);



searches=0;

    if (argc==1)
    {
	    fprintf(stderr,"Need  outfilename and options\n");
	    fprintf(stderr,"  outfilename must be LAST arg\n");
	    
	    fprintf(stderr,"-chans 0,1,2,3,128 \n");
	    fprintf(stderr,"-dir hdfgroup/path/ \n");
	    
	    exit(1);
    }

    //infilename = argv[1];
    outfilename=argv[argc-1];
    //datasetlength=atoi(argv[2]);
    
    // find options
    
    
    if (argc>=3)
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
	    if (strcmp(argv[argi],"-dir")==0)
	    {
	    	int ll;
		
	    	argi++;
		strcpy(rootname,argv[argi])
		argi++;
		
		//make sure there is / on end of the str.
		ll = strlen(rootname);
		if (rootname[ll-1]!='/')
		{
			//stick / on end of string. C string.. end in 0...
			rootname[ll]='/';
			rootname[ll+1]=0;
			
		}
		
	
		
	    }
	    else
	       argi++;
	
	}
	
	
    
    }
    
    
    //fin=fopen(infilename,"rb");
    
    //open new hdf file
    
    if (access(outfilename, F_OK) ==-1)
    {
        hfile = H5Fcreate( outfilename,H5F_ACC_EXCL , H5P_DEFAULT, H5P_DEFAULT ) ;

    }
    else
    {
        printf("File already exists, will append\n");
	hfile = H5Fopen( outfilename, H5F_ACC_RDWR, H5P_DEFAULT ); 
	openHdfFileObjects();
	
	if (hfile <0)
	{
	   fprintf(stderr,"Bad Hdf file already existant, cannot open\n");
	   exit(2);
	}
	
	
    }

//!!
//exit(0);



   // we will write arrauys of 32x1 arrays of floats . this is shape ofour memory we will write 
    
    memdims[0] = 1;
    memdims[1] = 32;
    memspace_id = H5Screate_simple (2, memdims, NULL); 


    memdims[0] = 1;
    memdims[1] = 1;
    memspace_id2 = H5Screate_simple (2, memdims, NULL); 


    memspace_id3 = H5Screate_simple (2, memdims, NULL); 
    memspace_id4 = H5Screate_simple (2, memdims, NULL); 
    memspace_id5 = H5Screate_simple (2, memdims, NULL); 




    //
    // if we spec'ed channel list, create the channels imn the hdf file if they are not already present
    //
    
    printf("Attempt to make channes in chan list %d\n",leg_chan_cnt);
    
    
    for (k3=0;k3<leg_chan_cnt;k3++)
    {
    	//see if chan is already in channel list
	chan=legal_chans[k3];

    	

	//serarch for chan in the list
        list_index = findChannel(chan);
	//if not in list, create the channel
	if (list_index==-1)
	    list_index = makeNewChannel(chan);
    }
    
    
    //
    // start reading stdin and dymping to hdf5
    //


    	
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
	    if ((membuff[k]&outmem_fff_mask) == 0xaaaa )
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


		    list_index = findChannel(chan);
		    if (list_index==-1)
			    list_index = makeNewChannel(chan);

		    writeData(list_index,  timestamp, datamag, dataph);

	        }
		else
		{
		    //printf("Illegal chan %d\n",chan);
		    num_illegal_chans++;
		}

		nextk=k+outmem_headerlen + outmem_datalen;			
		k = nextk;
		evtcnt=evtcnt+1;
		
		//!!
		//k=endsearch;

			    
	    }
	    else
	    {
	    	k++;
		searches++;
	    }

	}
	
	carryoffs=BUFFSIZE-k;	
	memcpy(membuff,membuff+k,carryoffs*sizeof(int));

	nread = fread(membuff+carryoffs,sizeof(int),BUFFSIZE-carryoffs,stdin);
	swapIntEndian(membuff+carryoffs, nread);
	//copy carryiover to start of buffer
	
	//!! 
	//nread=0;

    }
	

closeChannels();

printf("searches %d, events %d  k %d  badchannels %d",searches, evtcnt,k,num_illegal_chans);

//fclose(fin);

}



/***********************************************************************************************
 * for already existant files we search the files and pipulate the challen list.
 *  when file is oened, we call this to make sure we have info on the already exiosting data
 *********************************************************************************************/
  
  int openHdfFileObjects(void)
  {
    herr_t err;
    hsize_t nobj,len;
   hid_t root;
   int i;
   int otype;
   int chan;
   
   	char group_name[MAX_NAME];
	char memb_name[MAX_NAME];
	
	
	
	
   root = H5Gopen(hfile,rootname, H5P_DEFAULT);
    err = H5Gget_num_objs(root, &nobj);
    
    printf("Found %d objects \n",nobj);
	for (i = 0; i < nobj; i++) 
	{
	    printf("  Member: %d ",i);
	    
	    len = H5Gget_objname_by_idx(
	        root, 
		(hsize_t)i, 
		memb_name, 
		(size_t)MAX_NAME );
		otype =  H5Gget_objtype_by_idx(root, (size_t)i );
	
			
		printf("   %d ",len);fflush(stdout);
		printf("  Member: %s ",memb_name);fflush(stdout);
		
		if (otype==H5G_GROUP)
		{ 
		    printf("Group  ");
		    
		    if (strstr(memb_name,"Chan")!=NULL)
		    {
		        printf("Channel ");
			chan=atoi(memb_name+6);
			printf("%d \n",chan);
			
			openChannel(chan);
			
		    }    
		}
		
		
	    printf("\n");
	}
	
    H5Gclose(root);
  
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

/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  
int findChannel(int cnum)
{
    int k;
    int retval=-1;
    
    for (k = 0; k< chanlist_len;k++)
    {
        if (chanlist[k].chan==cnum)
	    return(k);
    
    }
    
    return(-1);

}

/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  
int makeNewChannel(int cnum)
{
    char gname[32];
herr_t       status;
    hid_t prop;
    
    hsize_t maxdims[2];

    hsize_t attr_dims[2];

    
    hsize_t d_dims[2];
hsize_t ts_dims[2];

    hid_t dataspace_id;

    hid_t attrspace;
    hid_t attrid;
    
    int k = chanlist_len;
    chanlist_len++;

    	        printf("make new chan %d\n",cnum);

    
    
    chanlist[k].chan = cnum;
    chanlist[k].dataindex = 0;
    chanlist[k].tsindex = 0;
    sprintf(gname,"%sChan_%05d",rootname,cnum);
    
    chanlist[k].groupid = H5Gcreate(hfile, gname, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
    
    
    //create datasets and dataspaces
    
    d_dims[0]=1;
    d_dims[1]=datasetlength;
    
    ts_dims[0]=1;
    ts_dims[1]=datasetlength/32;
   
    chanlist[k].datalen=d_dims[1];
    chanlist[k].tslen=ts_dims[1];
    
    maxdims[0]=1;
    maxdims[1]=H5S_UNLIMITED;
    
    
    
    // create infinite space
    
    dataspace_id = H5Screate_simple(2, d_dims,maxdims);
    
     /* Modify dataset creation properties, i.e. enable chunking  */
    prop = H5Pcreate (H5P_DATASET_CREATE);
    status = H5Pset_chunk (prop, 2, d_dims);
    
    chanlist[k].phsdsid = H5Dcreate(
     	chanlist[k].groupid, 
	"phase", 
	H5T_NATIVE_FLOAT,
	 dataspace_id,
        H5P_DEFAULT, prop, H5P_DEFAULT);
	
     attr_dims[0]=1;attr_dims[1]=1;	
     attrspace = H5Screate_simple(2, attr_dims,NULL);
     chanlist[k].phsattr = H5Acreate (
     	chanlist[k].phsdsid, 
	"DataLen",
	 H5T_NATIVE_INT, 
	 attrspace, 
	 H5P_DEFAULT,
         H5P_DEFAULT);
   
     H5Pclose(prop);	
     H5Sclose (dataspace_id);
     H5Sclose (attrspace);
     
   dataspace_id = H5Screate_simple(2,  d_dims,maxdims);
        /* Modify dataset creation properties, i.e. enable chunking  */
    prop = H5Pcreate (H5P_DATASET_CREATE);
    status = H5Pset_chunk (prop, 2, d_dims);

     chanlist[k].magdsid = H5Dcreate(
     	chanlist[k].groupid, 
	"magnitude", 
	H5T_NATIVE_FLOAT,
	 dataspace_id,
        H5P_DEFAULT, prop, H5P_DEFAULT);
     
     attr_dims[0]=1;attr_dims[1]=1;	
     attrspace = H5Screate_simple(2, attr_dims,NULL);
     chanlist[k].magattr = H5Acreate (
     	chanlist[k].magdsid, 
	"DataLen", 
	H5T_NATIVE_INT, 
	attrspace, 
	H5P_DEFAULT, 
	H5P_DEFAULT);

     
      H5Pclose(prop);
    H5Sclose (dataspace_id);
          H5Sclose (attrspace);

     
     
     
        dataspace_id = H5Screate_simple(2, ts_dims,maxdims);
	
	   /* Modify dataset creation properties, i.e. enable chunking  */
    prop = H5Pcreate (H5P_DATASET_CREATE);
    status = H5Pset_chunk (prop, 2, ts_dims);
 
    chanlist[k].tsid = H5Dcreate(
     	chanlist[k].groupid, 
	"timestamps", 
	H5T_NATIVE_INT,
	 dataspace_id,
        H5P_DEFAULT, prop, H5P_DEFAULT);
        
     attr_dims[0]=1;attr_dims[1]=1;	
     attrspace = H5Screate_simple(2, attr_dims,NULL);
     chanlist[k].tsattr = H5Acreate (
     	chanlist[k].tsid, 
	"DataLen", 
	H5T_NATIVE_INT, 
	attrspace, 
	H5P_DEFAULT, 
	H5P_DEFAULT);

     H5Pclose(prop);
       H5Sclose (dataspace_id);
        H5Sclose (attrspace);

}




/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  
int openChannel(int cnum)
{
    char gname[32];
herr_t       status;
    
 int dlen;

    
    hsize_t d_dims[2];

    hid_t dataspace_id;

    
    int k = chanlist_len;
    chanlist_len++;

    	        printf("Open chan %d\n",cnum);

    
    
    chanlist[k].chan = cnum;
    chanlist[k].dataindex = 0;
    chanlist[k].tsindex = 0;
    sprintf(gname,"%sChan_%05d",rootname,cnum);
    
    
    
    chanlist[k].groupid = H5Gopen( hfile, gname ,H5P_DEFAULT); 
    
    //create datasets and dataspaces
    
    
    chanlist[k].phsdsid = H5Dopen( chanlist[k].groupid, "phase",H5P_DEFAULT );
    chanlist[k].magdsid = H5Dopen( chanlist[k].groupid, "magnitude",H5P_DEFAULT );
    chanlist[k].tsid = H5Dopen( chanlist[k].groupid, "timestamps" ,H5P_DEFAULT);
    
    chanlist[k].phsattr = H5Aopen( chanlist[k].phsdsid, "DataLen", H5P_DEFAULT );
    chanlist[k].magattr = H5Aopen( chanlist[k].magdsid, "DataLen", H5P_DEFAULT );
    chanlist[k].tsattr = H5Aopen( chanlist[k].tsid, "DataLen", H5P_DEFAULT );
   
   
      dataspace_id = H5Dget_space(chanlist[k].phsdsid);    /* dataspace handle */
   
    status  = H5Sget_simple_extent_dims(dataspace_id, d_dims, NULL);
    
    chanlist[k].datalen=d_dims[1];
   H5Sclose(dataspace_id);
   
    printf("Mag/Phase data size %d\n",chanlist[k].datalen);
    
   
      dataspace_id = H5Dget_space(chanlist[k].tsid);    /* dataspace handle */
   
    status  = H5Sget_simple_extent_dims(dataspace_id, d_dims, NULL);
      
    chanlist[k].tslen=d_dims[1];
   H5Sclose(dataspace_id);
    
    
    printf("Timestamp data size %d\n",chanlist[k].tslen);
    
    
    status =  H5Aread(chanlist[k].phsattr, H5T_NATIVE_INT, &dlen );
     chanlist[k].dataindex=dlen;
     
     printf("Phase/Mag num elements %d\n",chanlist[k].dataindex);
     
     
    status =  H5Aread(chanlist[k].tsattr, H5T_NATIVE_INT, &dlen );
     chanlist[k].tsindex=dlen;
     
     printf("Timestamp num elements %d\n",chanlist[k].tsindex);
     

}





/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  
int writeData(int k, int timestamp, float mag[], float phs[])
{
    int dslen;
    
    herr_t      status;                             
   
    hsize_t     count[2];              /* size of subset in the file */
    hsize_t     offset[2];             /* subset offset in the file */
    hsize_t     stride[2];
    hsize_t     block[2];
       
    hsize_t d_dims[2];
 
    hid_t dataspace_id;
    
    if (chanlist[k].dataindex+WAVELEN > chanlist[k].datalen)
    {
    
    //printf("extend len chan %d\n",chanlist[k].chan);
    hsize_t d_dims[2];
 

   d_dims[0]=1;
   d_dims[1] = chanlist[k].datalen + datasetlength;
   chanlist[k].datalen+=datasetlength;

    status = H5Dset_extent (chanlist[k].phsdsid, d_dims);
    status = H5Dset_extent (chanlist[k].magdsid, d_dims);
   
   d_dims[0]=1;
   d_dims[1] = chanlist[k].tslen + datasetlength/32;
    status = H5Dset_extent (chanlist[k].tsid, d_dims);
    chanlist[k].tslen+=datasetlength/32;
   
    }
    
    
    //
    // Set up stride, offset, count block in dastasets...
    //
    
    stride[0]=1;
    stride[1]=1;
    block[0]=1;
    block[1]=1;
    count[0]=1;
    count[1]=WAVELEN;
    offset[0]=0;
    
    
   //select point in the ts data set
   //write one point at coord [0,tsindex]
   
   //memspace_id is 1x32 array of floats. defined in main()
   
   
   //
   // inc data set index for phs and bag. set offset before write ps and mags
   //
   offset[1] = chanlist[k].dataindex;
   chanlist[k].dataindex+=WAVELEN;

   //
   // select and write phase data
   //
   
   dataspace_id = H5Dget_space(chanlist[k].phsdsid);

   status = H5Sselect_hyperslab(
   	dataspace_id, 
	H5S_SELECT_SET, 
	offset,
         stride, 
	 count, 
	 block);
	 
	 
   status = H5Dwrite(
   	chanlist[k].phsdsid, 
	H5T_NATIVE_FLOAT, 
	memspace_id, 
	dataspace_id,
	 H5P_DEFAULT,
         phs);
	 
	 
		     
  status = H5Sclose (dataspace_id);	
  
  	 //
	// wr the length in phase attr
	//
	
	
	dslen=chanlist[k].dataindex;
	status = H5Awrite (chanlist[k].phsattr, H5T_NATIVE_INT,&dslen);



   //
   // select and write mag data
   //
 

   dataspace_id = H5Dget_space(chanlist[k].magdsid);

   status = H5Sselect_hyperslab(
   	dataspace_id, 
	H5S_SELECT_SET, 
	offset,
         stride, 
	 count, 
	 block);
	 
	 
   status = H5Dwrite(
   	chanlist[k].magdsid, 
	H5T_NATIVE_FLOAT, 
	memspace_id, 
	dataspace_id,
	 H5P_DEFAULT,
         mag);
	 
	 
		     
  status = H5Sclose (dataspace_id);	
  
  	 //
	// wr the length in mag attr
	//
	
	
	dslen=chanlist[k].dataindex;
	status = H5Awrite (chanlist[k].magattr, H5T_NATIVE_INT,&dslen);


  
  
  //
  // select ONE point in timestamps andwrite timestamps
  // inc the ts index
  //	 
    count[0]=1;
    count[1]=1;
    offset[0]=0;
   
   offset[1] = chanlist[k].tsindex;
   chanlist[k].tsindex++;
   
   
   dataspace_id = H5Dget_space(chanlist[k].tsid);

   status = H5Sselect_hyperslab(
   	dataspace_id, 
	H5S_SELECT_SET, 
	offset,
         stride, 
	 count, 
	 block);
	 
	 
   status = H5Dwrite(
   	chanlist[k].tsid, 
	H5T_NATIVE_INT, 
	memspace_id2, 
	dataspace_id,
	 H5P_DEFAULT,
         &timestamp);
	 
	 
		     
  status = H5Sclose (dataspace_id);	


  	 //
	// wr the length in ts attr
	//
	
	
	dslen=chanlist[k].tsindex;
	status = H5Awrite (chanlist[k].tsattr, H5T_NATIVE_INT,&dslen);

} 




/***********************************************************************************************
 *
 *
 *********************************************************************************************/
  


void closeChannels(void)
{
 int k;
 
 
 printf("Closing channels\n");
 
 for ( k = 0; k< chanlist_len;k++)
 {
 
 
    	H5Aclose(chanlist[k].magattr);
    	H5Aclose(chanlist[k].phsattr);
    	H5Aclose(chanlist[k].tsattr);
 	H5Dclose(chanlist[k].magdsid);
 	H5Dclose(chanlist[k].phsdsid);
 	H5Dclose(chanlist[k].tsid);
	H5Gclose(chanlist[k].groupid);
	
 }

 H5Sclose(memspace_id);
 H5Sclose(memspace_id2);
 	
 H5Fclose(hfile); 



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
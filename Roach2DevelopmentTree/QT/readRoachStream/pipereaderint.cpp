#include "pipereaderint.h"

pipeReaderInt::pipeReaderInt(QString fname, QObject *parent) :
    QObject(parent),
    qa(),
    qb(),
    in_pipe(fname)
{
    is_got_close_message=false;
    is_pipe_open=false;

    in_pipe=0;
}

void pipeReaderInt::getData(void)
{





  int cnt=0;
  int stat = 0;

  while(!is_got_close_message && is_pipe_open &&stat==0)
   {
       //get piped images for ever. killing theadd will stop this.

      int nread = in_pipe.read(2048);

       if (free_queue.dequeueIfOk(&item))
       {

          stat =  pread.readDataBlock(in_pipe,item);

           data_queue.enqueue(item);


           test_frame_number++;
           emit newImageReady();
           printf("Received new Image\n"); fflush(stdout);
           cnt++;


       }

   }

   if (is_pipe_open)
   {
       printf("Close inopuit pipt");
       fflush(stdout);
       fclose(in_pipe);
       in_pipe  = 0;
       is_pipe_open==false;
   }
   //!! we must close pipe here

}










//====================================================================
//                              Slots
//====================================================================

//!! should be queud connection and rn on imagepipe thread.
void pipeReaderInt::openPipe()
{
   is_pipe_open=false;


   is_got_close_message =false;

   printf("pipeReader::openPipe()\n");fflush(stdout);




  if (true)
   {

      is_pipe_open = in_pipe.open(QIODevice::ReadOnly);


      if (is_pipe_open)
      {

          printf("pipeReader::openPipe  opened pipe %s\n");
          fflush(stdout);
      }

       //runs forever until closePIpe on other thread stops it.
      if (is_pipe_open)
           getPipeImages();
      else
      {
          printf("ERROR - pipeReader::openPipe could not open pipe %s");
          fflush(stdout);
      }

   }
}

//!! this shoudl NON queued and should run on calling thread, not image pipe thread.
void pipeReaderInt::closePipe()
{

   printf("pipeReader::closePipe()\n");fflush(stdout);
   is_got_close_message=true;

}


//
// take images from free quue and send to data quque, emit data ready signal.
// we have to had alrdy collected tons of images. the old iamges will be sitting on the free queue.
// we jsut reusethem this is for debugging for fast mpi
//


//!!TJM changed this alot- added fifo_incnt

//!!TJM changed this alot- added fifo_incnt


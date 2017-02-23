#if 1

#ifndef HDFFILESAVER_H
#define HDFFILESAVER_H

#include "filesaver.h"
#include "hdf5.h"


class hdfFileSaver : public fileSaver
{
public:
    explicit hdfFileSaver(QObject *parent = 0);

public:
 virtual void saveNow(void);
    int trap(void);


protected:

 //hdf 5 file
 hid_t hfile;
 //top group for data
 hid_t topgroup;
 // channel group
 hid_t channelgroup;
 //current dataset
 hid_t curdataset;
 //current space fr data
 hid_t curdataspace;
 //memory dataspace
 hid_t memdataspace;

 enum {rawdatasize = 2000000};

 float *rawdata;
};

#endif // HDFFILESAVER_H
#endif

#if 1
#include "unistd.h"
#include "hdffilesaver.h"

hdfFileSaver::hdfFileSaver(QObject *parent) :
    fileSaver(parent)
{
    rawdata = (float*)malloc(sizeof(float)*rawdatasize);
}

int hdfFileSaver::trap(void)
{
    int a = 2;
    a = a+1;
    return(a);
}

void hdfFileSaver::saveNow(void)
{
    QDir prnt;
    herr_t status;
    hsize_t maxdims[1];
    hsize_t d_dims[1];

    int rank = 1;

    hsize_t datasetlength;
    size_t      memdims[1];
    hsize_t     count[1];              /* size of subset in the file */
      hsize_t     offset[1];             /* subset offset in the file */
      hsize_t     mcount[1];
      hsize_t     moffset[1];
hid_t prop;

    if (events==0)
        return;



        if (access(fname.toStdString().c_str(), F_OK) ==-1)
        {
            hfile = H5Fcreate(
                        fname.toStdString().c_str(),
                        H5F_ACC_EXCL ,
                        H5P_DEFAULT,
                        H5P_DEFAULT ) ;

            topgroup = H5Gcreate(
                        hfile,
                        "iqdata_raw",
                        H5P_DEFAULT,
                        H5P_DEFAULT,
                        H5P_DEFAULT);


            hid_t aid3  = H5Screate(H5S_SCALAR);
            hid_t  atype = H5Tcopy(H5T_C_S1);
            H5Tset_size(atype, 4);
            hid_t  attr3 = H5Acreate1(topgroup, "type", atype, aid3, H5P_DEFAULT);
            status = H5Awrite(attr3, atype,"dict");
            H5Aclose(attr3);
            H5Tclose(atype);
            H5Sclose(aid3);


        }
        else
        {
           //printf("File already exists, will append\n");
            hfile = H5Fopen(
                fname.toStdString().c_str(),
                H5F_ACC_RDWR,
                H5P_DEFAULT );


            topgroup = H5Gopen(hfile, "iqdata_raw", H5P_DEFAULT);

            //fprintf(stderr,"Bad Hdf file already existant, cannot open\n");
         }


        if (hfile <=0 || topgroup <=0)
        {
           fprintf(stderr,"Bad Hdf file, cannot open\n");
           return;
        }


        if (true)
        {


            //QHash<int,QHash<QString,QList<float> > > events;
            QList<int> keys1=(*events).keys();
            for (int i=0;i<keys1.length();i++)
            {
                int chan = keys1[i];

                if ((*events)[chan]["bin"].length() > 0)
                {
                    int bin = (int)((*events)[chan]["bin"][0]);
                    QString dirname = QString("keyint_%1").arg(chan);



                    //turn off errors when we query the group, using open
                    hid_t error_stack = H5Eget_current_stack();
                    H5E_auto2_t  oldfunc;
                    void *old_client_data;
                    H5Eget_auto(error_stack, &oldfunc, &old_client_data);
                    H5Eset_auto(error_stack, NULL, NULL);

                    channelgroup = H5Gopen(
                                topgroup,
                                dirname.toStdString().c_str(),
                                H5P_DEFAULT);

                    //turn errors back on.
                    H5Eset_auto(error_stack, oldfunc, old_client_data);

                    if (channelgroup<0)
                    {
                        channelgroup = H5Gcreate(
                                    topgroup,
                                    dirname.toStdString().c_str(),
                                    H5P_DEFAULT,
                                    H5P_DEFAULT,
                                    H5P_DEFAULT);



                        hid_t aid3  = H5Screate(H5S_SCALAR);
                        hid_t  atype = H5Tcopy(H5T_C_S1);
                        H5Tset_size(atype, 4);
                        hid_t  attr3 = H5Acreate1(channelgroup, "type", atype, aid3, H5P_DEFAULT);
                        status = H5Awrite(attr3, atype,"dict");
                        H5Aclose(attr3);
                        H5Tclose(atype);
                        H5Sclose(aid3);




                    }
                    if (channelgroup!=0)
                    {

                        QList<QString> keys2=(*events)[keys1[i]].keys();
                        for (int i2=0;i2<keys2.length();i2++)
                        {
                            QString dname = QString("keystr_%1").arg(keys2[i2]);
                            datasetlength = (*events)[keys1[i]][keys2[i2]].length();

                            if (datasetlength>0)
                            {

                                //Try to open dataset if it exists

                                //turn off errors when we query the group, using open
                                hid_t error_stack = H5Eget_current_stack();
                                H5E_auto2_t  oldfunc;
                                void *old_client_data;
                                H5Eget_auto(error_stack, &oldfunc, &old_client_data);
                                H5Eset_auto(error_stack, NULL, NULL);

                                //query or open dataset
                                curdataset = H5Dopen(channelgroup,dname.toStdString().c_str(),H5P_DEFAULT);

                                //turn errors back on.
                                H5Eset_auto(error_stack, oldfunc, old_client_data);

                                //if cannot open dataset, create it, and make it chunked.
                                if (curdataset<=0)
                                {

                                    //set up size info, chunks etc...

                                    maxdims[0]=H5S_UNLIMITED;
                                     rank = 1;
                                    d_dims[0]=datasetlength;

                                    curdataspace=  H5Screate_simple(rank, d_dims,maxdims);


                                     prop = H5Pcreate(H5P_DATASET_CREATE);
                                    status = H5Pset_chunk(prop, rank, d_dims);

                                    if (status) trap();

                                    curdataset = H5Dcreate(
                                        channelgroup,
                                        dname.toStdString().c_str(),
                                        H5T_NATIVE_FLOAT,
                                        curdataspace,
                                        H5P_DEFAULT,
                                        prop,
                                        H5P_DEFAULT);


                                    hid_t aid3  = H5Screate(H5S_SCALAR);
                                    hid_t  atype = H5Tcopy(H5T_C_S1);
                                    H5Tset_size(atype, 5);
                                    hid_t  attr3 = H5Acreate1(curdataset, "type", atype, aid3, H5P_DEFAULT);
                                    status = H5Awrite(attr3, atype,"array");
                                    H5Aclose(attr3);
                                    H5Tclose(atype);
                                    H5Sclose(aid3);





                                    H5Pclose(prop);

                                }//if (curdataset<=0)
                                else
                                {
                                    //get dataspace from exant dataset
                                    curdataspace = H5Dget_space(curdataset);
                                    H5Sget_simple_extent_dims(curdataspace, d_dims, maxdims);
                                    H5Sclose(curdataspace);
                                    //if dataset already exist, extend its size

                                    d_dims[0] = d_dims[0] + datasetlength;
                                    status = H5Dset_extent(curdataset, d_dims);


                                    if (status) trap();

                                    curdataspace = H5Dget_space(curdataset);
                                    H5Sget_simple_extent_dims(curdataspace, d_dims, maxdims);



                                }//else

                                if (curdataset>0)
                                {

                                  //
                                  // Set up stride, offset, count block in dastasets...
                                  //

                                 // stride[0]=1;//hop size between floats in dataset...
                                  //block[0]=1;//get 1 slab
                                  count[0]=datasetlength;//size of hyperslab or chunk of data
                                  offset[0]=d_dims[0] - datasetlength;//offset from beginning of file.


                                  status = H5Sselect_hyperslab(
                                    curdataspace,
                                    H5S_SELECT_SET,
                                    offset,
                                    NULL,
                                    count,
                                    NULL);

                                  if (status) trap();


                                  rank = 1;


                                 memdims[0]=datasetlength;

                                 memdataspace=  H5Screate_simple(rank, (const hsize_t*)memdims,NULL);

                                 mcount[0] = datasetlength;
                                 moffset[0] = 0;

                                 status = H5Sselect_hyperslab(
                                   memdataspace,
                                   H5S_SELECT_SET,
                                   moffset,
                                   NULL,
                                   mcount,
                                   NULL);

                                  if (status) trap();


                                  for (int mmm=0;mmm<datasetlength;mmm++)
                                      this->rawdata[mmm]=(*events)[keys1[i]][keys2[i2]][mmm];

                                  status = H5Dwrite(
                                   curdataset,
                                   H5T_NATIVE_FLOAT,
                                   memdataspace,
                                   curdataspace,
                                    H5P_DEFAULT,
                                        this->rawdata);

                                  if (status) trap();

                                 H5Sclose(memdataspace);
                                 H5Sclose(curdataspace);
                                 H5Dclose(curdataset);


                                } //if (curdataset>0)

                            }

                        }//for (int i2=0;i2<keys2.length();i2++)


                        status = H5Gclose(channelgroup);

                    }//if (channelgroup!=0)
                }//if ((*events)[chan]["bin"].length() > 0)
            }//for (int i=0;i<keys1.length();i++)
        }//if (true)

        status = H5Gclose(topgroup);
        status = H5Fclose(hfile);

}



#endif

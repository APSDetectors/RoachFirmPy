'''

hdf.open('test.h5','r')

qq=hdf.read()






hdf.write(dd,'dd')


hdf.write(dd.iqdata,'iq')



hdf.close()



execfile('hdfSerdes.py')

hdf=hdfSerdes()


hdf.open('R2_33res_test.h5','w')


hdf.write(dd,'dd')




aa=range(100)

hdf.write(aa,'aa')

ab = [ range(100) ,range(50) ]

hdf.write(ab,'ab')


dct = { 'listxxx':range(100) , 'intxx':22,  'floatxxx':22.1  }

hdf.write(dct,'dct')


ar=numpy.arange(1000)


hdf.write(ar,'ar')


lar=[ arange(100), arange(200)]


hdf.write(lar,'lar')



arar = numpy.array(  [range(100), range(100)] )

hdf.write(arar,'arar')



lll = [ range(10), 3, 4, numpy.arange(100), [ range(10), range(10)  ]  , 'maddog is cool'   ]

hdf.write(lll,'lll')



ss = 'fhdfkjhsdkfjhsdkfjshdkfjhsdkfhsdfasdfasdf'

hdf.write(ss,'ss')



class inline: pass

obj=inline()


obj.name = 'inline obj'
obj.arx=numpy.arange(100)

hdf.write(obj,'obj')




hdf.close()


'''



import inspect
import h5py
import types

class hdfSerdes:

    def __init__(self):
    
        self.hdffile=None
    
    
           
    
    def write(self,mydata,grpname):
    
        if (self.hdffile!=None):
        

	       
            #self.iq_index = self.iq_index + 1
            self.writeObj(self.hdffile, mydata,grpname)



    #read hdf data. stick data in myobj, or make new inline() obj
    def read(self):
     
        if (self.hdffile!=None):
        

	       
            #self.iq_index = self.iq_index + 1
            data = self.readObj(self.hdffile)
            return(data)


    def readObj(self,parent):
    
       
            
            
        htype = type(parent)
        print parent
        
        if htype == h5py._hl.dataset.Dataset:
           
            
            ptype = parent.attrs['type']
            
            
            if ptype == 'list':
                data = parent.value.tolist()
            elif ptype == 'array':
                data = parent.value
            elif ptype == 'int':
                data  = int(parent.value[0])
            elif ptype == 'float':
                data  = float(parent.value[0])
                
            elif ptype == 'str':
                data  = str(parent.value[0])
            else:
                pass 
                
            print 'return dataset %s'%parent
                
            return(data)   
            

        elif htype==h5py._hl.group.Group:
       
       
            print 'in group %s'%parent
            
            ptype = parent.attrs['type']
            
            if ptype == 'dict':
                data = {}
            
            elif ptype == 'listOfContainers':
                data=[]
            elif ptype == 'arrayOfContainers':
                data =[]
            elif ptype=='instance':
                #try to make new instance of the class, else use inline
                try:
                    exec('data = %s()'%(parent.attrs['class']))
                except:
                    class inline:pass
                
                    data = inline()  
            else:
                print "unknown type"      
            
            
            print data
            
            for key_ in parent.keys():

                print 'group key %s'%key_  
                
                pyobj = self.readObj(parent[key_])
                


                if ptype == 'listOfContainers':
                    data.append(pyobj) 

                elif ptype == 'arrayOfContainers':
                    data.append(pyobj)
                elif ptype == 'dict':
                    
                    if 'keyint_' in key_:
                        key2 = int(key_[7:])
                        
                    elif 'keyfloat_' in key_:
                        key2 = float(key_[9:])

                    elif 'keystr_' in key_:
                        key2 = str(key_[7:])
                    else:
                        print "dict key error"
                        
                    data[key2]=pyobj
                        
                elif ptype == 'instance':
                    exec('data.%s=pyobj'%(key_) )
                else:
                    pass
                            
            if  ptype == 'arrayOfContainers':
                data = numpy.array(data)
                    

            return(data)

        
            
        elif htype==h5py._hl.files.File:
        
           #if have many keys, put resulting obks into dict.
            
            data = {}
            
            print 'infile %s'%parent

            nkeys = len(parent.keys())


            for key_ in parent.keys():


                print 'file key %s'%key_

                pyobj = self.readObj(
                    parent[key_])




                data[key_]=pyobj

               

            #if only one key, just return obj, not list
            if nkeys==1:
                return(pyobj)
            else:
                return(data)






    def writeObj(self,parent,mydata,dataname):
    
        if type(mydata)==types.InstanceType:
            grp=parent.create_group(dataname)

            grp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
            grp.attrs.create('type',numpy.array('instance'))
            grp.attrs.create('class',numpy.array(mydata.__class__.__name__))
    
            contents= inspect.getmembers(mydata)
            for c in contents:
                self.writeObj(grp,c[1],c[0])
                
                
                
        elif type(mydata)==list:
            if (self.isListOfContainers(mydata)):
                grp=parent.create_group(dataname)

                grp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
                grp.attrs.create('type',numpy.array('listOfContainers'))
                
                k=0
                for item in mydata:
                    iname = 'item_%d'%k
                    self.writeObj(grp,item,iname)
                    k=k+1
    
            else:
                dims=[len(mydata)]
                ds = parent.create_dataset(dataname, dims, dtype='f8', maxshape=dims)
                ds.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
                ds.attrs.create('type',numpy.array('list'))
                                
                ds[:]=mydata
                        
            

                
        elif type(mydata)==numpy.ndarray:
            if (self.isListOfContainers(mydata)):
                grp=parent.create_group(dataname)

                grp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
                grp.attrs.create('type',numpy.array('arrayOfContainers'))
                k=0
                for item in mydata:
                    iname = 'item_%d'%k
                    self.writeObj(grp,item,iname)
                    k=k+1
           
    
            else:
                dims=[len(mydata)]
                ds = parent.create_dataset(dataname, dims, dtype='f8', maxshape=dims)
                ds.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
                ds.attrs.create('type',numpy.array('array'))
                                
                ds[:]=mydata
                        


        elif type(mydata)==dict:

            grp=parent.create_group(dataname)

            grp.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
            grp.attrs.create('type',numpy.array('dict'))
            k=0
            for key_ in mydata.keys():
                val_=mydata[key_]
                
                if type(key_)==int or type(key_)==numpy.int64:
                
                    iname = 'keyint_%d'%key_
                    self.writeObj(grp,val_,iname)
                
                elif type(key_)==str:
                
                    iname = 'keystr_%s'%key_
                    self.writeObj(grp,val_,iname)
                    
                elif type(key_)==float:
                
                    iname = 'keyfloat_%f'%key_
                    self.writeObj(grp,val_,iname)
                else:
                    print "Unknown key type K=%s  T=%s"%(key_,type(key_))
                
                
                
                k=k+1

        elif type(mydata)==str or type(mydata)==unicode:
        
                if type(mydata)==unicode:
                    mydata = str(mydata)
                    
                dims=[1]
                ds = parent.create_dataset(dataname, dims, dtype='S%d'%len(mydata), maxshape=dims)
                ds.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
                ds.attrs.create('type',numpy.array('str'))
                                
                ds[:]=mydata




        elif type(mydata)==int:

               #print 'scalar'
               dims=[1]
               ds = parent.create_dataset(dataname, dims, dtype='i4', maxshape=dims)
               ds.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
               ds.attrs.create('type',numpy.array('int'))
               
               ds[0]=mydata
               #print ds

        elif type(mydata)==float or type(mydata)==numpy.float64:

               #print 'scalar'
               dims=[1]
               ds = parent.create_dataset(dataname, dims, dtype='f8', maxshape=dims)
               ds.attrs.create('timecreated',numpy.array(time.strftime('%m-%d-%Y %H:%M:%S')))
               ds.attrs.create('type',numpy.array('float'))
               
               ds[0]=mydata
               #print ds

        else:
            pass


        self.hdffile.flush()
        



    def close(self):
        if self.hdffile!=None:
            self.hdffile.flush()
            self.hdffile.close()
            self.hdffile=None
  
    
    def open(self,name,wrspec):
        
      
        self.close()


        self.hdffile = h5py.File(name,wrspec)


        print self.hdffile.keys()




    def isListOfContainers(self,lst):
        ans=False
        for x in lst:
            if type(x)==list or \
            type(x)==numpy.ndarray or \
            type(x)==str or \
            type(x)==dict or \
            type(x) == types.InstanceType:
                ans=True

		return(ans)





print "Loaded hdfSerdes.py"
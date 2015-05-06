#-----------------------------------------------------
# Author: Yaqiang Wang
# Date: 2014-12-27
# Purpose: MeteoInfo Dataset module
# Note: Jython
#-----------------------------------------------------
import os
from org.meteoinfo.data import GridData, StationData, DataMath, TableData, ArrayMath
from org.meteoinfo.data.meteodata import MeteoDataInfo
from org.meteoinfo.data.mapdata import MapDataManage

import dimdatafile
import dimvariable
import dimarray
import miarray
from dimdatafile import DimDataFile
from dimvariable import DimVariable
from dimarray import PyGridData, DimArray
from miarray import MIArray

from java.awt import Color

# Global variables
meteodatalist = []
c_meteodata = None
currentfolder = None

def isgriddata(gdata):
    return isinstance(gdata, PyGridData)
    
def isstationdata(sdata):
    return isinstance(sdata, PyStationData)

###############################################################         
# The encapsulate class of StationData
class PyStationData():
    
    # data must be a GridData object
    def __init__(self, data=None):
        self.data = data
    
    def add(self, other):
        gdata = None
        if isinstance(other, PyStationData):            
            gdata = PyStationData(self.data.add(other.data))
        else:
            gdata = PyStationData(self.data.add(other))
        return gdata
    
    def __add__(self, other):
        gdata = None
        print isinstance(other, PyStationData)
        if isinstance(other, PyStationData):            
            gdata = PyStationData(self.data.add(other.data))
        else:
            gdata = PyStationData(self.data.add(other))
        return gdata
        
    def __radd__(self, other):
        return PyStationData.__add__(self, other)
        
    def __sub__(self, other):
        gdata = None
        if isinstance(other, PyStationData):
            gdata = PyStationData(self.data.sub(other.data))
        else:
            gdata = PyStationData(self.data.sub(other))
        return gdata
        
    def __rsub__(self, other):
        gdata = None
        if isinstance(other, PyStationData):
            gdata = PyStationData(other.data.sub(self.data))
        else:
            gdata = PyStationData(DataMath.sub(other, self.data))
        return gdata
    
    def __mul__(self, other):
        gdata = None
        if isinstance(other, PyStationData):
            gdata = PyStationData(self.data.mul(other.data))
        else:
            gdata = PyStationData(self.data.mul(other))
        return gdata
        
    def __rmul__(self, other):
        return PyStationData.__mul__(self, other)
        
    def __div__(self, other):
        gdata = None
        if isinstance(other, PyStationData):
            gdata = PyStationData(self.data.div(other.data))
        else:
            gdata = PyStationData(self.data.div(other))
        return gdata
        
    def __rdiv__(self, other):
        gdata = None
        if isinstance(other, PyStationData):
            gdata = PyStationData(other.data.div(self.data))
        else:
            gdata = PyStationData(DataMath.div(other, self))
        return gdata
        
    # other must be a numeric data
    def __pow__(self, other):
        gdata = PyStationData(self.data.pow(other))
        return gdata

###############################################################        
#  The encapsulate class of TableData
class PyTableData():
    # Must be a TableData object
    def __init__(self, data=None):
        self.data = data
        
    def __getitem__(self, key):
        if isinstance(key, str):
            print key
            return self.data.getColumnData(key).getValidDataValues()
        return None

#################################################################  

def __getfilename(fname):
    if os.path.exists(fname):
        if os.path.isabs(fname):
            return fname
        else:
            return os.path.join(currentfolder, fname)
    else:
        if currentfolder != None:
            fname = os.path.join(currentfolder, fname)
            if os.path.isfile(fname):
                return fname
            else:
                print 'File not exist: ' + fname
                return None
        else:
            print 'File not exist: ' + fname
            return None
      
def addfile_grads(fname):
    fname = __getfilename(fname)
    meteodata = MeteoDataInfo()
    meteodata.openGrADSData(fname)
    __addmeteodata(meteodata)
    datafile = DimDataFile(meteodata)
    return datafile
    
def addfile(fname):
    fname = __getfilename(fname)
    if os.path.splitext(fname)[1] == '.ctl':
        return addfile_grads(fname)
    
    meteodata = MeteoDataInfo()
    meteodata.openData(fname)
    __addmeteodata(meteodata)
    datafile = DimDataFile(meteodata)
    return datafile
    
def addfile_nc(fname):
    fname = __getfilename(fname)
    meteodata = MeteoDataInfo()
    meteodata.openNetCDFData(fname)
    __addmeteodata(meteodata)
    datafile = DimDataFile(meteodata)
    return datafile
    
def addfile_arl(fname):
    fname = __getfilename(fname)
    meteodata = MeteoDataInfo()
    meteodata.openARLData(fname)
    __addmeteodata(meteodata)
    datafile = DimDataFile(meteodata)
    return datafile
    
def addfile_surfer(fname):
    fname = __getfilename(fname)
    meteodata = MeteoDataInfo()
    meteodata.openSurferGridData(fname)
    __addmeteodata(meteodata)
    datafile = DimDataFile(meteodata)
    return datafile
    
def addfile_mm5(fname):
    fname = __getfilename(fname)
    meteodata = MeteoDataInfo()
    meteodata.openMM5Data(fname)
    __addmeteodata(meteodata)
    datafile = DimDataFile(meteodata)
    return datafile
    
def addfile_micaps(fname):
    fname = __getfilename(fname)
    meteodata = MeteoDataInfo()
    meteodata.openMICAPSData(fname)
    __addmeteodata(meteodata)
    datafile = DimDataFile(meteodata)
    return datafile
    
def addfile_hyconc(fname):
    fname = __getfilename(fname)
    meteodata = MeteoDataInfo()
    meteodata.openHYSPLITConcData(fname)
    __addmeteodata(meteodata)
    datafile = DimDataFile(meteodata)
    return datafile

def __addmeteodata(meteodata):
    global c_meteodata, meteodatalist
    meteodatalist.append(meteodata)
    c_meteodata = meteodata
    #print 'Current meteodata: ' + c_meteodata.toString()        
    
def getgriddata(varname='var', timeindex=0, levelindex=0, yindex=None, xindex=None):
    if c_meteodata.isGridData():
        c_meteodata.setTimeIndex(timeindex)
        c_meteodata.setLevelIndex(levelindex)
        gdata = PyGridData(c_meteodata.getGridData(varname))
        return gdata
    else:
        return None
        
def getstationdata(varname='var', timeindex=0, levelindex=0):
    if c_meteodata.isStationData():
        c_meteodata.setTimeIndex(timeindex)
        c_meteodata.setLevelIndex(levelindex)
        sdata = PyStationData(c_meteodata.getStationData(varname))
        return sdata
    else:
        return None
        
def readtable(filename, **kwargs):
    delimiter = kwargs.pop('delimiter', ',')
    format = kwargs.pop('format', None)
    headerlines = kwargs.pop('headerlines', 0)
    encoding = kwargs.pop('encoding', 'UTF8')
    tdata = TableData()
    tdata.readASCIIFile(filename, delimiter, headerlines, format, encoding)
    return PyTableData(tdata)
    
def arange(start=0, stop=1, step=1, dtype=None):
    return MIArray(ArrayMath.arrayRange(start, stop, step))
    
def linspace(start=0, stop=1, n=100, dtype=None):
    return MIArray(ArrayMath.lineSpace(start, stop, n))
    
def zeros(n):
    return MIArray(ArrayMath.zeros(n))
    
def asgriddata(data):
    if isinstance(data, PyGridData):
        return data
    elif isinstance(data, DimArray):
        return data.asgriddata()
    else:
        return None
        
def shaperead(fn):
    layer = MapDataManage.loadLayer(fn)
    pgb = layer.getLegendScheme().getLegendBreaks().get(0)
    pgb.setDrawFill(False)
    pgb.setOutlineColor(Color.darkGray) 
    return layer
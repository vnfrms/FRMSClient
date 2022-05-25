#-*- coding: utf-8 -*-
##File tien ich chung
'''
Created on 24 May 2015
ThanhGIS updated May 2022

@author: NITACO
'''
from builtins import map
from builtins import object
from qgis.core import *
from qgis.core import QgsSpatialIndex
from decimal import Decimal
from PyQt5.uic import loadUiType
import webbrowser
import os
import datetime
#from qgis.core import QgsPalLabeling
#from qgis.gui import *
class Utils(object):
    #CHuyen tu dinh dang dd/MM/yyyy sang yyyy-MM-dd de cap nhat co so du lieu
    @staticmethod
    def convertDate(str):
        if str: 
            monitorDate = datetime.datetime.strptime(str,"%d/%M/%Y")
            monitorDate = monitorDate.strftime('%Y-%M-%d')
            return monitorDate
        return str
    @staticmethod
    def gdalUri(qgsDSURI):
        schema = ( u'schema=%s' % qgsDSURI.schema() ) if qgsDSURI.schema() else ''
        gdalUri = u'PG: dbname=%s host=%s user=%s password=%s port=%s mode=2 %s table=%s' % (qgsDSURI.database(), qgsDSURI.host(), qgsDSURI.username(), qgsDSURI.password(), qgsDSURI.port(), schema, qgsDSURI.table())
        return gdalUri

    @staticmethod
    def getDecimalFromText(str):
        try:
            result = Decimal(str)
        except:
            result = Decimal("0.0")
        return result
    
    @staticmethod
    def getIntFromText(str):
        result = 0
        try:
            result = int(str)
        except:
            result = 0
        return result
    
    @staticmethod
    def findAdjacentPlot(layer, selectedFeature):
        adj_ids = []
        adj_ids.append(selectedFeature.id())
        # Select all features along with their attributes
        allAttrs = layer.pendingAllAttributesList()
        layer.select(allAttrs)
        # Get all the features to start
        for (feature) in layer.getFeatures():
            allfeatures = {feature.id(): feature }
        # Build the spatial index for faster lookup.
        index = QgsSpatialIndex()
        list(map(index.insertFeature, list(allfeatures.values())))
        # Loop each feature in the layer again and get only the features that are going to touch.
        #for feature in allfeatures.values():
        ids = index.intersects(selectedFeature.geometry().boundingBox())
        for id in ids:
            f = allfeatures[id]
            touches = f.geometry().touches(selectedFeature.geometry())
            if touches == True:
                adj_ids.append(f.id())
                #print f.id()
        layer.deselect(allAttrs)
        return adj_ids
def get_ui_class(ui_file):
    """return class object of a uifile"""
    ui_file_full = '%s%sui%s%s' % (os.path.dirname(os.path.abspath(__file__)),
                                   os.sep, os.sep, ui_file)
    return loadUiType(ui_file_full)[0]
def open_url(url):
    """open URL in web browser"""

    webbrowser.open(url)
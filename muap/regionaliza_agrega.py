import pandas as import pd
import clusterpy
import numpy as np


def regionaliza_agrega(dataframe,shp_path='data/distritos_variables.shp',n_regiones=50):
    datos = clusterpy.importArcData(shp_path)
    datos.cluster('random',[datos.fieldNames[0]],50,dissolve=0)
    resultado = datos.getVars(['cve_dist',datos.fieldNames[-1]])
    df = pd.DataFrame(resultado)
    df = df.transpose()
    df.columns=['cve_dist','id_region']
    region = dataframe.merge(df,how='inner',on='cve_dist')
    agregados = region.groupby(by='id_region').sum()
    intensidad = agregados['comercio'] + agregados['viv'] + agregados['ocio']
    prop_comercio = agregados['comercio'] / intensidad
    prop_viv = agregados['viv'] / intensidad
    prop_ocio = agregados['ocio'] / intensidad
    entropia = (prop_comercio*np.log(prop_comercio) + prop_viv*np.log(prop_viv) + prop_ocio*np.log(prop_ocio))/np.log(3)
    agregados.ix[:,'entropia']= entropia
    return agregados

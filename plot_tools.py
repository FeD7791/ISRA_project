import numpy as np

def mesh_builder(x_lims:list,y_lims:list,n_elements:int, model):
    x = np.linspace(x_lims[0],x_lims[1],n_elements)
    y = np.linspace(y_lims[0],y_lims[1],n_elements)
    x_mesh,y_mesh = np.meshgrid(x,y)
    mesh = np.c_[x_mesh.ravel(),y_mesh.ravel()]
    pred = model.predict(mesh)
    return [x_mesh.ravel(),y_mesh.ravel(),pred]
from srctools import Property
import os, subprocess

class qc:
    ''' QC details the specifications of the model for generation '''
    def __init__(self,mdlname):
        self.__props = {
            'model_out':mdlname,
            'model_phys':None,
            'model_ref':None,
            'anims':[],
            'skins':[]
        }
    def add_skin(self,ski):
        ''' appends a skin to the model '''
        self.__props['skins'].append(ski)
    def __getattr__(self,attr):
        return self.__props[attr]
    def compile_raw(self):
        ''' outputs a string of the generated qc '''
class skin:
    def __init__(self,texlist):
        if not (all([isinstance(x,mat) for x in texlist])):
            raise Exception("All items in texture list of skin must be type str.")
        self.__texlist = texlist
class mat:
    def __init__(self,diffuse,normal=None,bump=None,glossy=None,tags=[]):
        self.vmt = Property('$basetexture',diffuse)
        if normal:
            self.vmt.append(Property('$normalmap',normal))
        if bump:
            self.vmt.append(Property('$bumpmap',bump))
        if glossy:
            self.vmt.append(Property('$envmap'))
            self.vmt.append(Property('$envmapmask',glossy))
        if len(tags):
            self.vmt.append(Property('%keywords',",".join(tags)))
    def compile(self,pth):
        ''' output the material to a vmt '''
        
class tex:
    def __init__(self,img):
        self.__img = img
        self.path = remove_postfix(img)+'.vtf'
    def compile(self):
        ''' output the texture to a vtf '''
        


def remove_postfix(st):
    ''' take a guess. It removes the file ending. '''
    return '.'.join(st.split('.')[:-1])

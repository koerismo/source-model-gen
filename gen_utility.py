from srctools import Property
import os, subprocess
''' A python library to automate material and model generation. '''
class qc:
    ''' QC details the specifications of the model for generation '''
    def __init__(self,mdlname,mdl_ref,phys_model=None,anims=[]):
        self.__props = {
            'model_out':mdlname,
            'model_phys':None,
            'model_ref':mdl_ref,
            'anims':[],
            'skins':[]
        }
    def add_skin(self,ski):
        ''' appends a skin to the model '''
        if (not isinstance(ski,skin)):
            raise Exception('Skin must be of type skin.')
        self.__props['skins'].append(ski)
    def __getattr__(self,attr):
        return self.__props[attr]
    def compile_raw(self):
        ''' outputs a string of the generated qc '''
        pass

    
class skin:
    ''' A collection of materials to be used on a model. '''
    def __init__(self,texlist):
        # Check for argument type
        if not (all([isinstance(x,mat) for x in texlist])):
            raise Exception("All items in texture list of skin must be type str.")
        # Check for material compatibility
        if not (all([x.mat_type in ['VertexLitGeneric','UnlitGeneric'] for x in texlist])):
            raise Exception('Materials for models should be VertexLitGeneric or UnlitGeneric.')
        self.__texlist = texlist

''' like to die instantly '''
 
class mat:
    ''' A source material file. This can be used on models or on brushes.'''
    def __init__(self,pth,diffuse,mat_type='LightmappedGeneric',normal=None,bump=None,glossy=None,tags=[]):
        if (not mat_type in ['LightmappedGeneric','VertexLitGeneric','UnlitGeneric']):
            raise Exception('mat_type should be LightmapperGeneric, VertexLitGeneric, or UnlitGeneric.')
        self.mat_type = mat_type
        
        for a,x in enumerate([diffuse,normal,bump,glossy]):
            if (not isinstance(x,tex) and not x is None):
                raise Exception(['diffuse','normal','bump','glossy'][a]+' must be of type tex.')
        self.path = pth
        self.vmt = Property(mat_type,[])
        self.__mats = [x for x in [diffuse,normal,bump,glossy] if x]
        ''' do image processing here '''
        diffuse = get_path_relative(pth,diffuse.path)
        self.vmt.append(Property('$basetexture',diffuse))
        if normal:
            normal = get_path_relative(pth,normal.path)
            self.vmt.append(Property('$normalmap',normal))
        if bump:
            bump = get_path_relative(pth,bump.path)
            self.vmt.append(Property('$bumpmap',bump))
        if glossy:
            glossy = get_path_relative(pth,glossy.path)
            self.vmt.append('$envmap','1')
            self.vmt.append(Property('$envmapmask',glossy))
        if len(tags):
            self.vmt.append(Property('%keywords',",".join(tags)))
    def compile(self):
        ''' output the material to a vmt '''
        for a,x in enumerate(self.__mats):
            y = ['diffuse','normal','bump','glossy'][a]
            if (os.path.isfile(x.__path)):
                print(f'VTF texture for {y} already exists. Copying to material location.')
                continue
            if not os.path.isfile(x.__img):
                raise Exception(f'Unable to find texture file for {y}.')
        pass

        
class tex:
    ''' An image file to be converted into something useable by materials. '''
    def __init__(self,img):
        self.__img = img
        self.path = remove_postfix(img)
        


def remove_postfix(st):
    ''' take a guess. It removes the file ending. '''
    return '.'.join(st.split('.')[:-1])

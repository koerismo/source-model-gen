# source-model-gen
A Python library to automate the full creation of models in Source

Example use:
```py
>>> mymdl = qc('test.mdl','test_ref.smd',phys_model='test_phys.smd')
>>> mytex = tex('test_texture.png')
>>> mymat = mat('test_mat.vmt',mytex,mat_type='VertexLitGeneric')
>>> myskin = skin([mymat])
>>> mymdl.add_skin(myskin)
```

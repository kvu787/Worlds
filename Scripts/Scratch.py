def inspect_stuff():
   print(bpy.context.active_object)
   print(type(bpy.context.active_object.keys()))
   print(list(bpy.context.active_object.keys()))
   print(type(bpy.context.active_object['1_BaseColor']))
   print(list(bpy.context.active_object['1_BaseColor']))
   print(dict(bpy.context.active_object))
   print(bpy.context.active_object)
   print(type(bpy.context.active_object.id_properties_ui('1_BaseColor')))
   print(bpy.context.active_object.id_properties_ui('1_BaseColor').as_dict())
   print(inspect.getmembers(bpy.context.active_object.id_properties_ui('1_BaseColor')))
   print(dir(bpy.context.active_object.id_properties_ui('1_BaseColor')))
   for x in dir(bpy.context.active_object):
       print(x)
   print(type(bpy.context.active_object.id_properties_ui('1_BaseColor')))
   for x in dir(bpy.context.active_object.id_properties_ui('1_BaseColor')):
       print(x)
   print('=====')
   print(bpy.context.active_object.id_properties_ui('1_BaseColor').as_dict())

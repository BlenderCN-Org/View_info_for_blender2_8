import bpy,blf
from collections import OrderedDict
bl_info = {
    "name":"View_info_for_blender2_8",
    "author": "iCyP",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "3DView->UI",
    "description": "Show info about view",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Scene"
}

def draw_change(self, context):
    if context.scene.icyp_view_info_flag:
        ICYP_OT_view_info_drawer.draw_func_add()
    else:
        ICYP_OT_view_info_drawer.draw_func_remove()
    return None

class ICYP_OT_view_info_drawer(bpy.types.Panel):
    bl_idname = "icyp.view_info"
    bl_label = "Show info about view"

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "View info"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        self.layout.prop(context.scene,"icyp_view_info_flag")
        self.layout.prop(context.scene,"icyp_view_info_text_size")
    

    draw_func = None
    @staticmethod
    def draw_func_add():
        if ICYP_OT_view_info_drawer.draw_func is not None:
            ICYP_OT_view_info_drawer.draw_func_remove()
        ICYP_OT_view_info_drawer.draw_func = bpy.types.SpaceView3D.draw_handler_add(
            ICYP_OT_view_info_drawer.texts_draw,
            (), 'WINDOW', 'POST_PIXEL')

    @staticmethod
    def draw_func_remove():
        if ICYP_OT_view_info_drawer.draw_func is not None:
            bpy.types.SpaceView3D.draw_handler_remove(
                ICYP_OT_view_info_drawer.draw_func, 'WINDOW')
            ICYP_OT_view_info_drawer.draw_func = None
    
    messages_dict = OrderedDict()
    @staticmethod
    def texts_draw():
        messages = ICYP_OT_view_info_drawer.messages_dict
        persp = bpy.context.space_data.region_3d.view_perspective
        if persp == "CAMERA":
            messages["Focal len"] =  f"Focal len :{bpy.context.space_data.camera.data.lens}"
        elif persp == "ORTHO":
             messages["Focal len"] = f"Focal len: ORTHO"
        else:
            messages["Focal len"] = f"Focal len :{bpy.context.space_data.lens}"
        messages["camera mode"] = f"camera mode :{bpy.context.space_data.region_3d.view_perspective}"
        #なんかちがうmessages["camera height"] = f"camera height :{bpy.context.space_data.region_3d.view_location[2]}"
        text_size = bpy.context.scene.icyp_view_info_text_size
        dpi = 72
        blf.size(0, text_size, dpi)
        for i,text in enumerate(messages.values()):
            blf.position(0, text_size, text_size*(i+1)+100, 0)
            blf.draw(0, f"{text}")


# アドオン有効化時の処理
classes = [ICYP_OT_view_info_drawer]
def register():
    bpy.types.Scene.icyp_view_info_flag = bpy.props.BoolProperty(default=False,update=draw_change,name="Show view info")
    bpy.types.Scene.icyp_view_info_text_size = bpy.props.IntProperty(default=20,min=1,name = "text size")
    for c in classes:
        bpy.utils.register_class(c)
    #bpy.app.handlers.load_post.append(draw_change)
    

# アドオン無効化時の処理
def unregister():
    del bpy.types.Scene.icyp_view_info_flag
    del bpy.types.Scene.icyp_view_info_text_size
    for c in classes:
        bpy.utils.unregister_class(c)
    #bpy.app.handlers.load_post.remove(draw_change)

if "__main__" == __name__:
    register()

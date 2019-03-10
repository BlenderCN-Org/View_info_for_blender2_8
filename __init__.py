import bpy,blf
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
    
    messages_set = [1]
    @staticmethod
    def texts_draw():
        ICYP_OT_view_info_drawer.messages_set[0] = f"forcus len :{bpy.context.space_data.lens}"
        text_size = 20
        dpi = 72
        blf.size(0, text_size, dpi)
        for i,text in enumerate(list(ICYP_OT_view_info_drawer.messages_set)):
            blf.position(0, text_size, text_size*(i+1)+100, 0)
            blf.draw(0, f"{text}")
        blf.position(0,text_size,text_size*(2+len(ICYP_OT_view_info_drawer.messages_set))+100,0)



# アドオン有効化時の処理
classes = [ICYP_OT_view_info_drawer]
def register():
    bpy.types.Scene.icyp_view_info_flag = bpy.props.BoolProperty(default=False,update=draw_change)
    for c in classes:
        bpy.utils.register_class(c)
    

# アドオン無効化時の処理
def unregister():
    del bpy.types.Scene.icyp_view_info_flag
    for c in classes:
        bpy.utils.unregister_class(c)

if "__main__" == __name__:
    register()

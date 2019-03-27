import bpy,blf
from bpy.app.handlers import persistent
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

@persistent
def draw_change_load_post(_):
    if bpy.context.scene.icyp_view_info_flag:
        ICYP_OT_view_info_drawer.draw_func_add()
    else:
        ICYP_OT_view_info_drawer.draw_func_remove()
    return None

def draw_change(self,context):
    if context.scene.icyp_view_info_flag:
        ICYP_OT_view_info_drawer.draw_func_add()
    else:
        ICYP_OT_view_info_drawer.draw_func_remove()
    return None

def camera_info(messages):
    persp = bpy.context.space_data.region_3d.view_perspective
    cam_messages = messages["camera_info"] = OrderedDict()
    if persp == "ORTHO":
        cam_messages["Focal len"] = f"Focal len: ORTHO"
    else:
        if persp == "CAMERA":
            focal_len = bpy.context.space_data.camera.data.lens
        else:
            focal_len = bpy.context.space_data.lens
        if bpy.context.space_data.camera is not None:
            camera = bpy.context.space_data.camera
            hit,loc,norm,_,_,_ = bpy.context.scene.ray_cast(bpy.context.view_layer,camera.location,[0,0,-1])
            if hit:
                cam_messages["CAMERA_HEIGHT"] = f"CAMERA_HEIGHT :{camera.location[2]-loc[2]:.2f}m"
            else:
                cam_messages["CAMERA_HEIGHT"] = f"CAMERA_HEIGHT :{camera.location[2]:.2f}m"
        else:
            if "CAMERA_HEIGHT" in cam_messages.keys():
                del cam_messages["CAMERA_HEIGHT"]
        cam_messages["Focal len"] = f"Focal len :{focal_len:.1f}"
        if focal_len >= 60:
            cam_messages["Focal len"] += " ZOOM"
        elif focal_len >= 47 and focal_len <= 52:
            cam_messages["Focal len"] += " Eye like"
        elif focal_len <= 25:
            cam_messages["Focal len"] += " WIDE"

    cam_messages["camera mode"] = f"camera mode :{bpy.context.space_data.region_3d.view_perspective}"
    return

def mesh_info(messages):
    mesh_messages = messages["mesh_info"] = OrderedDict()
    obj = bpy.context.active_object
    if obj.active_shape_key is not None:
        mesh_messages["ACTIVE_SHAPE"]=f"ACTIVE SHAPE KEY : {obj.active_shape_key.name}"
    else:
        del mesh_messages["AC"]

    return

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
        self.layout.prop(context.scene,"icyp_view_info_text_color")
    

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
    draw_dict = dict()
    @staticmethod
    def texts_draw():
        messages_parent = ICYP_OT_view_info_drawer.messages_dict
        draw_dict = ICYP_OT_view_info_drawer.draw_dict
        camera_info(messages_parent)
        draw_dict["camera_info"] = True
        if bpy.context.mode == "EDIT_MESH":
            mesh_info(messages_parent)
            draw_dict["mesh_info"] = True
        else:
            draw_dict["mesh_info"] = False
        #なんかちがうmessages["camera height"] = f"camera height :{bpy.context.space_data.region_3d.view_location[2]}"
        text_size = bpy.context.scene.icyp_view_info_text_size
        text_color = bpy.context.scene.icyp_view_info_text_color
        dpi = 72
        blf.size(0, text_size, dpi)
        blf.color(0,*text_color,1)
        blf.enable(0,blf.SHADOW)
        blf.shadow(0,3,0,0,0,1) #fontid shadowlevel r g b a
        blf.shadow_offset(0,1,-1) #fontid x(pixel) y
        for i,text in enumerate([(log_func,message) for log_func,messages in messages_parent.items() for message in messages.values()]):
            if draw_dict[text[0]]:
                blf.position(0, text_size, text_size*(i+1)+100, 0)
                blf.draw(0, f"{text[1]}")
            else:
                i -= 1


# アドオン有効化時の処理
classes = [ICYP_OT_view_info_drawer]
def register():
    bpy.types.Scene.icyp_view_info_flag = bpy.props.BoolProperty(default=False,update=draw_change,name="Show view info")
    bpy.types.Scene.icyp_view_info_text_size = bpy.props.IntProperty(default=20,min=1,name = "text size")
    bpy.types.Scene.icyp_view_info_text_color = bpy.props.FloatVectorProperty(name="Text color", subtype="COLOR", default=[0.8, 1.0, 0.4], min=0, max=1)
    for c in classes:
        bpy.utils.register_class(c)
    bpy.app.handlers.load_post.append(draw_change_load_post)

# アドオン無効化時の処理
def unregister():
    del bpy.types.Scene.icyp_view_info_flag
    del bpy.types.Scene.icyp_view_info_text_size
    del bpy.types.Scene.icyp_view_info_text_color
    for c in classes:
        bpy.utils.unregister_class(c)
    bpy.app.handlers.load_post.remove(draw_change_load_post)

if "__main__" == __name__:
    register()

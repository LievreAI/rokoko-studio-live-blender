import bpy
from ..core import animations, animation_lists
from ..operators.detector import DetectFaceShapes


# Create a panel in the Object category of all objects
class ObjectsPanel(bpy.types.Panel):
    bl_label = "Rokoko Studio Live"
    bl_idname = "OBJECT_PT_rsl_objects"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj.type == 'ARMATURE':
            self.draw_actor(context, layout)

        elif obj.type == 'MESH':
            self.draw_tracker(context, layout)
            self.draw_face(context, layout)

        else:
            self.draw_tracker(context, layout)

    @staticmethod
    def draw_tracker(context, layout):
        row = layout.row(align=True)
        row.label(text='Attach to tracker or prop:')

        if not animations.trackers and not animations.props:
            row = layout.row(align=True)
            row.label(text='No prop or tracker data available.', icon='INFO')
            return

        row = layout.row(align=True)
        row.prop(context.object, 'rsl_animations_props_trackers')

    @staticmethod
    def draw_actor(context, layout):
        row = layout.row(align=True)
        row.label(text='Attach to actor:')

        if not animations.actors:
            row = layout.row(align=True)
            row.label(text='No actor data available.', icon='INFO')
            return

        row = layout.row(align=True)
        row.prop(context.object, 'rsl_animations_actors')

    @staticmethod
    def draw_face(context, layout):
        layout.separator()

        row = layout.row(align=True)
        row.label(text='Attach to face:')

        if not animations.faces:
            row = layout.row(align=True)
            row.label(text='No face data available.', icon='INFO')
            return

        row = layout.row(align=True)
        row.prop(context.object, 'rsl_animations_faces')

        if context.object.rsl_animations_faces and context.object.rsl_animations_faces != 'None':
            layout.separator()
            row = layout.row(align=True)
            row.label(text='Select Shapekeys:')
            row.operator(DetectFaceShapes.bl_idname)

            mesh = bpy.data.meshes[context.object.name]
            for shape in animation_lists.face_shapes:
                row = layout.row(align=True)
                row.prop_search(mesh, 'rsl_face_' + shape, context.object.data.shape_keys, "key_blocks", text=shape)

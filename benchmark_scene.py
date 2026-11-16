import bpy
import sys
import time

argv = sys.argv[sys.argv.index("--") + 1 :]
start_frame = int(argv[0])
end_frame = int(argv[1])
shard_id = argv[2]

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 64
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.02
scene.cycles.use_denoising = True
scene.cycles.denoiser = "OPENIMAGEDENOISE"
scene.view_settings.view_transform = "AgX"

scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.fps = 24

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# Stoic Marble Column + Dramatic Key Light
bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1, depth=4, location=(0, 0, 2))
col = bpy.context.active_object
mat = bpy.data.materials.new(name="Marble")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.85, 0.83, 0.78, 1.0)
bsdf.inputs["Roughness"].default_value = 0.25
col.data.materials.append(mat)

bpy.ops.object.light_add(type="AREA", location=(3, -3, 5))
light = bpy.context.active_object
light.data.energy = 800
light.data.size = 2.0

bpy.ops.object.camera_add(location=(0, -6, 2.2), rotation=(1.45, 0, 0))
cam = bpy.context.active_object
scene.camera = cam
cam.keyframe_insert(data_path="location", frame=1)
cam.location.y = -4.5
cam.keyframe_insert(data_path="location", frame=240)

scene.frame_start = start_frame
scene.frame_end = end_frame
scene.render.filepath = f"/tmp/shard_{shard_id}_frame_"

t0 = time.time()
bpy.ops.render.render(animation=True)
elapsed = time.time() - t0
total_frames = (end_frame - start_frame) + 1
print(f"BENCHMARK_RESULT | Shard {shard_id} | Frames: {total_frames} | Total: {elapsed:.2f}s | Avg: {elapsed/total_frames:.2f}s/frame")

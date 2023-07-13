import os
import shutil
from pathlib import Path
from meshlib import mrmeshpy

in_path = r"Input Path"
out_path = r"Output Path"

decimate = True
decimate_deviation = 0.02  # Controls the max deviation (what unit is this in?)
# .5 = visible number of sides on rivets. 113/379 MB = 29% of original
# .02 = Can't visually tell. 153/379 MB = 40% of original
# No decimation, 278/379 MB = 73% of original


root = in_path
for path, dirs, files in os.walk(in_path):
    print(path)
    for file in files:
        name_no_ext, extension = os.path.splitext(file)
        is_mesh = (extension.lower() in [".obj", ".stl"])

        new_file_name = file
        if is_mesh:
            new_file_name = name_no_ext + ".obj"

        original_file_path = os.path.join(path, file)
        rel_path = os.path.relpath(path, root)
        rel_file_path = os.path.join(rel_path, new_file_name)
        output_path = os.path.join(out_path, rel_file_path)
        output_folder = os.path.dirname(output_path)
        Path(output_folder).mkdir(parents=True, exist_ok=True)  # Make directory if needed
        print("Copying {} to {}".format(original_file_path, output_path))
        if is_mesh:
            mesh = mrmeshpy.loadMesh(mrmeshpy.Path(original_file_path))
            if decimate:
                settings = mrmeshpy.DecimateSettings()  # https://meshinspector.github.io/MeshLib/html/structMR_1_1DecimateSettings.html
                settings.maxError = decimate_deviation
                mrmeshpy.decimateMesh(mesh, settings)
                # Consider using https://github.com/HusseinBakri/3DMeshBulkSimplification instead?
            mrmeshpy.saveMesh(mesh, mrmeshpy.Path(output_path))
        else:
            shutil.copyfile(original_file_path, output_path)

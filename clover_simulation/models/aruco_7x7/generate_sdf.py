import os
from pathlib import Path

# Path to your textures directory
textures_dir = Path(os.getcwd()) / 'materials/textures'
output_file = Path(os.getcwd()) / 'aruco_model_7x7.sdf'

# Get list of marker PNG files
marker_files = sorted(
    [f for f in os.listdir(textures_dir) if f.startswith("aruco_") and f.endswith(".png")]
)


# Sort numerically by marker ID
marker_ids = [int(f.split('_')[3].split('.')[0]) for f in marker_files]
# marker_files = [f"aruco_marker_2_{i}.png" for i in sorted(marker_ids)]

# Start building SDF content
sdf_content = '''<?xml version='1.0' encoding='UTF-8'?>
<sdf version="1.6">
  <model name="aruco_marker">
    <static>true</static>
    <link name="link">
'''

row = 0.0
col = 6.0

# Add visual blocks
for id in marker_ids:
    filename = f"aruco_marker_2_{id}.png"
    sdf_content += f'''
      <visual name="{id}">
        <pose>{row} {col} 0 0 0 0</pose>
        <geometry>
          <box>
            <size>0.33 0.33 0.001</size>
          </box>
        </geometry>
        <material>
          <script>
            <uri>model://aruco_7x7/materials/scripts</uri>
            <uri>model://aruco_7x7/materials/textures</uri>
            <name>aruco/marker_2_{id}</name>
          </script>
        </material>
      </visual>
    '''

    row += 1.0  

    if row > 6.0:
      row = 0.0
      col -= 1.0

    if col == 0.0:
      break

# Close tags
sdf_content += '''    </link>
  </model>
</sdf>
'''

# Write to file
with open(output_file, 'w') as f:
    f.write(sdf_content)

print(f"Wrote {len(marker_files)} markers to {output_file}")
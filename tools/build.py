"""Rebuild every SVG from the source media.  Usage:  python tools/build.py
Needs:  pip install pillow numpy scipy fonttools brotli imageio-ffmpeg
Steps:  cut characters out of the checkerboard JPGs -> extract the wave frames -> encode assets -> render 5 SVGs into ../assets
"""
import os, subprocess, sys, glob, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE, SRC = os.path.join(HERE, '.cache'), os.path.join(HERE, 'src')
os.makedirs(CACHE, exist_ok=True)
os.makedirs(os.path.join(HERE, '..', 'assets'), exist_ok=True)
py = sys.executable


def run(*a):
    subprocess.run([py, *a], check=True, cwd=HERE)


# 1) cutouts (crop + exclusion box keep the neon "Amy Rouge" lettering out of the pointing pose)
run('cutout.py', os.path.join(SRC, 'handles.jpg'), os.path.join(CACHE, 'point_full.png'), '980,100,1780,1536', '520,600,800,1436')
run('cutout.py', os.path.join(SRC, 'id.jpg'), os.path.join(CACHE, 'id_full.png'), '')

# 2) the wave: 2.65s starting at 6.75s of the 10s clip, every frame (24 fps)
import imageio_ffmpeg
frames = os.path.join(CACHE, 'frames')
shutil.rmtree(frames, ignore_errors=True); os.makedirs(frames)
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-loglevel', 'error', '-ss', '6.75', '-i', os.path.join(SRC, 'hero video.mp4'),
                '-t', '2.65', '-vsync', '0', os.path.join(frames, 'f%03d.png')], check=True)
print('frames:', len(glob.glob(frames + '/*.png')))

# 3) encode + 4) render
run('prep.py')
for s in ('hero', 'about', 'stack', 'dash', 'connect'):
    run(s + '.py')

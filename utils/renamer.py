import os
import glob

os.chdir("skills")
for oldfile in glob.glob("*.png"):
    newfile = oldfile.replace(".png", ".jpg")
    print(f"Renamed {oldfile}")
    os.rename(oldfile, newfile)
    os.rename(newfile, oldfile)